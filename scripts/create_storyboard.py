from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
OUT=Path('video_frames'); OUT.mkdir(exist_ok=True)
W,H=1280,720; bg='#f5f7f4'; ink='#17222b'; muted='#6e7c83'; green='#18764b'; red='#a34343'; mint='#c9f0d7'; line='#dce4df'; white='#fff'
reg='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; bold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; mono='/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'; f=lambda n,b=False,m=False: ImageFont.truetype(mono if m else (bold if b else reg),n)
def base(k,t,s=''):
 im=Image.new('RGB',(W,H),bg); d=ImageDraw.Draw(im); d.rectangle((0,0,W,74),fill=white); d.rectangle((52,24,92,61),fill=ink); d.text((61,31),'IDX',font=f(10,True),fill=white); d.text((112,28),'COMPOSITE INDEX INVESTIGATION',font=f(14,True),fill=ink); d.text((58,120),k.upper(),font=f(13,True),fill=green); d.text((58,157),t,font=f(40,True)); d.text((60,216),s,font=f(18),fill=muted); return im,d
def save(im,n): im.save(OUT/f'{n:02d}.png')
im,d=base('Challenge 4','Index order matters','A reporting query, two composite indexes, and the left-most prefix rule.')
d.rounded_rectangle((70,310,1210,585),radius=20,fill=white,outline=line,width=2)
d.text((110,365),'WHERE',font=f(18,True),fill=green); d.text((245,365),'department = Sales',font=f(25,True,m=True),fill=ink); d.text((245,420),'AND salary > 50000',font=f(25,True,m=True),fill=ink); d.text((110,505),'Equality first · range second',font=f(20,True),fill=muted)
save(im,1)
im,d=base('The workload','A multi-filter employee report','The same predicate shape appears for Sales and Engineering departments.')
for y,h,b in [(305,'Sales','department = Sales AND salary > 50000'),(395,'Engineering','department = Engineering AND salary >= 70000'),(485,'Goal','use one composite index for both filters')]:
 d.rounded_rectangle((78,y,1200,y+60),radius=11,fill=white,outline=line,width=2); d.text((105,y+19),h,font=f(15,True),fill=green); d.text((390,y+19),b,font=f(16,m=True),fill=ink)
save(im,2)
im,d=base('Wrong order','The first key does not match the filter','The experiment creates salary first, so the department key is beyond the range boundary.')
d.rounded_rectangle((80,310,1200,560),radius=20,fill=white,outline=line,width=2); d.text((120,360),'idx_salary_department',font=f(24,True,m=True),fill=red); d.text((120,425),'( salary , department )',font=f(32,True,m=True),fill=ink); d.text((120,505),'Plan: salary>? only',font=f(20,True,m=True),fill=red); save(im,3)
im,d=base('Correct order','Match the left-most prefix','Department equality narrows the tree first; salary range scanning happens inside that slice.')
d.rounded_rectangle((80,310,1200,560),radius=20,fill=white,outline=line,width=2); d.text((120,360),'idx_department_salary',font=f(24,True,m=True),fill=green); d.text((120,425),'( department , salary )',font=f(32,True,m=True),fill=ink); d.text((120,505),'Plan: department=? AND salary>?',font=f(20,True,m=True),fill=green); save(im,4)
im,d=base('Evidence','EXPLAIN output makes the difference visible','The verification harness repeats the experiment on 50,000 deterministic rows.')
comp=Image.open('docs/query-plan-comparison.png').convert('RGB'); comp.thumbnail((1040,320)); im.paste(comp,(120,285)); save(im,5)
im,d=base('Delivery','Fast reads, intentional write cost','The corrected index follows the workload, but production plans must still be monitored.')
d.rounded_rectangle((70,320,1210,560),radius=20,fill=ink)
for i,(a,b) in enumerate([('50,000 rows','deterministic experiment data'),('2 plans','wrong order vs corrected order'),('1 rule','left-most prefix governs composite indexes')]):
 y=360+i*58; d.text((110,y),a,font=f(20,True),fill=mint); d.text((600,y),b,font=f(19),fill=white)
d.text((70,640),'Index Order Matters · Challenge 4 · composite index investigation',font=f(15,True),fill=green); save(im,6)
