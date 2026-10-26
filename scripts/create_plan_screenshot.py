from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
out=Path(__file__).resolve().parents[1]/'docs/query-plan-comparison.png'
W,H=1280,720; bg='#f5f7f4'; ink='#17222b'; muted='#6e7c83'; green='#18764b'; red='#a34343'; mint='#c9f0d7'; line='#dce4df'; white='#fff'
reg='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; bold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; mono='/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'; f=lambda n,b=False,m=False: ImageFont.truetype(mono if m else (bold if b else reg),n)
im=Image.new('RGB',(W,H),bg); d=ImageDraw.Draw(im)
d.rectangle((0,0,W,76),fill=white); d.rectangle((52,24,92,61),fill=ink); d.text((61,31),'IDX',font=f(10,True),fill=white); d.text((112,28),'COMPOSITE INDEX INVESTIGATION',font=f(14,True),fill=ink)
d.text((58,122),'EXPLAIN PLAN COMPARISON',font=f(13,True),fill=green); d.text((58,157),'Column order changes the search path',font=f(39,True),fill=ink); d.text((60,214),'Query: department = Sales AND salary > 50000',font=f(18),fill=muted)
for x,title,idx,plan,color in [(70,'BEFORE · WRONG ORDER','(salary, department)','salary>? only',red),(660,'AFTER · CORRECT ORDER','(department, salary)','department=? AND salary>?',green)]:
 d.rounded_rectangle((x,285,x+550,590),radius=18,fill=white,outline=line,width=2); d.text((x+28,320),title,font=f(16,True),fill=color); d.text((x+28,365),'B-tree index',font=f(14,True),fill=muted); d.text((x+28,397),idx,font=f(24,True),fill=ink); d.line((x+28,445,x+522,445),fill=line,width=2); d.text((x+28,477),'SEARCH employees USING INDEX',font=f(13,True,m=True),fill=muted); d.text((x+28,511),('idx_salary_department' if x<100 else 'idx_department_salary'),font=f(13,True,m=True),fill=ink); d.text((x+28,551),plan,font=f(15,True,m=True),fill=color)
d.text((70,655),'Left-most prefix rule · equality first, range second · writes pay the index storage cost',font=f(15,True),fill=green)
im.save(out)
