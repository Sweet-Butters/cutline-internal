"""python build.py: editable native PPTX, guarded PowerPoint PDF + slide PNGs."""
import json,re,subprocess,sys,time,math
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches,Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent; OUT=R/'out'; OUT.mkdir(exist_ok=True); (OUT/'slides').mkdir(exist_ok=True)
deck=json.loads((R/'deck.json').read_text(encoding='utf-8')); facts=json.loads((R/'facts.json').read_text(encoding='utf-8'))
missing=set()
def resolve(x):
    if isinstance(x,str):
        def sub(m):
            k=m[1]
            if k in facts:
                f=facts[k]
                if f.get('value') is None: missing.add(k); return '측정 중'
                if not f.get('source'): raise ValueError('Every measured fact needs source: '+k)
                return str(f.get('display') or f['value'])
            if k in deck['placeholders']: return deck['placeholders'][k]
            missing.add(k); return '측정 중'
        return re.sub(r'\{\{(\w+)\}\}',sub,x)
    if isinstance(x,list): return [resolve(i) for i in x]
    if isinstance(x,dict): return {k:resolve(v) for k,v in x.items()}
    return x
D=resolve(deck)
FONT=deck.get('font','Malgun Gothic')
BG='10151D'; PANEL='1B2431'; WHITE='F3F6FA'; MUTED='ACB9C9'; GREEN='8FE3BD'; BLUE='7DBBFF'; AMBER='F4BB73'; LINE='354354'
prs=Presentation(); prs.slide_width=Inches(16); prs.slide_height=Inches(9)
regions=[]
def box(s,x,y,w,h,fill=PANEL,line=None,radius=False):
    sh=s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    sh.fill.solid();sh.fill.fore_color.rgb=RGBColor.from_string(fill)
    if line:sh.line.color.rgb=RGBColor.from_string(line)
    else:sh.line.fill.background()
    return sh
def txt(s,text,x,y,w,h,size=22,color=WHITE,bold=False,role='body'):
    sh=s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h));sh.name=f'TEXT_{len(regions)}_{role}'
    tf=sh.text_frame;tf.clear();tf.word_wrap=True
    tf.margin_left=tf.margin_right=0;tf.margin_top=Pt(2);tf.margin_bottom=0
    for n,line in enumerate(text.split('\n')):
        p=tf.paragraphs[0] if n==0 else tf.add_paragraph();p.text=line;p.font.name=FONT;p.font.size=Pt(size);p.font.bold=bold;p.font.color.rgb=RGBColor.from_string(color);p.space_after=Pt(5);p.space_before=Pt(0)
    regions.append(dict(slide=len(prs.slides),name=sh.name,x=x,y=y,w=w,h=h,text=text,role=role,size=size))
    return sh
def line(s,x1,y1,x2,y2,color=LINE,width=1.5):
    sh=s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2));sh.line.color.rgb=RGBColor.from_string(color);sh.line.width=Pt(width)
def arrow(s,x,y,w=.36,color=GREEN):
    line(s,x,y,x+w,y,color,1.5)
    line(s,x+w-.07,y-.055,x+w,y,color,1.5)
    line(s,x+w-.07,y+.055,x+w,y,color,1.5)
def base(d,i):
    s=prs.slides.add_slide(prs.slide_layouts[6]);s.background.fill.solid();s.background.fill.fore_color.rgb=RGBColor.from_string(BG)
    box(s,.55,.52,.09,.22,GREEN);txt(s,d['kicker'],.78,.46,14,.35,12,GREEN,True,'label')
    if d['layout'] not in ['hero','closing']:
        txt(s,d['title'],.7,1.03,14.7,1.3 if '\n' in d['title'] else .75,32,WHITE,True)
        if d.get('subtitle'):txt(s,d['subtitle'],.72,2.45 if '\n' in d['title'] else 1.93,14.4,.65,17,MUTED)
    line(s,.7,8.52,15.3,8.52);txt(s,'CUTLINE  /  AGENT VIDEO WORKSPACE',.7,8.65,10,.22,9,MUTED,role='footer');txt(s,f'{i:02d} / 13',14.2,8.62,1.1,.28,10,MUTED,role='footer')
    if d.get('foot'):txt(s,d['foot'],.72,7.68,14.6,.73,10,MUTED,role='footnote')
    return s
exec((R/'layouts_v2.py').read_text(encoding='utf-8'))
prs.save(OUT/'Cutline_pitch.pptx')
(OUT/'text_regions.json').write_text(json.dumps(regions,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'build_report.json').write_text(json.dumps({'missing_measurements':sorted(missing),'slides':len(prs.slides),'font':FONT},ensure_ascii=False,indent=2),encoding='utf-8')
if '--pptx-only' in sys.argv:sys.exit(0)
# Refuse to connect to ANY existing PowerPoint instance.
running=subprocess.run(['powershell','-NoProfile','-Command',"@(Get-Process POWERPNT -ErrorAction SilentlyContinue).Count"],capture_output=True,text=True,check=True).stdout.strip()
if running!='0':
    raise SystemExit('PowerPoint already running: left untouched. PPTX built; PDF export deferred. Close it yourself and rerun build.py.')
import win32com.client,pythoncom
pythoncom.CoInitialize();app=None;presentation=None;overflow=[]
try:
    app=win32com.client.DispatchEx('PowerPoint.Application')
    presentation=app.Presentations.Open(str(OUT/'Cutline_pitch.pptx'),ReadOnly=True,Untitled=False,WithWindow=False)
    for i in range(1,presentation.Slides.Count+1):
        sl=presentation.Slides(i)
        for sh in sl.Shapes:
            if sh.HasTextFrame and sh.TextFrame.HasText:
                tr=sh.TextFrame2.TextRange
                if tr.BoundHeight>sh.Height+2 or tr.BoundWidth>sh.Width+2:
                    overflow.append({'slide':i,'shape':sh.Name,'text':sh.TextFrame.TextRange.Text,'box':[sh.Width,sh.Height],'bound':[tr.BoundWidth,tr.BoundHeight]})
        sl.Export(str(OUT/'slides'/f'slide-{i:02d}.png'),'PNG',1920,1080)
    # SaveAs(ppSaveAsPDF=32) avoids dynamic COM's optional PrintRange marshaling bug.
    presentation.SaveAs(str(OUT/'Cutline_pitch.pdf'),32)
finally:
    if presentation is not None:presentation.Close()
    if app is not None and app.Presentations.Count==0:app.Quit()
    pythoncom.CoUninitialize()
size=(OUT/'Cutline_pitch.pdf').stat().st_size
report={'slides':len(prs.slides),'pdf_bytes':size,'pdf_under_20MB':size<=20_000_000,'overflow':overflow,'missing_measurements':sorted(missing),'font':FONT}
(OUT/'build_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
for start,end in [(1,7),(8,13)]:
    sheet=Image.new('RGB',(1440,math.ceil((end-start+1)/2)*440),'#29313c');draw=ImageDraw.Draw(sheet)
    for idx,i in enumerate(range(start,end+1)):
        im=Image.open(OUT/'slides'/f'slide-{i:02d}.png');im.thumbnail((700,394));x=(idx%2)*720+10;y=(idx//2)*440+30;sheet.paste(im,(x,y));draw.text((x,y-20),f'Slide {i:02d}',fill='white')
    sheet.save(OUT/f'contact-{start:02d}-{end:02d}.jpg',quality=90)
print(json.dumps(report,ensure_ascii=False,indent=2))
if overflow:sys.exit(2)
if size>20_000_000:sys.exit('PDF exceeds 20 MB')
