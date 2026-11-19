"""Check final deliverables, numeric provenance and slide geometry."""
from pathlib import Path
import json,re,zipfile
from pptx import Presentation
import pymupdf
R=Path(__file__).resolve().parent
p=Presentation(R/'out/Cutline_pitch.pptx');doc=pymupdf.open(R/'out/Cutline_pitch.pdf')
texts=['\n'.join(sh.text for sh in s.shapes if sh.has_text_frame) for s in p.slides]
assert len(p.slides)==len(doc)==13
assert (R/'out/Cutline_pitch.pdf').stat().st_size <= 20_000_000
assert len(list((R/'out/slides').glob('slide-*.png')))==13
assert all('Cutline' in doc[i].get_text() or 'CUTLINE' in doc[i].get_text() for i in range(13))
assert all(not re.search(r'\{\{\w+\}\}',t) for t in texts)
for word in ['강의감','ChannelGam','왕중왕전','54분','26.8%','64/64','41~57%','2h→20m','5,680','19,900','49,000','99,000','HACK:ON','강의 B2B','0.12 → 0.07']:
    assert not any(word in t for t in texts),word
for i,t in enumerate(texts,1):
    if '채널감' in t:
        assert i in (1,13) and 'Team 채널감' in t
assert len(re.findall(r'^## ',(R/'QA.md').read_text(encoding='utf-8'),re.M))==10
assert len(re.findall(r'^## ',(R/'script.md').read_text(encoding='utf-8'),re.M))==13
overlaps=[];offslide=[];small=[]
for i,s in enumerate(p.slides,1):
    shapes=[sh for sh in s.shapes if sh.has_text_frame and sh.text and sh.name.startswith('TEXT_')]
    for a in shapes:
        if a.left<0 or a.top<0 or a.left+a.width>p.slide_width or a.top+a.height>p.slide_height:offslide.append([i,a.name])
        if a.name.endswith('_body'):
            for para in a.text_frame.paragraphs:
                if para.font.size and para.font.size.pt<16:small.append([i,a.name,para.font.size.pt])
    for j,a in enumerate(shapes):
        for b in shapes[j+1:]:
            dx=min(a.left+a.width,b.left+b.width)-max(a.left,b.left)
            dy=min(a.top+a.height,b.top+b.height)-max(a.top,b.top)
            if dx>9144 and dy>9144:overlaps.append([i,a.name,b.name,round(dx/914400,3),round(dy/914400,3)])
report=json.loads((R/'out/build_report.json').read_text(encoding='utf-8'))
out={'slides':13,'pdf_pages':len(doc),'pngs':13,'pdf_bytes':report['pdf_bytes'],'powerpoint_text_overflow':report['overflow'],'textbox_overlap':overlaps,'offslide':offslide,'body_below_16pt':small,'editable_text_shapes':sum(len([sh for sh in s.shapes if sh.has_text_frame and sh.text]) for s in p.slides),'notes_present':all(s.has_notes_slide for s in p.slides),'separation_check':'passed','pdf_text_extraction':'passed'}
(R/'out/audit.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(out,ensure_ascii=True,indent=2))
assert not report['overflow'] and not overlaps and not offslide and not small
