#!/usr/bin/env python3
import re, glob, os
from reportlab.lib.pagesizes import inch
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak, Flowable
from reportlab.pdfbase.pdfmetrics import stringWidth

PAGE=(6*inch,9*inch)
OUT="book1/print/EMPTY_ORIGIN_6x9_PRINT_INTERIOR.pdf"
WORDS=["","ONE","TWO","THREE","FOUR","FIVE","SIX","SEVEN","EIGHT","NINE","TEN","ELEVEN","TWELVE","THIRTEEN","FOURTEEN","FIFTEEN","SIXTEEN","SEVENTEEN","EIGHTEEN","NINETEEN","TWENTY","TWENTY-ONE","TWENTY-TWO","TWENTY-THREE","TWENTY-FOUR","TWENTY-FIVE","TWENTY-SIX","TWENTY-SEVEN","TWENTY-EIGHT","TWENTY-NINE","THIRTY","THIRTY-ONE","THIRTY-TWO"]

class Ring(Flowable):
    def __init__(self,n): Flowable.__init__(self); self.n=n; self.width=82; self.height=72
    def draw(self):
        c=self.canv; cx=41; cy=38; r=24
        c.setLineWidth(.85); c.circle(cx,cy,r)
        c.setLineWidth(1.2); c.line(cx+15,cy+19,cx+21,cy+24); c.line(cx+20,cy+16,cx+25,cy+18)
        c.setFont("Times-Roman",22); s=str(self.n)
        c.drawString(cx-stringWidth(s,"Times-Roman",22)/2,cy-7,s)

class SceneMark(Flowable):
    def __init__(self): Flowable.__init__(self); self.width=50; self.height=16
    def draw(self):
        c=self.canv; cx=25; cy=8
        c.setLineWidth(.55); c.circle(cx,cy,3.2); c.line(cx-17,cy,cx-5,cy); c.line(cx+5,cy,cx+17,cy)

def footer(canvas,doc):
    p=canvas.getPageNumber()
    if p<=2:return
    canvas.saveState(); canvas.setFont("Times-Roman",9)
    canvas.drawCentredString(PAGE[0]/2,0.43*inch,str(p-2)); canvas.restoreState()

class BookDoc(BaseDocTemplate):
    def __init__(self,fn):
        BaseDocTemplate.__init__(self,fn,pagesize=PAGE,leftMargin=.72*inch,rightMargin=.58*inch,topMargin=.66*inch,bottomMargin=.68*inch,title="Empty Origin",author="Nora Whitcomb")
        f=Frame(self.leftMargin,self.bottomMargin,self.width,self.height,id="body")
        self.addPageTemplates(PageTemplate(id="main",frames=[f],onPage=footer))

body=ParagraphStyle("Body",fontName="Times-Roman",fontSize=10.75,leading=13.35,alignment=TA_JUSTIFY,firstLineIndent=15,spaceAfter=0,widowOrphanControl=1)
first=ParagraphStyle("First",parent=body,firstLineIndent=0)
system=ParagraphStyle("System",fontName="Helvetica",fontSize=9.15,leading=12,alignment=TA_CENTER,spaceBefore=4,spaceAfter=4)
chat=ParagraphStyle("Chat",fontName="Helvetica",fontSize=9.4,leading=12.1,alignment=TA_LEFT,leftIndent=12,rightIndent=8,spaceBefore=1,spaceAfter=1)
chap=ParagraphStyle("Chap",fontName="Times-Roman",fontSize=15.5,leading=18,alignment=TA_CENTER,spaceAfter=19)
title=ParagraphStyle("Title",fontName="Times-Roman",fontSize=29,leading=34,alignment=TA_CENTER)
author=ParagraphStyle("Author",fontName="Times-Roman",fontSize=13,leading=18,alignment=TA_CENTER)

def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
def clean(s):
    s=s.strip()
    return s[2:-2] if s.startswith("**") and s.endswith("**") else s
def is_system(s):
    t=clean(s); return t.startswith("[") and t.endswith("]")
def is_chat(s): return bool(re.match(r"^[A-Za-z0-9_]+:\s",s.strip()))

def chapter(path,n):
    txt=open(path,encoding="utf-8").read().replace("\r\n","\n")
    parts=re.split(r"\n\s*\n",txt)
    if parts and parts[0].strip().upper().startswith("CHAPTER"): parts=parts[1:]
    out=[Spacer(1,7),Ring(n),Spacer(1,1),Paragraph(" ".join(list("CHAPTER "+WORDS[n])),chap),Spacer(1,3)]
    fresh=True
    for raw in parts:
        t=raw.strip()
        if not t: continue
        if t=="---":
            out += [Spacer(1,7),SceneMark(),Spacer(1,7)]; fresh=True; continue
        if is_system(t): out.append(Paragraph(esc(clean(t)),system)); fresh=False; continue
        if is_chat(t): out.append(Paragraph(esc(t),chat)); fresh=False; continue
        out.append(Paragraph(esc(t).replace("\n"," "),first if fresh else body)); fresh=False
    return out

os.makedirs(os.path.dirname(OUT),exist_ok=True)
story=[Spacer(1,2.15*inch),Paragraph("EMPTY ORIGIN",title),Spacer(1,.26*inch),Paragraph("NORA WHITCOMB",author),PageBreak(),PageBreak()]
files=sorted(glob.glob("book1/chapters/chapter-*.md"))
if len(files)!=32: raise SystemExit(f"Expected 32 chapters, found {len(files)}")
for i,p in enumerate(files,1):
    if i>1: story.append(PageBreak())
    story.extend(chapter(p,i))
BookDoc(OUT).build(story)
print(OUT)
