#!/usr/bin/env python3\n# Production rebuild after pagination/font preflight
import re, glob, os, html
from reportlab.lib.pagesizes import inch
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak, Flowable, KeepTogether
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

SERIF="/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS="/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed.ttf"
pdfmetrics.registerFont(TTFont("BookSerif",SERIF))
pdfmetrics.registerFont(TTFont("BookSans",SANS))

PAGE=(6*inch,9*inch)
OUT="book1/print/EMPTY_ORIGIN_6x9_PRINT_INTERIOR.pdf"
WORDS=["","ONE","TWO","THREE","FOUR","FIVE","SIX","SEVEN","EIGHT","NINE","TEN","ELEVEN","TWELVE","THIRTEEN","FOURTEEN","FIFTEEN","SIXTEEN","SEVENTEEN","EIGHTEEN","NINETEEN","TWENTY","TWENTY-ONE","TWENTY-TWO","TWENTY-THREE","TWENTY-FOUR","TWENTY-FIVE","TWENTY-SIX","TWENTY-SEVEN","TWENTY-EIGHT","TWENTY-NINE","THIRTY","THIRTY-ONE","THIRTY-TWO"]
LOC={1:"EARTH",2:"WESTERN FOREST",3:"WESTERN FOREST",4:"WESTERN ROAD",5:"GREYWARD",6:"GREYWARD",7:"GREYWARD",8:"GREYWARD",9:"ROAD TO ROOK",10:"ROOK",11:"ROOK",12:"GREYWARD",13:"GREYWARD",14:"GREYWARD",15:"GREYWARD",16:"ROOK",17:"ROOK",18:"ROOK",19:"ROOK",20:"ROOK",21:"ROOK",22:"ROOK",23:"ROOK",24:"EAST RELIEF WORKS",25:"EAST RELIEF WORKS",26:"ROOK",27:"ROOK",28:"ROOK",29:"ROOK",30:"ROOK",31:"ROOK",32:"ROOK"}

class Ring(Flowable):
    def __init__(self,n):
        Flowable.__init__(self); self.n=n; self.width=145; self.height=130; self.hAlign="CENTER"
    def draw(self):
        c=self.canv; cx=72.5; cy=65; r=49
        # layered distressed aperture: deterministic vector approximation of approved reference
        for off,lw,dash in [(0,1.8,None),(-3,.7,[5,3]),(3,.55,[2,4])]:
            c.saveState(); c.setLineWidth(lw)
            if dash: c.setDash(dash)
            c.circle(cx,cy,r+off); c.restoreState()
        # fractures / ink rays
        c.setLineWidth(1.15)
        for x1,y1,x2,y2 in [(72,114,72,126),(72,16,72,4),(23,65,9,65),(122,65,136,65),(106,100,115,109),(39,99,31,108),(39,31,30,22),(106,31,115,22)]:
            c.line(x1,y1,x2,y2)
        # small chips around ring
        c.setLineWidth(.8)
        for x,y in [(17,79),(24,91),(29,111),(43,119),(96,118),(118,104),(129,82),(126,48),(113,25),(91,14),(48,13),(27,30),(14,51)]:
            c.circle(x,y,1.1,stroke=1,fill=0)
        c.setFont("BookSerif",36); s=str(self.n)
        c.drawString(cx-stringWidth(s,"BookSerif",36)/2,cy-12,s)

class SceneMark(Flowable):
    def __init__(self): Flowable.__init__(self); self.width=48; self.height=16; self.hAlign="CENTER"
    def draw(self):
        c=self.canv; c.setLineWidth(.6); c.circle(24,8,3.4); c.line(7,8,19,8); c.line(29,8,41,8)

def footer(canvas,doc):
    p=canvas.getPageNumber()
    if p<=2:return
    canvas.saveState(); canvas.setFont("BookSerif",8.8)
    canvas.drawCentredString(PAGE[0]/2,0.34*inch,str(p-2)); canvas.restoreState()

class BookDoc(BaseDocTemplate):
    def __init__(self,fn):
        BaseDocTemplate.__init__(self,fn,pagesize=PAGE,leftMargin=.72*inch,rightMargin=.58*inch,topMargin=.48*inch,bottomMargin=.62*inch,title="Empty Origin",author="Nora Whitcomb")
        self.addPageTemplates(PageTemplate(id="main",frames=[Frame(self.leftMargin,self.bottomMargin,self.width,self.height,id="body")],onPage=footer))

