"""Slide layouts executed by build.py with its native PowerPoint primitives."""
for i,d in enumerate(D['slides'],1):
    s=base(d,i);typ=d['layout']
    if typ=='hero':
        txt(s,d['title'],.75,1.2,10,1.4,76,WHITE,True)
        txt(s,d['tagline'],.82,2.85,13,.55,24,GREEN)
        txt(s,d['subtitle'],.78,3.65,14,1.85,43,WHITE,True)
        txt(s,d['team'],.83,6.1,14,.55,22,MUTED)
        txt(s,d['bottom'],.83,7.3,14,.6,23)
        for k,(c,w) in enumerate([(GREEN,2.8),(BLUE,1.7),(AMBER,2.2)]):box(s,11+k*.5,1.55+k*.43,w,.2,c)
    elif typ=='quote':
        txt(s,d['quotes'][0],.85,2.65,14.2,.65,28,WHITE,True)
        box(s,.75,3.65,14.5,2.05)
        txt(s,d['quotes'][1],1.05,3.95,13.9,1.35,30,WHITE,True)
        txt(s,d['goal'],.85,6.5,14.2,.75,26,GREEN,True)
    elif typ in ['cards','market']:
        for j,(title,body) in enumerate(d['cards']):
            x=.75+j*5;box(s,x,2.9,4.5,3.62);box(s,x,2.9,.05,3.62,[GREEN,BLUE,AMBER][j])
            txt(s,title,x+.22,3.16,4.08,.66,25 if typ=='market' else 23,GREEN,True)
            txt(s,body,x+.22,4.15,4.08,2.08,20,MUTED)
        if d.get('bottom'):txt(s,d['bottom'],.8,6.92,14.5,.55,20,GREEN)
    elif typ=='product':
        im=Image.open(R/d['image']);w=10.25;h=w*im.height/im.width
        s.shapes.add_picture(str(R/d['image']),Inches(.72),Inches(2.55),width=Inches(w),height=Inches(h))
        for j,(a,b) in enumerate(d['callouts']):
            y=2.9+j*1.03;txt(s,a,11.3,y,4,.44,21,GREEN,True);txt(s,b,11.3,y+.48,4,.5,16,MUTED)
        # Keep the unaltered sample screenshot clear of source text.
        for sh in s.shapes:
            if sh.name.endswith('_footnote'):sh.left=Inches(11.3);sh.top=Inches(7.13);sh.width=Inches(4);sh.height=Inches(1.15);sh.text_frame.paragraphs[0].font.size=Pt(9)
    elif typ=='loop':
        for j,(a,b) in enumerate(d['steps']):
            x=.75+j*2.45;box(s,x,3.05,2.17,1.75);txt(s,a,x+.13,3.35,1.91,.48,20,GREEN,True);txt(s,b,x+.13,4.05,1.91,.42,16,MUTED)
            if j<5:arrow(s,x+2.21,3.93,.18)
        line(s,14.1,4.91,14.1,5.35,GREEN);line(s,14.1,5.35,1.8,5.35,GREEN);line(s,1.8,5.35,1.8,4.91,GREEN)
        txt(s,'수정 지시로 반복',6.1,5.43,4,.45,18,GREEN)
        txt(s,d['note'],.85,6.14,14.3,1.12,21,WHITE)
    elif typ=='resultsv2':
        for j,(value,label,note) in enumerate(d['metrics']):
            x=.75+j*7.4;box(s,x,2.85,7.05,2.25)
            txt(s,value,x+.25,3.03,6.55,.85,43,GREEN,True)
            txt(s,label,x+.25,4.05,6.55,.43,21,WHITE,True)
            txt(s,note,x+.25,4.61,6.55,.33,15,MUTED,role='label')
        txt(s,d['runtime'],.85,5.48,14.2,.6,27,BLUE,True)
        txt(s,d['finding'],.85,6.35,14.2,.45,21)
        txt(s,d['next'],.85,7.0,14.2,.44,20,GREEN)
    elif typ=='demo':
        for j,(a,b) in enumerate(d['steps']):
            row=j//4;col=j%4;x=.75+col*3.7;y=2.85+row*1.45
            box(s,x,y,3.35,1.15);txt(s,a,x+.18,y+.12,2.99,.35,16,GREEN,True);txt(s,b,x+.18,y+.57,2.99,.4,21,WHITE,True)
        txt(s,d['note'],.85,6.55,14.2,.7,25,GREEN,True)
    elif typ in ['competition','prices']:
        n=len(d['rows']);rh=.82 if typ=='competition' else .78;y0=2.8
        for j,(a,b,c) in enumerate(d['rows']):
            y=y0+j*rh;box(s,.75,y,14.5,rh-.05,GREEN if a=='Cutline' else PANEL)
            col=BG if a=='Cutline' else WHITE
            txt(s,a,.95,y+.14,2.65,rh-.19,18,col,True)
            txt(s,b,3.7,y+.12,5.0,rh-.15,17,col,True)
            txt(s,c,8.95,y+.14,6.03,rh-.19,17,col)
        if d.get('note'):txt(s,d['note'],.85,6.4,14.2,1.0,23,GREEN,True)
    elif typ=='team':
        for j,(name,role,school,history) in enumerate(d['members']):
            x=.75+j*5;box(s,x,2.8,4.5,4.45)
            txt(s,name,x+.25,3.08,4,.6,31,GREEN,True)
            txt(s,role,x+.25,3.9,4,.48,19,WHITE,True)
            txt(s,school,x+.25,4.58,4,.85,17,MUTED)
            txt(s,history,x+.25,5.65,4,1.35,18,WHITE)
    else:raise ValueError('Unknown layout: '+typ)
    chunks=re.split(r'(?m)^## ',(R/'script.md').read_text(encoding='utf-8'))[1:]
    if i<=len(chunks):s.notes_slide.notes_text_frame.text=chunks[i-1]
