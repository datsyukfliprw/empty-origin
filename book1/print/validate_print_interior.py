#!/usr/bin/env python3
"""Validate all PDF text/pages and generate reproducible proof/contact sheets."""
from __future__ import annotations
import argparse, json, re, unicodedata
from pathlib import Path
import pymupdf as fitz
from PIL import Image, ImageDraw
import build_print_interior as book


def normalized(text):
    # PDF line wrapping may introduce a discretionary hyphen and whitespace.
    return re.sub(r'[\s\-\u00ad]', '', unicodedata.normalize('NFKC', text))


def validate(pdf):
    doc = fitz.open(pdf)
    manifest = json.loads(pdf.with_suffix('.manifest.json').read_text())
    chapters = book.load_chapters()
    errors = []
    check = lambda condition, message: errors.append(message) if not condition else None
    check(book.digest(book.MASTER) == manifest['source_sha256'], 'Master hash changed')
    check(book.digest(pdf) == manifest['pdf_sha256'], 'PDF hash changed')
    check(len(doc) == len(manifest['pages']), 'Manifest page count mismatch')
    check(len(doc) % 2 == 0, 'Odd physical page count')
    check(len(doc.get_toc()) == 32, 'Missing chapter bookmarks')
    texts, positions, used_fonts, font_refs = [], {}, set(), {}
    rendered = []
    low_fill = []
    for page, record in zip(doc, manifest['pages']):
        number = page.number+1
        check(tuple(page.rect) == (0,0,432,648), f'Incorrect trim on page {number}')
        check(not page.get_images(), f'Unexpected raster image on page {number}')
        if record['chapter']:
            n = record['chapter']
            expected_left = book.INSIDE if number % 2 else book.OUTSIDE
            check(bool(record['blocks']), f'Empty story page {number}')
            for entry in record['blocks']:
                key = (n,entry['index'])
                check(key not in positions, f'Duplicate block {key}')
                positions[key] = number
                check(entry['left'] == expected_left, f'Wrong facing margin {number}')
                check(entry['top']+entry['height'] <= book.FLOOR+.01, f'Vertical overflow {key}')
            for a,b in zip(record['blocks'],record['blocks'][1:]):
                check(a['top']+a['height'] <= b['top']+.01, f'Overlapping flowables page {number}')
            if record['opening']:
                check(record['blocks'][0]['index'] == 0, f'Opener detached from prose in chapter {n}')
            elif record['blocks'][-1]['top']+record['blocks'][-1]['height'] < 400:
                low_fill.append(number)
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines',[]):
                for span in line['spans']:
                    used_fonts.add(span['font'])
                    x0,y0,x1,y1=span['bbox']
                    check(x0 >= 0 and y0 >= 0 and x1 <= 432 and y1 <= 648,
                          f'Text outside trim page {number}: {span["text"]}')
                if not record['chapter']:
                    continue
                y0=line['bbox'][1]
                if y0 < (book.OPENING_TOP-6 if record['opening'] else book.TOP-9) or y0 > 605:
                    continue
                for span in line['spans']:
                    texts.append(span['text'])
                    x0,y0,x1,y1=span['bbox']
                    check(x0>=expected_left-2 and x1<=expected_left+book.TEXT_WIDTH+2 and y1<=606,
                          f'Text outside type area page {number}: {span["text"]}')
        for xref,extension,kind,name,*_ in page.get_fonts():
            font_refs[xref]=name
        # Inspect actual ink operators. Color-managed RGB previews of pure CMYK
        # black can look slightly warm; those previews do not imply colored ink.
        stream=page.read_contents().decode('latin1')
        number_pattern=r'([-+]?\d*\.?\d+)'
        for match in re.finditer(r'\s'.join([number_pattern]*4)+r'\s+[kK]\b',stream):
            check(all(float(v)==0 for v in match.groups()[:3]), f'CMY ink on page {number}')
        check(not re.search(r'\s(?:rg|RG|scn|SCN)\b',stream), f'RGB or spot ink on page {number}')
        # Rendering every page also detects damaged streams and missing resources.
        pix=page.get_pixmap(matrix=fitz.Matrix(.5,.5), colorspace=fitz.csRGB, alpha=False)
        rendered.append(Image.frombytes('RGB',[pix.width,pix.height],pix.samples))
    expected=''.join(book.plain(t) for parts in chapters for t in parts if t!='---')
    a,b=normalized(expected),normalized(''.join(texts))
    if a!=b:
        offset=next((i for i,(x,y) in enumerate(zip(a,b)) if x!=y),min(len(a),len(b)))
        errors.append(f'PDF text mismatch at {offset}: expected {a[offset:offset+90]!r}; got {b[offset:offset+90]!r}')
    for n,parts in enumerate(chapters,1):
        for i,t in enumerate(parts):
            check((n,i) in positions, f'Missing chapter {n} block {i}')
            if i+1>=len(parts):continue
            if t=='---':
                check(positions[n,i]==positions[n,i+1], f'Stranded scene ornament {n}:{i}')
            if book.is_system(t) and parts[i+1]!='---':
                check(positions[n,i]==positions[n,i+1], f'Split System/reaction {n}:{i}')
            if t in book.BREAK_AFTER.get(n,set()):
                check(positions[n,i+1]==positions[n,i]+1, f'Missing intentional page turn {n}:{i}')
                if 'HE’S DOWN!' in t:check(positions[n,i]==3, 'Vharos beat must end story page 1')
    embedded=[]
    for xref,name in font_refs.items():
        _,extension,_,data=doc.extract_font(xref)
        check(bool(data) and extension!='n/a', f'Unembedded font {name}')
        embedded.append(name)
    report={'passed':not errors,'errors':errors,'physical_pages':len(doc),
            'story_pages':sum(bool(p['chapter']) for p in manifest['pages']),
            'chapters':32,'source_words':manifest['source_words'],
            'source_sha256':manifest['source_sha256'],'pdf_sha256':book.digest(pdf),
            'text_comparison':'NFKC, excluding whitespace and discretionary/literal hyphens; all other characters compared in order',
            'matching_normalized_characters':len(a) if a==b else None,
            'fonts_embedded':embedded,'all_pages_rendered':True,
            'checks':['trim','mirrored margins','text bounds','flowable overlaps','32 chapter bookmarks',
                      'source and PDF hashes','complete ordered manuscript text','whole paragraphs',
                      'scene ornaments with prose','System blocks and immediate reactions',
                      'Chapter 1 intentional page turns','neutral ink','no raster images','embedded fonts'],
            'sparse_pages_for_visual_review':low_fill,
            'chapter_openers':[{k:p[k] for k in ('chapter','pdf_page','folio')} for p in manifest['pages'] if p['opening']]}
    (book.HERE/'PRINT_VALIDATION.json').write_text(json.dumps(report,indent=2)+'\n')
    if errors:
        print(f'FAIL: {len(errors)} errors; first 20: {errors[:20]}');raise SystemExit(1)
    proof_dir=book.HERE/'proofs';proof_dir.mkdir(exist_ok=True)
    # 48 thumbnails per sheet: structural inspection of every single page.
    for start in range(0,len(rendered),48):
        sheet=Image.new('RGB',(6*228,8*350),'#e9e9e9'); draw=ImageDraw.Draw(sheet)
        for offset,thumb in enumerate(rendered[start:start+48]):
            x=(offset%6)*228+6;y=(offset//6)*350+5
            sheet.paste(thumb,(x,y));draw.text((x,y+325),f'PDF {start+offset+1}',fill='black')
        sheet.save(proof_dir/f'contact-{start//48+1:02d}.jpg',quality=85)
    # A focused packet, not a substitute for the complete PDF.
    selected={0,2,3,4,len(doc)-2}
    for p in manifest['pages']:
        if p['opening'] and p['chapter'] in (9,10,11,12,24,30,32):
            selected.update((p['pdf_page']-1,p['pdf_page']))
    for n,parts in enumerate(chapters,1):
        for i,t in enumerate(parts):
            if t=='My eyes open.':selected.update((positions[n,i]-1,positions[n,i]))
            if '→' in t:selected.add(positions[n,i]-1)
    proof=fitz.open()
    for index in sorted(selected):proof.insert_pdf(doc,from_page=index,to_page=index)
    proof.save(proof_dir/'EMPTY_ORIGIN_LAYOUT_REVIEW.pdf',garbage=4,deflate=True)
    ch1=fitz.open();ch1.insert_pdf(doc,from_page=2,to_page=positions[2,0]-2)
    ch1.save(proof_dir/'EMPTY_ORIGIN_CHAPTER_01_LAYOUT_PROOF.pdf',garbage=4,deflate=True)
    for index,name in [(2,'chapter-01-opener'),(3,'body-page'),(positions[12,0]-1,'chapter-12-opener')]:
        doc[index].get_pixmap(matrix=fitz.Matrix(1.5,1.5)).save(proof_dir/f'{name}.png')
    print(f'PASS: {len(doc)} pages, {len(a):,} matching normalized characters, {len(embedded)} embedded fonts')
    print(f'Review packet: {proof_dir/"EMPTY_ORIGIN_LAYOUT_REVIEW.pdf"}')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('pdf',nargs='?',type=Path,default=book.OUTPUT)
    validate(parser.parse_args().pdf)
