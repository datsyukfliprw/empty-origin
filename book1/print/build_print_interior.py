#!/usr/bin/env python3
"""Build the frozen book with the Scribus kit typography, without GUI or network.
Whole paragraphs are pagination units: sentences never cross page turns.
"""
from __future__ import annotations
import argparse, hashlib, html, json, re
from dataclasses import dataclass
from pathlib import Path
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import Paragraph
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MASTER = ROOT / 'book1/frozen/EMPTY_ORIGIN_BETA_ARC_MASTER_2026-09-20.md'
OUTPUT = HERE / 'EMPTY_ORIGIN_6x9_PRINT_INTERIOR.pdf'
RING = HERE / 'EMPTY_ORIGIN_SCRIBUS_MASTER_KIT/assets/aperture_ring.svg'
FONTS = HERE / 'assets/fonts'
WIDTH, HEIGHT = 432., 648.
INSIDE, OUTSIDE, TOP, BOTTOM = 54.72, 44.64, 38.88, 44.64
TEXT_WIDTH = WIDTH - INSIDE - OUTSIDE
FLOOR = HEIGHT - BOTTOM
OPENING_TOP = 270.
WORDS = ('ONE TWO THREE FOUR FIVE SIX SEVEN EIGHT NINE TEN ELEVEN TWELVE '
         'THIRTEEN FOURTEEN FIFTEEN SIXTEEN SEVENTEEN EIGHTEEN NINETEEN TWENTY '
         'TWENTY-ONE TWENTY-TWO TWENTY-THREE TWENTY-FOUR TWENTY-FIVE '
         'TWENTY-SIX TWENTY-SEVEN TWENTY-EIGHT TWENTY-NINE THIRTY '
         'THIRTY-ONE THIRTY-TWO').split()
# Dominant setting, checked against chapter text and CHAPTER_LEDGER.md.
LOCATIONS = {1: 'EARTH', 2: 'WESTERN FOREST', 3: 'WESTERN FOREST',
             4: 'WESTERN ROAD', **{n: 'GREYWARD' for n in range(5, 10)},
             10: 'ROAD TO ROOK', **{n: 'ROOK' for n in range(11, 33)},
             24: 'EAST RELIEF WORKS', 25: 'EAST RELIEF WORKS'}
BREAK_AFTER = {1: {'“HE’S DOWN! HE’S FUCKING DOWN!”', 'My eyes open.'}}
CHAT = re.compile(r'^(?:Derek|pixelwitch|BoredAtWork88|ManaAddict):\s')

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def plain(text):
    return text.replace('**', '').replace('*', '')

def inline(text):
    text = html.escape(' '.join(text.splitlines()), quote=False)
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    return re.sub(r'(?<!\*)\*([^*]+?)\*(?!\*)', r'<i>\1</i>', text)

def is_system(text):
    t = plain(text).strip()
    return ((t.startswith('[') and t.endswith(']')) or
            bool(re.fullmatch(r'\*\*[\d /→]+\*\*', text)))

def load_chapters():
    raw = MASTER.read_text(encoding='utf-8')
    chunks = re.split(r'(?m)^CHAPTER ([A-Z -]+)\n', raw)
    if chunks[0].strip() or len(chunks) != 65:
        raise ValueError('Expected exactly 32 chapters in frozen master')
    chapters = []
    for n in range(1, 33):
        heading, text = chunks[2*n-1:2*n+1]
        if heading != WORDS[n-1]:
            raise ValueError(f'Unexpected chapter heading: {heading}')
        chapters.append([p.strip() for p in re.split(r'\n\s*\n', text) if p.strip()])
    current = '\n\n'.join(p.read_text().strip() for p in
                           sorted((ROOT/'book1/chapters').glob('chapter-*.md')))
    if raw.split() != current.split():
        raise ValueError('Active chapters differ from frozen master; select a new approved master explicitly')
    return chapters

