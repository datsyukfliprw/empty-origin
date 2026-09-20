#!/usr/bin/env python3
"""Apply the reviewed, hash-guarded ARC repair once and rebuild the EPUB.

Patch JSON contains zero-based line slices and complete expected before/after
SHA-256 hashes. All target files and the complete manuscript are checked before
any source file is written. Rerunning on the exact repaired text is harmless;
any other manuscript drift stops the operation. This script uses no network.
"""
from __future__ import annotations
import difflib
import hashlib
import json
import re
from pathlib import Path
from xml.etree import ElementTree as ET
import zipfile
from build_arc import build, blocks, inline

ROOT = Path(__file__).resolve().parents[1]
BEFORE = '8d2293e0ab418cd13823dd7b438012b4c124204bc3227fe5794617a62bc68229'
AFTER = '9e202c70ad94ad5ec4b99197e7fbcf3ea1d0a4b577d9a127e6fc6c5be4e6f1c5'
EPUB = '47cf4d1639eb128e57da2a488bda260fcdafcd5923a8c6b44510d04a395c0dc7'

def sha(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def need(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)

def displays(text: str) -> list[str]:
    return [line for line in text.splitlines()
            if re.fullmatch(r'\*?\*?\[.*\]\*?\*?', line)
            or re.fullmatch(r'\*\*[\d /→]+\*\*', line)]

def main() -> None:
    changes = []
    for suffix in ('a', 'b'):
        source = ROOT / f'tools/arc_repair_data/2026-09-19.{suffix}.json'
        changes.extend(json.loads(source.read_text(encoding='utf-8')))
    paths = [f'book1/chapters/chapter-{n:02d}.md' for n in range(1, 33)]
    original = {path: (ROOT / path).read_text(encoding='utf-8') for path in paths}
    compiled_before = '\n\n'.join(original[p].strip() for p in paths) + '\n'
    need(sha(compiled_before) in (BEFORE, AFTER), 'Unexpected canonical manuscript snapshot')
    need((ROOT / 'book1/WORKING_DRAFT.md').read_text(encoding='utf-8') == compiled_before,
         'The existing compilation is not synchronized; refusing to guess')
    staged = {}
    diff = []
    for entry in changes:
        path = entry['path']
        need(path == 'README.md' or path.startswith('book1/'), 'Unexpected patch path')
        need('..' not in Path(path).parts and not Path(path).is_absolute(), 'Unsafe path')
        need(path not in staged, f'Duplicate target: {path}')
        old = (ROOT / path).read_text(encoding='utf-8')
        if sha(old) == entry['after']:
            staged[path] = old
            continue
        need(sha(old) == entry['before'], f'Input changed: {path}')
        lines = old.splitlines(keepends=True)
        last = len(lines) + 1
        for start, end, replacement in reversed(entry['patches']):
            need(0 <= start <= end < last, f'Invalid or overlapping slices: {path}')
            lines[start:end] = replacement
            last = start + 1
        new = ''.join(lines)
        need(sha(new) == entry['after'], f'Result mismatch: {path}')
        staged[path] = new
        diff.extend(difflib.unified_diff(old.splitlines(True), new.splitlines(True),
                                       fromfile='a/' + path, tofile='b/' + path))
    texts = [staged.get(path, original[path]) for path in paths]
    compiled = '\n\n'.join(text.strip() for text in texts) + '\n'
    need(sha(compiled) == AFTER, 'Final manuscript fingerprint differs from proofed ARC')
    need(sum(len(text.split()) for text in texts) == 100303, 'Unexpected word count')
    for path, text in zip(paths, texts):
        need(displays(text) == displays(original[path]), f'System display drift: {path}')
        need(text.splitlines().count('---') == original[path].splitlines().count('---'),
             f'Scene break drift: {path}')
        need(text.count('“') == text.count('”'), f'Unpaired dialogue quotes: {path}')
    # All source checks passed. Only now touch the canonical files.
    for path, text in staged.items():
        (ROOT / path).write_text(text, encoding='utf-8')
    (ROOT / 'book1/WORKING_DRAFT.md').write_text(compiled, encoding='utf-8')
    if diff:
        (ROOT / 'book1/ARC_REPAIR_PATCH_2026-09-19.diff').write_text(''.join(diff), encoding='utf-8')
    output = ROOT / 'book1/arc'
    manifest = build(ROOT, output)
    need(manifest['epub_sha256'] == EPUB, 'EPUB differs from the locally proofed edition')
    ns = {'h': 'http://www.w3.org/1999/xhtml', 'o': 'http://www.idpf.org/2007/opf'}
    with zipfile.ZipFile(output / 'The_Unheld_Warder_ARC.epub') as archive:
        need(archive.namelist()[0] == 'mimetype', 'EPUB mimetype must be first')
        need(archive.getinfo('mimetype').compress_type == zipfile.ZIP_STORED, 'Compressed mimetype')
        opf = ET.fromstring(archive.read('EPUB/package.opf'))
        spine = [e.attrib['idref'] for e in opf.findall('o:spine/o:itemref', ns)]
        need(spine == ['title'] + [f'chapter-{n:02d}' for n in range(1,33)], 'Reading order mismatch')
        for entry in opf.findall('o:manifest/o:item', ns):
            need('EPUB/' + entry.attrib['href'] in archive.namelist(), 'Missing manifest target')
        nav = ET.fromstring(archive.read('EPUB/nav.xhtml'))
        need(len(nav.findall("h:body/h:nav[@id='toc']//h:a", ns)) == 32, 'Chapter navigation mismatch')
        for n, text in enumerate(texts, 1):
            chapter = ET.fromstring(archive.read(f'EPUB/Text/chapter-{n:02d}.xhtml'))
            section = chapter.find('h:body/h:section', ns)
            actual = [''.join(e.itertext()) for e in section]
            expected = ['* * *' if kind == 'scene-break' else
                        ''.join(ET.fromstring('<p>' + inline(s) + '</p>').itertext())
                        for kind, s in blocks(text)]
            need(actual == expected, f'EPUB text mismatch: chapter {n}')
    verification = {'source_sha256': AFTER, 'whitespace_word_count': 100303,
                    'chapters': 32, 'source_and_compilation': 'pass',
                    'epub_manifest_spine_navigation_text': 'pass',
                    'epub_sha256': EPUB,
                    'system_displays_preserved': sum(len(displays(t)) for t in texts),
                    'scene_breaks_preserved': sum(t.splitlines().count('---') for t in texts),
                    'scope': 'Repeatable source and EPUB checks. PDF and browser checks were performed separately locally.'}
    (output / 'ARC_REMOTE_VERIFICATION.json').write_text(json.dumps(verification, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(verification, indent=2))

if __name__ == '__main__':
    main()
