# Run from Scribus: Script -> Execute Script
import os
try:
    import scribus
except ImportError:
    print('Run this script from inside Scribus.')
    raise

HERE=os.path.dirname(os.path.abspath(__file__))
ROOT=os.path.dirname(HERE)
RING=os.path.join(ROOT,'assets','aperture_ring.svg')
CH1=os.path.normpath(os.path.join(ROOT,'..','..','chapters','chapter-01.md'))
OUT=os.path.join(ROOT,'EMPTY_ORIGIN_MASTER_GENERATED.sla')
W,H=432.0,648.0
MARGINS=(54.72,44.64,38.88,44.64)

scribus.newDocument((W,H),MARGINS,scribus.PORTRAIT,1,scribus.UNIT_POINTS,scribus.PAGE_2,1,12)

for name,rgb in [('EO Ink',(33,29,26)),('EO Meta',(81,74,67)),('EO System',(75,70,65)),('EO Chat',(102,94,86))]:
    try: scribus.defineColorRGB(name,*rgb)
    except Exception: pass

styles=[
 ('EO Body Char','EB Garamond',11.35,'EO Ink',0),
 ('EO System Char','Noto Sans Condensed',9.15,'EO System',0),
 ('EO Chat Char','Noto Sans Condensed',9.35,'EO Chat',0),
 ('EO Label Char','Noto Sans Condensed Medium',9.6,'EO Meta',0),
 ('EO Chapter Char','EB Garamond',15.0,'EO Ink',120),
 ('EO Meta Char','Noto Sans Condensed',9.15,'EO Meta',60),
 ('EO Page Char','Noto Serif',9.6,'EO Ink',0)]
for name,font,size,color,tracking in styles:
    try: scribus.createCharStyle(name=name,font=font,fontsize=size,fillcolor=color,tracking=tracking,language='en_US')
    except Exception: pass

pstyles=[
 dict(name='EO Body',linespacingmode=0,linespacing=13.55,alignment=3,firstindent=14.5,charstyle='EO Body Char'),
 dict(name='EO Body First',linespacingmode=0,linespacing=13.55,alignment=3,firstindent=0,charstyle='EO Body Char'),
 dict(name='EO Continuation',linespacingmode=0,linespacing=13.55,alignment=3,firstindent=0,charstyle='EO Body Char'),
 dict(name='EO System',linespacingmode=0,linespacing=10.9,alignment=1,firstindent=0,charstyle='EO System Char'),
 dict(name='EO Chat',linespacingmode=0,linespacing=11.2,alignment=0,leftmargin=18,firstindent=0,charstyle='EO Chat Char'),
 dict(name='EO Label',linespacingmode=0,linespacing=11.5,alignment=0,leftmargin=14.5,firstindent=0,charstyle='EO Label Char'),
 dict(name='EO Chapter Title',linespacingmode=0,linespacing=18,alignment=1,firstindent=0,charstyle='EO Chapter Char'),
 dict(name='EO Metadata',linespacingmode=0,linespacing=11,alignment=1,firstindent=0,charstyle='EO Meta Char'),
 dict(name='EO Page Number',linespacingmode=0,linespacing=11,alignment=1,firstindent=0,charstyle='EO Page Char')]
for kw in pstyles:
    try: scribus.createParagraphStyle(**kw)
    except Exception: pass

def tf(x,y,w,h,name,text='',style=None):
    f=scribus.createText(x,y,w,h,name)
    scribus.setLineColor('None',f); scribus.setFillColor('None',f)
    if text: scribus.setText(text,f)
    if style:
        try: scribus.setStyle(style,f)
        except Exception: pass
    return f

body=[]
for p in range(1,13):
    scribus.gotoPage(p)
    if p==1:
        img=scribus.createImage(151.9,40,128.2,128.2,'EO_RING')
        scribus.loadImage(RING,img); scribus.setScaleImageToFrame(True,True,img)
        tf(176,91,80,45,'EO_CHAPTER_NUM','1','EO Page Number')
        try: scribus.setFontSize(29.5,'EO_CHAPTER_NUM')
        except Exception: pass
        tf(70,171,292,28,'EO_CHAPTER_TITLE','C H A P T E R   O N E','EO Chapter Title')
        tf(100,205,232,20,'EO_META_LOCATION','[ LOCATION: EARTH ]','EO Metadata')
        tf(100,225,232,20,'EO_META_RUN','[ RUN: UNSET ]','EO Metadata')
        bf=tf(54.72,270,332.64,326,'EO_BODY_P01','','EO Body')
    else:
        bf=tf(54.72,38.88,332.64,557,'EO_BODY_P%02d'%p,'','EO Body')
    body.append(bf)
    tf(190,610,52,18,'EO_PAGE_NUM_%02d'%p,str(p),'EO Page Number')

for a,b in zip(body,body[1:]):
    try: scribus.linkTextFrames(a,b)
    except Exception: pass

try:
    text=open(CH1,encoding='utf-8').read()
    if text.startswith('CHAPTER ONE'): text=text.split('\n',2)[-1]
    scribus.setText(text,body[0]); scribus.setStyle('EO Body',body[0])
except Exception as e:
    print('Could not load Chapter 1:',e)

scribus.saveDocAs(OUT)
scribus.docChanged(True)
print('Created:',OUT)