def setup_fonts():
    names = {'Body': 'EBGaramond-Regular.ttf', 'BodyItalic': 'EBGaramond-Italic.ttf',
             'BodyBold': 'EBGaramond-Bold.ttf', 'BodyBoldItalic': 'EBGaramond-BoldItalic.ttf',
             'System': 'NotoSansCondensed-Regular.ttf', 'SystemMedium': 'NotoSansCondensed-Medium.ttf',
             'Numeral': 'NotoSerif-Regular.ttf'}
    for name, filename in names.items():
        pdfmetrics.registerFont(TTFont(name, str(FONTS/filename)))
    pdfmetrics.registerFontFamily('Body', normal='Body', italic='BodyItalic',
                                  bold='BodyBold', boldItalic='BodyBoldItalic')
    pdfmetrics.registerFontFamily('System', normal='System', bold='SystemMedium',
                                  italic='System', boldItalic='SystemMedium')
    return names

def styles():
    body = ParagraphStyle('Body', fontName='Body', fontSize=11.35, leading=13.55,
                          alignment=TA_JUSTIFY, firstLineIndent=14.5,
                          textColor=colors.CMYKColor(0, 0, 0, 1),
                          allowWidows=0, allowOrphans=0, hyphenationLang='en_US',
                          embeddedHyphenation=1, splitLongWords=0)
    return {
        'body': body,
        'first': ParagraphStyle('First', parent=body, firstLineIndent=0),
        'opening': ParagraphStyle('Opening', parent=body, firstLineIndent=0, autoLeading='max'),
        'system': ParagraphStyle('System', parent=body, fontName='System', fontSize=9.15,
                                leading=10.9, firstLineIndent=0, alignment=TA_CENTER,
                                hyphenationLang=None),
        'chat': ParagraphStyle('Chat', parent=body, fontName='System', fontSize=9.35,
                              leading=11.2, firstLineIndent=0, leftIndent=18,
                              alignment=TA_LEFT, hyphenationLang=None),
    }

@dataclass
class Block:
    chapter: int
    index: int
    text: str
    kind: str
    paragraph: Paragraph | None
    height: float
    before: float = 0
    after: float = 0
    @property
    def extent(self):
        return self.before + self.height + self.after

def make_blocks(n, parts, sty):
    result, fresh = [], True
    for index, text in enumerate(parts):
        if text == '---':
            result.append(Block(n, index, text, 'scene', None, 12, 7, 7))
            fresh = True
            continue
        kind = 'system' if is_system(text) else 'chat' if CHAT.match(text) else 'body'
        before, after = (3, 3) if kind == 'system' else (0, 0)
        content = inline(plain(text) if kind == 'system' else text)
        if kind != 'system':
            content = re.sub(r'(\[[^\[\]]+\])', r'<font name="System" size="9.15">\1</font>', content)
        if kind == 'system':
            content = content.replace('→', '<font name="Body">→</font>')
        if kind == 'body' and fresh:
            kind = 'opening' if index == 0 else 'first'
            if kind == 'opening':
                # Raised initial matching the sample, with a small opening quote.
                content = re.sub(r'^([“‘\"\s]*)([A-Za-z])',
                                 r'\1<font size="31">\2</font>', content, count=1)
        paragraph = Paragraph(content, sty[kind])
        _, height = paragraph.wrap(TEXT_WIDTH, HEIGHT)
        if height > FLOOR-TOP:
            raise ValueError(f'Chapter {n} block {index} exceeds one page')
        result.append(Block(n, index, text, kind, paragraph, height, before, after))
        fresh = False
    return result

