#!/usr/bin/env python3
"""Build an EPUB 3 ARC from canonical chapters; optionally make a PDF.

EPUB generation uses only the Python standard library. PDF output additionally
requires ReportLab, Noto Serif and DejaVu Sans installed on the host.
No network calls, publishing, account access, or changes to chapter prose occur.
"""
from __future__ import annotations
import argparse, hashlib, html, json, re, uuid, zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

TITLE = 'The Unheld Warder'
REVISION = '2026-09-19'
CSS = '''html { color: #171717; background: #fff; }
body { font-family: Georgia, "Noto Serif", serif; line-height: 1.45; margin: 5%; }
p { margin: 0 0 .15em; text-indent: 1.15em; orphans: 2; widows: 2; }
h1 { font-size: 1.25em; font-weight: normal; text-align: center; margin: 2.5em 0 2em; }
p.first { text-indent: 0; }
p.scene-break { text-indent: 0; text-align: center; margin: 1em 0; page-break-after: avoid; }
p.system { font-family: Arial, "Noto Sans", sans-serif; font-size: .87em; text-indent: 0;
 margin: .3em .5em; line-height: 1.5; overflow-wrap: anywhere; }
.title-page { text-align: center; padding-top: 14%; }
.title-page h1 { font-size: 2em; margin-bottom: .7em; }
.title-page p { text-indent: 0; margin: .8em 0; }
.edition { font-family: Arial, sans-serif; font-size: .8em; letter-spacing: .06em; }
nav ol { padding-left: 1.4em; }
nav li { margin-bottom: .4em; }
nav a { color: inherit; }
'''

def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def inline(text: str) -> str:
    """Escape source text before translating the two inline styles in this novel."""
    escaped = html.escape(text, quote=False)
    escaped = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', escaped)
    escaped = re.sub(r'(?<!\*)\*([^*]+?)\*(?!\*)', r'<em>\1</em>', escaped)
    return escaped

def blocks(text: str) -> list[tuple[str, str]]:
    parts = re.split(r'\n\s*\n', text.strip())
    result: list[tuple[str, str]] = []
    first = True
    for i, part in enumerate(parts):
        part = ' '.join(part.splitlines()).strip()
        if i == 0:
            result.append(('heading', part))
            continue
        if part == '---':
            result.append(('scene-break', '* * *'))
            first = True
            continue
        plain = part.removeprefix('**').removesuffix('**')
        system = ((plain.startswith('[') and plain.endswith(']')) or
                  bool(re.fullmatch(r'\*\*[\d /→]+\*\*', part)))
        kind = 'system' if system else ('first' if first else 'body')
        result.append((kind, part))
        first = False
    return result

def xhtml(title: str, body: str, css_path: str) -> str:
    return ('<?xml version="1.0" encoding="utf-8"?>\n'
            '<!DOCTYPE html>\n'
            '<html xmlns="http://www.w3.org/1999/xhtml" '
            'xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en-US" lang="en-US">'
            f'<head><title>{html.escape(title)}</title>'
            '<meta charset="utf-8"/>'
            f'<link rel="stylesheet" type="text/css" href="{css_path}"/>'
            f'</head><body>{body}</body></html>')

def chapter_body(number: int, parsed: list[tuple[str, str]]) -> str:
    out = [f'<section epub:type="chapter" id="chapter-{number:02d}">']
    for kind, text in parsed:
        if kind == 'heading':
            out.append(f'<h1>{inline(text)}</h1>')
        else:
            out.append(f'<p class="{kind}">{html.escape(text) if kind == "scene-break" else inline(text)}</p>')
    return '\n'.join(out + ['</section>'])

