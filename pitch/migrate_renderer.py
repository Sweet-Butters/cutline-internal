from pathlib import Path
p=Path(__file__).with_name('build.py');t=p.read_text(encoding='utf-8')
a=t.index('for i,d in enumerate');b=t.index('prs.save(',a)
t=t[:a]+"exec((R/'layouts_v2.py').read_text(encoding='utf-8'))\n"+t[b:]
p.write_text(t,encoding='utf-8')