def units(blocks):
    """Group scene starts, reveals/reactions and chat without locking whole scenes."""
    result, i = [], 0
    while i < len(blocks):
        group = []
        if blocks[i].kind == 'scene':
            group.append(blocks[i]); i += 1
        if i >= len(blocks):
            raise ValueError('Scene ornament has no following paragraph')
        if blocks[i].kind == 'system':
            # Short prose bridges are part of a multi-stage System reveal.
            while i < len(blocks):
                while i < len(blocks) and blocks[i].kind == 'system':
                    group.append(blocks[i]); i += 1
                j, bridge_words = i, 0
                while j < len(blocks) and blocks[j].kind not in ('system', 'scene', 'chat') and j-i < 6:
                    words = len(plain(blocks[j].text).split())
                    if words > 32 or bridge_words+words > 70:
                        break
                    bridge_words += words; j += 1
                if (j > i and j < len(blocks) and blocks[j].kind == 'system'
                        and sum(b.extent for b in group+blocks[i:j+1]) < 350):
                    group.extend(blocks[i:j]); i = j
                else:
                    break
            if i < len(blocks) and blocks[i].kind != 'scene':
                group.append(blocks[i]); i += 1
        elif blocks[i].kind == 'chat':
            while i < len(blocks) and blocks[i].kind == 'chat':
                group.append(blocks[i]); i += 1
        else:
            group.append(blocks[i]); i += 1
        if (i < len(blocks) and blocks[i].kind not in ('scene', 'system', 'chat')
                and group[-1].text not in BREAK_AFTER.get(group[-1].chapter, set())
                and len(plain(group[-1].text).split()) <= 8
                and sum(b.extent for b in group) + blocks[i].extent <= 180):
            group.append(blocks[i]); i += 1
        if sum(b.extent for b in group) > FLOOR-TOP:
            raise ValueError('Narrative unit exceeds a full page')
        result.append(group)
    # Do not strand a short lead-in before its notification or dramatic payoff.
    # Dialogue-heavy scenes remain free to paginate; joins are deliberately bounded.
    merged = []
    for group in result:
        if merged:
            previous = merged[-1]
            tail = plain(previous[-1].text)
            setup = ((len(tail.split()) <= 12 and not tail.startswith('“'))
                     or tail.endswith('?”')
                     or (group[0].kind == 'system' and len(tail.split()) <= 32))
            if (setup and group[0].kind != 'scene'
                    and previous[-1].text not in BREAK_AFTER.get(previous[-1].chapter, set())
                    and sum(b.extent for b in previous+group) <= 240):
                previous.extend(group)
                continue
        merged.append(group)
    return merged

def tracked(c, text, cx, baseline, font, size, tracking):
    c.saveState()
    width = pdfmetrics.stringWidth(text, font, size) + tracking*(len(text)-1)
    if width > TEXT_WIDTH:
        tracking = max(0, (TEXT_WIDTH-pdfmetrics.stringWidth(text, font, size))/(len(text)-1))
        width = pdfmetrics.stringWidth(text, font, size) + tracking*(len(text)-1)
    obj = c.beginText(cx-width/2, baseline)
    obj.setFont(font, size); obj.setCharSpace(tracking); obj.textOut(text)
    c.drawText(obj)
    c.restoreState()