def make_pdf(output: Path, chapters: list[tuple[str, str]], count: int,
             source_hash: str) -> dict:
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame,
        Paragraph, PageBreak, Spacer, KeepTogether)
    fontdir = Path('/usr/share/fonts/truetype/noto')
    fonts = {'Novel': 'NotoSerif-Regular.ttf', 'Novel-Bold': 'NotoSerif-Bold.ttf',
             'Novel-Italic': 'NotoSerif-Italic.ttf',
             'Novel-BoldItalic': 'NotoSerif-BoldItalic.ttf',
             'Interface': '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
             'Interface-Bold': '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'}
    for name, filename in fonts.items():
        p = fontdir / filename
        if not p.is_file():
            raise FileNotFoundError(f'PDF font missing: {p}')
        pdfmetrics.registerFont(TTFont(name, str(p)))
    pdfmetrics.registerFontFamily('Novel', normal='Novel', bold='Novel-Bold',
        italic='Novel-Italic', boldItalic='Novel-BoldItalic')
    pdfmetrics.registerFontFamily('Interface', normal='Interface', bold='Interface-Bold',
        italic='Interface', boldItalic='Interface-Bold')
    width, height = 432, 648  # 6 by 9 inches
    left, right, top, bottom = 49, 49, 49, 45
    starts = []
    class ArcDocument(BaseDocTemplate):
        def afterFlowable(self, flowable):
            chapter = getattr(flowable, 'chapter_number', None)
            if chapter is not None:
                key = f'chapter-{chapter:02d}'
                self.canv.bookmarkPage(key)
                self.canv.addOutlineEntry(flowable.getPlainText(), key, 0, False)
                starts.append({'chapter': chapter, 'pdf_page': self.page,
                               'printed_page': self.page - 2})
    def furniture(canvas, doc):
        if doc.page <= 2:
            return
        canvas.saveState()
        canvas.setFont('Interface', 7)
        canvas.drawString(left, height - 28, TITLE.upper())
        canvas.drawRightString(width - right, height - 28, 'ADVANCE READER COPY')
        canvas.setFont('Interface', 8)
        canvas.drawCentredString(width / 2, 24, str(doc.page - 2))
        canvas.restoreState()
    doc = ArcDocument(str(output), pagesize=(width, height),
        title=TITLE, subject=f'Advance Reader Copy, revision {REVISION}',
        author='', leftMargin=left, rightMargin=right, topMargin=top,
        bottomMargin=bottom, pageCompression=1)
    frame = Frame(left, bottom, width-left-right, height-top-bottom,
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates(PageTemplate(id='novel', frames=[frame], onPage=furniture))
    body = ParagraphStyle('Body', fontName='Novel', fontSize=10.5, leading=14,
        firstLineIndent=12, spaceAfter=.8, alignment=TA_LEFT,
        allowWidows=0, allowOrphans=0, splitLongWords=1)
    first = ParagraphStyle('First', parent=body, firstLineIndent=0)
    system = ParagraphStyle('System', fontName='Interface', fontSize=9.0,
        leading=12.5, leftIndent=9, rightIndent=9, spaceBefore=2, spaceAfter=2,
        firstLineIndent=0, allowWidows=0, allowOrphans=0)
    scene = ParagraphStyle('Scene', parent=body, alignment=TA_CENTER,
        firstLineIndent=0, spaceBefore=8, spaceAfter=8, keepWithNext=1)
    head = ParagraphStyle('Chapter', fontName='Novel', fontSize=14,
        leading=20, alignment=TA_CENTER, spaceBefore=30, spaceAfter=28,
        keepWithNext=1)
    title_style = ParagraphStyle('Title', fontName='Novel', fontSize=27,
        leading=34, alignment=TA_CENTER, spaceAfter=24)
    label = ParagraphStyle('Label', fontName='Interface', fontSize=9,
        leading=15, alignment=TA_CENTER, spaceAfter=12)
    note = ParagraphStyle('Note', parent=body, fontSize=10, leading=15,
        firstLineIndent=0, spaceAfter=15)
    story = [Spacer(1, 125), Paragraph('The Unheld<br/>Warder', title_style),
        Paragraph('BOOK ONE', label), Spacer(1, 30),
        Paragraph('ADVANCE READER COPY', label),
        Paragraph(f'Revision {REVISION}', label), PageBreak(), Spacer(1, 80),
        Paragraph('About this reading edition', head),
        Paragraph('This edition contains the complete thirty-two-chapter Book One manuscript. '
                  'Please identify corrections by chapter and a short quoted phrase, '
                  'since page numbers differ between reading formats.', note),
        Paragraph('Publication metadata and cover artwork are not included in this advance edition.', note),
        Paragraph(f'Manuscript count: {count:,} whitespace-separated tokens, including chapter headings '
                  'and scene markers. Word-processor counts may differ.', note),
        Paragraph(f'Revision: {REVISION}<br/>Source fingerprint: {source_hash[:16]}', note)]
    for number, (title, text) in enumerate(chapters, 1):
        story.append(PageBreak())
        parsed = blocks(text)
        i = 0
        while i < len(parsed):
            kind, content = parsed[i]
            content = (html.escape(content) if kind == 'scene-break' else inline(content)).replace('<strong>', '<b>').replace('</strong>', '</b>')
            content = content.replace('<em>', '<i>').replace('</em>', '</i>')
            if kind == 'heading':
                p = Paragraph(content, head); p.chapter_number = number; story.append(p)
            elif kind == 'system':
                group = [Paragraph(content, system)]
                while i+1 < len(parsed) and parsed[i+1][0] == 'system':
                    i += 1
                    c = inline(parsed[i][1]).replace('<strong>', '<b>').replace('</strong>', '</b>')
                    group.append(Paragraph(c, system))
                story.append(KeepTogether(group))
            else:
                story.append(Paragraph(content, scene if kind == 'scene-break' else first if kind == 'first' else body))
            i += 1
    doc.build(story)
    return {'chapter_starts': starts, 'pages': doc.page, 'sha256': digest(output.read_bytes())}

def build(root: Path, out: Path, pdf: bool = False) -> dict:
    paths = sorted((root / 'book1/chapters').glob('chapter-*.md'))
    expected = [f'chapter-{n:02d}.md' for n in range(1,33)]
    if [p.name for p in paths] != expected:
        raise ValueError('Expected exactly 32 ordered canonical chapter files.')
    texts = [p.read_text(encoding='utf-8') for p in paths]
    compiled = '\n\n'.join(s.strip() for s in texts) + '\n'
    if (root/'book1/WORKING_DRAFT.md').read_text(encoding='utf-8') != compiled:
        raise ValueError('Compiled draft does not match the canonical chapters.')
    out.mkdir(parents=True, exist_ok=True)
    source_hash = digest(compiled.encode('utf-8'))
    count = sum(len(s.split()) for s in texts)
    uid = 'urn:uuid:' + str(uuid.uuid5(uuid.NAMESPACE_URL, TITLE + source_hash))
    data: dict[str,str] = {}
    data['META-INF/container.xml'] = ('<?xml version="1.0"?>'
        '<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">'
        '<rootfiles><rootfile full-path="EPUB/package.opf" media-type="application/oebps-package+xml"/>'
        '</rootfiles></container>')
    data['EPUB/Styles/novel.css'] = CSS
    data['EPUB/Text/title.xhtml'] = xhtml(TITLE,
        f'<section class="title-page" epub:type="titlepage"><h1>{TITLE}</h1>'
        '<p>Book One</p><p class="edition">ADVANCE READER COPY</p>'
        f'<p class="edition">Revision {REVISION}</p>'
        '<p>Please reference chapter numbers when noting corrections.</p></section>', '../Styles/novel.css')
    chapters = []
    navitems, ncxitems, manifest, spine = [], [], [], []
    for n, text in enumerate(texts,1):
        parsed = blocks(text); title = parsed[0][1]; chapters.append((title,text))
        name = f'Text/chapter-{n:02d}.xhtml'; cid=f'chapter-{n:02d}'
        data['EPUB/'+name] = xhtml(title, chapter_body(n,parsed), '../Styles/novel.css')
        navitems.append(f'<li><a href="{name}">{html.escape(title.title())}</a></li>')
        ncxitems.append(f'<navPoint id="{cid}" playOrder="{n}"><navLabel><text>{html.escape(title.title())}'
                        f'</text></navLabel><content src="{name}"/></navPoint>')
        manifest.append(f'<item id="{cid}" href="{name}" media-type="application/xhtml+xml"/>')
        spine.append(f'<itemref idref="{cid}"/>')
    data['EPUB/nav.xhtml'] = xhtml('Contents',
        '<nav epub:type="toc" id="toc"><h1>Contents</h1><ol>'+''.join(navitems)+'</ol></nav>'
        '<nav epub:type="landmarks" hidden="hidden"><h2>Landmarks</h2><ol>'
        '<li><a epub:type="bodymatter" href="Text/chapter-01.xhtml">Begin reading</a></li>'
        '</ol></nav>', 'Styles/novel.css')
    data['EPUB/toc.ncx'] = ('<?xml version="1.0" encoding="utf-8"?>'
        '<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">'
        f'<head><meta name="dtb:uid" content="{uid}"/></head><docTitle><text>{TITLE}</text></docTitle>'
        '<navMap>'+''.join(ncxitems)+'</navMap></ncx>')
    data['EPUB/package.opf'] = ('<?xml version="1.0" encoding="utf-8"?>'
        '<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="book-id" xml:lang="en-US">'
        '<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">'
        f'<dc:identifier id="book-id">{uid}</dc:identifier><dc:title>{TITLE}</dc:title>'
        '<dc:language>en-US</dc:language><dc:description>Book One. Advance Reader Copy.</dc:description>'
        f'<meta property="dcterms:modified">{REVISION}T00:00:00Z</meta></metadata>'
        '<manifest><item id="style" href="Styles/novel.css" media-type="text/css"/>'
        '<item id="title" href="Text/title.xhtml" media-type="application/xhtml+xml"/>'
        '<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>'
        '<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>'
        + ''.join(manifest)+'</manifest><spine toc="ncx"><itemref idref="title"/>'
        + ''.join(spine)+'</spine></package>')
    for name, content in data.items():
        if name.endswith(('.xml','.opf','.ncx','.xhtml')):
            ET.fromstring(content)  # fail before producing an invalid XML package
    epub = out/'The_Unheld_Warder_ARC.epub'
    with zipfile.ZipFile(epub,'w') as z:
        def member(name: str, content: str, compressed: bool = True) -> None:
            info = zipfile.ZipInfo(name, (2026,9,19,0,0,0))
            info.compress_type = zipfile.ZIP_DEFLATED if compressed else zipfile.ZIP_STORED
            info.external_attr = 0o644 << 16
            z.writestr(info, content.encode('utf-8'))
        member('mimetype','application/epub+zip',False)
        for name, content in data.items(): member(name,content)
    result = {'title':TITLE,'revision':REVISION,'source_sha256':source_hash,
        'chapter_count':len(texts),'whitespace_word_count':count,
        'epub_sha256':digest(epub.read_bytes()),
        'chapters':[{'chapter':n,'path':str(p.relative_to(root)),
                     'sha256':digest(p.read_bytes()),'words':len(t.split()),
                     'scene_breaks':sum(k=='scene-break' for k,_ in blocks(t))}
                    for n,(p,t) in enumerate(zip(paths,texts),1)]}
    if pdf:
        result['pdf'] = make_pdf(out/'The_Unheld_Warder_ARC.pdf',chapters,count,source_hash)
    (out/'ARC_BUILD_MANIFEST.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return result

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    parser.add_argument('--output',type=Path)
    parser.add_argument('--pdf',action='store_true')
    args=parser.parse_args()
    result=build(args.root,args.output or args.root/'book1/arc',args.pdf)
    print(json.dumps({k:v for k,v in result.items() if k!='chapters'},ensure_ascii=False,indent=2))