body=ParagraphStyle("Body",fontName="BookSerif",fontSize=10.6,leading=13.25,alignment=TA_JUSTIFY,firstLineIndent=15,spaceAfter=0,widowOrphanControl=1)
first=ParagraphStyle("First",parent=body,firstLineIndent=0)
system=ParagraphStyle("System",fontName="BookSans",fontSize=8.55,leading=11.2,alignment=TA_CENTER,spaceBefore=3,spaceAfter=3)
chap=ParagraphStyle("Chap",fontName="BookSerif",fontSize=15.2,leading=18,alignment=TA_CENTER,spaceAfter=12)
title=ParagraphStyle("Title",fontName="BookSerif",fontSize=29,leading=34,alignment=TA_CENTER)
author=ParagraphStyle("Author",fontName="BookSerif",fontSize=13,leading=18,alignment=TA_CENTER)
drop=ParagraphStyle("Drop",parent=first)

def esc(s): return html.escape(s)
def clean(s):
    s=s.strip()
    return s[2:-2] if s.startswith("**") and s.endswith("**") else s
def is_system(s):
    t=clean(s); return t.startswith("[") and t.endswith("]")
def run_for(n): return "UNSET" if n<10 else "WARDER"

def dropcap_text(t):
    t=t.replace("\n"," ")
    # only alphabetic starts get the reference-style drop cap
    if t and t[0].isalpha():
        return '<font size="25">'+esc(t[0])+'</font>'+esc(t[1:])
    return esc(t)

def make_prose(t,fresh=False):
    return Paragraph(dropcap_text(t) if fresh else esc(t).replace("\n"," "), drop if fresh else body)

def chapter(path,n):
    txt=open(path,encoding="utf-8").read().replace("\r\n","\n")
    parts=[p.strip() for p in re.split(r"\n\s*\n",txt) if p.strip()]
    if parts and parts[0].upper().startswith("CHAPTER"): parts=parts[1:]

    opener=[Ring(n),Spacer(1,-2),
            Paragraph("C H A P T E R&nbsp;&nbsp;&nbsp;"+WORDS[n],chap),
            Paragraph("[ LOCATION: "+LOC[n]+" ]",system),
            Paragraph("[ RUN: "+run_for(n)+" ]",system),Spacer(1,18)]
    out=[]
    i=0
    # Keep the entire opener with its first prose paragraph.
    if parts:
        first_text=parts[0]
        if first_text!="---" and not is_system(first_text):
            opener.append(make_prose(first_text,True))
            i=1
    out.append(KeepTogether(opener))
    fresh=(i==0)

    while i<len(parts):
        t=parts[i]
        if t=="---":
            unit=[Spacer(1,6),SceneMark(),Spacer(1,6)]
            if i+1<len(parts) and parts[i+1]!="---":
                nxt=parts[i+1]
                if is_system(nxt):
                    # Scene begins with System output: keep the complete System block together.
                    j=i+1; sysunit=[]
                    while j<len(parts) and is_system(parts[j]):
                        sysunit.append(Paragraph(esc(clean(parts[j])),system)); j+=1
                    unit.extend(sysunit)
                    if j<len(parts) and parts[j]!="---":
                        unit.append(make_prose(parts[j],False)); j+=1
                    i=j
                else:
                    unit.append(make_prose(nxt,False)); i+=2
                out.append(KeepTogether(unit)); fresh=False; continue
            out.append(KeepTogether(unit)); i+=1; fresh=True; continue

        if is_system(t):
            # Build one complete System reveal beat. Short prose bridges such as
            # "Then:" or "The line brightens..." stay with the System lines they connect.
            unit=[]; j=i; seen_system=False
            while j<len(parts) and parts[j]!="---":
                cur=parts[j]
                if is_system(cur):
                    unit.append(Paragraph(esc(clean(cur)),system)); seen_system=True; j+=1; continue
                words=len(cur.replace("\n"," ").split())
                # If a short prose bridge is followed by more System output, keep bridging.
                if words<=28 and j+1<len(parts) and is_system(parts[j+1]):
                    unit.append(make_prose(cur,False)); j+=1; continue
                # Keep the immediate reaction after the final System line.
                if seen_system:
                    unit.append(make_prose(cur,False)); j+=1
                break
            out.append(KeepTogether(unit)); i=j; fresh=False; continue

        out.append(make_prose(t,fresh)); fresh=False; i+=1
    return out