class Interior:
    def __init__(self, output):
        self.canvas = Canvas(str(output), pagesize=(WIDTH, HEIGHT),
                             pageCompression=1, invariant=1, enforceColorSpace='SEP_BLACK',
                             initialFontName='Body')
        self.canvas.setTitle('Empty Origin')
        self.canvas.setAuthor('Nora Whitcomb')
        self.canvas.setSubject('6 × 9 inch interior — frozen September 20, 2026 master')
        self.ring = svg2rlg(str(RING))
        self.ring.initialFontName = 'Body'
        self.pages, self.active, self.y = [], False, TOP

    def ring_at(self, cx, top, size):
        c = self.canvas
        c.saveState()
        c.translate(cx-size/2, HEIGHT-top-size)
        c.scale(size/self.ring.width, size/self.ring.height)
        renderPDF.draw(self.ring, c, 0, 0)
        c.restoreState()

    def new_page(self, chapter=None, opening=False, front=None):
        if self.active:
            self.canvas.showPage()
        self.active = True
        number = len(self.pages)+1
        self.page = {'pdf_page': number, 'folio': number-2 if chapter else None,
                     'chapter': chapter, 'opening': opening, 'front': front,
                     'blocks': [], 'units': []}
        self.pages.append(self.page)
        self.left = INSIDE if number % 2 else OUTSIDE
        self.y = OPENING_TOP if opening else TOP
        c = self.canvas
        c.setFillColor(colors.CMYKColor(0, 0, 0, 1))
        c.setStrokeColor(colors.CMYKColor(0, 0, 0, 1))
        if chapter:
            c.setFont('Numeral', 9.6)
            c.drawCentredString(WIDTH/2, .39*72, str(number-2))
        if opening:
            center = self.left+TEXT_WIDTH/2
            c.bookmarkPage(f'chapter-{chapter}')
            c.addOutlineEntry(f'Chapter {WORDS[chapter-1].title()}', f'chapter-{chapter}', 0)
            self.ring_at(center, 40, 128.16)
            c.setFont('Numeral', 30)
            c.drawCentredString(center, HEIGHT-115, str(chapter))
            tracked(c, 'CHAPTER '+WORDS[chapter-1], center, HEIGHT-190, 'Body', 15, 2.6)
            tracked(c, '[ LOCATION: '+LOCATIONS[chapter]+' ]', center, HEIGHT-222, 'System', 9.15, .7)
            run = 'UNSET' if chapter <= 10 else 'WARDER'
            tracked(c, '[ RUN: '+run+' ]', center, HEIGHT-241, 'System', 9.15, .7)

    def draw_group(self, group):
        self.page['units'].append([b.index for b in group])
        for b in group:
            self.y += b.before
            if b.kind == 'scene':
                self.ring_at(self.left+TEXT_WIDTH/2, self.y, 12)
            else:
                b.paragraph.drawOn(self.canvas, self.left, HEIGHT-self.y-b.height)
            self.page['blocks'].append({'index': b.index, 'kind': b.kind,
                                        'top': round(self.y, 3), 'height': round(b.height, 3),
                                        'left': self.left})
            self.y += b.height + b.after

    def build(self, chapters, sty):
        self.new_page(front='title')
        c = self.canvas
        self.ring_at(WIDTH/2, 150, 78)
        tracked(c, 'EMPTY ORIGIN', WIDTH/2, 350, 'Body', 29, 1.5)
        tracked(c, 'NORA WHITCOMB', WIDTH/2, 307, 'Body', 13, 1.4)
        self.new_page(front='blank verso')
        for n, parts in enumerate(chapters, 1):
            self.new_page(n, opening=True)
            groups = units(make_blocks(n, parts, sty))
            break_next = False
            for group in groups:
                extent = sum(b.extent for b in group)
                if break_next or self.y+extent > FLOOR+.001:
                    if not self.page['blocks']:
                        raise ValueError(f'Chapter {n}: opener and first narrative unit do not fit')
                    self.new_page(n)
                self.draw_group(group)
                break_next = group[-1].text in BREAK_AFTER.get(n, set())
            if self.page['blocks'][-1]['index'] != len(parts)-1:
                raise ValueError('Missing chapter ending')
        if len(self.pages) % 2:
            self.new_page(front='blank end verso')
        self.canvas.save()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=OUTPUT)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    chapters = load_chapters()
    names = setup_fonts()
    book = Interior(args.output)
    book.build(chapters, styles())
    manifest = {'source': str(MASTER.relative_to(ROOT)), 'source_sha256': digest(MASTER),
                'source_words': len(MASTER.read_text().split()), 'chapters': 32,
                'pdf': args.output.name, 'pdf_sha256': digest(args.output),
                'trim_points': [WIDTH, HEIGHT],
                'fonts': {filename: digest(FONTS/filename) for filename in names.values()},
                'ring_sha256': digest(RING), 'pages': book.pages}
    args.output.with_suffix('.manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    print(f'{args.output}: {len(book.pages)} pages; {len(chapters)} chapters')

if __name__ == '__main__':
    main()
