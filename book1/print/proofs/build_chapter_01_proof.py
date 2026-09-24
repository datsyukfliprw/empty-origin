#!/usr/bin/env python3
# proof build trigger
import os,re,html,math,random
from pathlib import Path
from PIL import Image,ImageDraw
from reportlab.platypus import *
from reportlab.lib.pagesizes import inch
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY,TA_CENTER,TA_LEFT
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/"book1/print/proofs"
OUT.mkdir(parents=True,exist_ok=True)
RING=OUT/"EMPTY_ORIGIN_APERTURE_RING.png"
PDF=OUT/"EMPTY_ORIGIN_CHAPTER_01_LAYOUT_PROOF.pdf"
CH=ROOT/"book1/chapters/chapter-01.md"

# High-resolution reusable aperture asset, no numeral.
S=1400
im=Image.new("RGBA",(S,S),(255,255,255,0)); d=ImageDraw.Draw(im)
random.seed(101)
cx=cy=S//2
for k in range(8):
    r=440+random.randint(-18,18)
    box=(cx-r,cy-r,cx+r,cy+r)
    start=random.randint(0,25)
    end=360-random.randint(0,25)
    d.arc(box,start,end,fill=(20,18,17,220),width=random.randint(4,11))
for a in range(0,360,15):
    if random.random()<.65:
        th=math.radians(a); r=445+random.randint(-12,12)
        x=cx+math.cos(th)*r; y=cy+math.sin(th)*r
        rr=random.randint(2,8)
        d.ellipse((x-rr,y-rr,x+rr,y+rr),fill=(20,18,17,random.randint(130,235)))
for a in (0,90,180,270):
    th=math.radians(a); r1=420; r2=520
    d.line((cx+math.cos(th)*r1,cy+math.sin(th)*r1,cx+math.cos(th)*r2,cy+math.sin(th)*r2),fill=(20,18,17,235),width=5)
im.save(RING,optimize=True)

# Fonts available on Ubuntu runners.
serif="/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
sans="/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed.ttf"
sansb="/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf"
pdfmetrics.registerFont(TTFont("BookSerif",serif))
pdfmetrics.registerFont(TTFont("BookSans",sans))
pdfmetrics.registerFont(TTFont("BookSansB",sansb))

PAGE=(6*inch,9*inch); cream=colors.HexColor("#F7F3EC"); ink=colors.HexColor("#211E1B")
body=ParagraphStyle("body",fontName="BookSerif",fontSize=10.75,leading=13.5,textColor=ink,alignment=TA_JUSTIFY,firstLineIndent=15)
first=ParagraphStyle("first",parent=body,firstLineIndent=0)
system=ParagraphStyle("system",fontName="BookSansB",fontSize=8.8,leading=11,alignment=TA_CENTER,textColor=ink,spaceBefore=2,spaceAfter=2)
chat=ParagraphStyle("chat",fontName="BookSans",fontSize=9.4,leading=11.5,leftIndent=14,textColor=ink)
meta=ParagraphStyle("meta",fontName="BookSans",fontSize=8.5,leading=11,alignment=TA_CENTER,textColor=colors.HexColor("#4E473F"))
chap=ParagraphStyle("chap",fontName="BookSerif",fontSize=15,leading=18,alignment=TA_CENTER,textColor=ink)

class Opener(Flowable):
    def __init__(self): super().__init__(); self.height=210
    def wrap(self,aw,ah): self.width=aw; return aw,self.height
    def draw(self):
        c=self.canv; cx=self.width/2; w=118
        c.drawImage(str(RING),cx-w/2,92,width=w,height=w,mask="auto")
        c.setFont("BookSerif",30); c.setFillColor(ink); c.drawCentredString(cx,133,"1")
        c.setFont("BookSerif",15); c.drawCentredString(cx,67,"C H A P T E R   O N E")
        c.setFont("BookSans",8.5); c.setFillColor(colors.HexColor("#4E473F"))
        c.drawCentredString(cx,42,"[ LOCATION: EARTH ]"); c.drawCentredString(cx,27,"[ RUN: UNSET ]")

def page(c,doc):
    c.saveState(); c.setFillColor(cream); c.rect(0,0,*PAGE,fill=1,stroke=0)
    c.setFillColor(ink); c.setFont("BookSerif",8.5); c.drawCentredString(PAGE[0]/2,24,str(doc.page)); c.restoreState()

raw=CH.read_text(encoding="utf-8")
parts=[x.strip() for x in re.split(r"\n\s*\n",raw) if x.strip()]
if parts and parts[0].upper().startswith("CHAPTER"): parts=parts[1:]
story=[Opener(),Spacer(1,6)]
i=0; fresh=True
while i<len(parts):
    t=parts[i]
    if t=="---": story += [Spacer(1,8),Paragraph("○",meta),Spacer(1,8)]; fresh=True; i+=1; continue
    if t.startswith("[") and t.endswith("]"):
        unit=[]; j=i
        while j<len(parts) and parts[j].startswith("[") and parts[j].endswith("]"):
            unit.append(Paragraph(html.escape(parts[j]),system)); j+=1
        if j<len(parts) and parts[j]!="---":
            unit.append(Paragraph(html.escape(parts[j]).replace("\n"," "),body)); j+=1
        story.append(KeepTogether(unit)); i=j; fresh=False; continue
    if re.match(r"^[A-Za-z0-9_]+:\s",t):
        story.append(Paragraph(html.escape(t),chat)); fresh=False; i+=1; continue
    story.append(Paragraph(html.escape(t).replace("\n"," "),first if fresh else body)); fresh=False; i+=1

doc=BaseDocTemplate(str(PDF),pagesize=PAGE,leftMargin=.76*inch,rightMargin=.62*inch,topMargin=.54*inch,bottomMargin=.62*inch,title="Empty Origin Chapter 1 Layout Proof",author="Nora Whitcomb")
doc.addPageTemplates(PageTemplate("p",[Frame(doc.leftMargin,doc.bottomMargin,doc.width,doc.height,id="f")],onPage=page))
doc.build(story)
print(PDF)
