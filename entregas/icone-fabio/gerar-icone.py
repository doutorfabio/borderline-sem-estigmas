import sys, math, random
from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageEnhance, ImageChops
S=sys.argv[1]
src=Image.open(f'{S}/fabio-recorte.png').convert('RGBA')
N=1600  # final icon canvas
# portrait cut, upscaled
por=src.resize((1300,1300),Image.LANCZOS)
alpha=por.split()[3]
g=ImageOps.grayscale(por.convert('RGB'))
g=ImageOps.autocontrast(g,cutoff=1)
g=ImageEnhance.Contrast(g).enhance(1.35)
g=g.filter(ImageFilter.GaussianBlur(1.2))
# halftone 45deg
step=11
W,H=g.size
ht=Image.new('L',(W,H),255)
d=ImageDraw.Draw(ht)
ang=math.radians(45); ca,sa=math.cos(ang),math.sin(ang)
R=int(max(W,H)*1.5)
for i in range(-R,R,step):
  for j in range(-R,R,step):
    x=W/2+i*ca-j*sa; y=H/2+i*sa+j*ca
    if 0<=x<W and 0<=y<H:
      v=g.getpixel((int(x),int(y)))
      dark=(255-v)/255
      r=step*0.62*math.sqrt(dark)
      if r>0.4: d.ellipse([x-r,y-r,x+r,y+r],fill=0)
paper=(242,234,219)
ink=(22,20,19)
col=Image.new('RGBA',(W,H),paper+(255,))
inkl=Image.new('RGBA',(W,H),ink+(255,))
col=Image.composite(col,inkl,ht)
col.putalpha(alpha.point(lambda a:255 if a>128 else 0))
# cream keyline around cutout
a2=col.split()[3]
kl=a2.filter(ImageFilter.MaxFilter(23))
keyl=Image.new('RGBA',(W,H),(250,245,233,255)); keyl.putalpha(kl)
cut=Image.alpha_composite(keyl,col)
# canvas: red paper circle + cut-out breaking top
N2=N+200
can=Image.new("RGBA",(N,N),(0,0,0,0))
cx,cy,rad=N//2,N//2+190,560
circ=Image.new('RGBA',(N,N),(0,0,0,0)); cd=ImageDraw.Draw(circ)
cd.ellipse([cx-rad-22,cy-rad-22,cx+rad+22,cy+rad+22],fill=(250,245,233,255))
cd.ellipse([cx-rad,cy-rad,cx+rad,cy+rad],fill=(200,38,32,255))
# paper grain on circle
random.seed(3)
gr=Image.effect_noise((N,N),18).convert('L')
grc=Image.merge('RGBA',[gr,gr,gr,circ.split()[3].point(lambda a:int(a*0.10))])
# portrait: below circle bottom cut by circle, above free (pop-out)
px,py=(N-W)//2, 300
layer=Image.new('RGBA',(N,N),(0,0,0,0)); layer.paste(cut,(px,py),cut)
mask_circle=Image.new('L',(N,N),0); ImageDraw.Draw(mask_circle).ellipse([cx-rad-22,cy-rad-22,cx+rad+22,cy+rad+22],fill=255)
upper=Image.new('L',(N,N),0); ImageDraw.Draw(upper).rectangle([0,0,N,cy],fill=255)
keep=ImageChops.lighter(mask_circle,upper)
la=ImageChops.multiply(layer.split()[3],keep); layer.putalpha(la)
# shadow
def shadow(im,off=(14,22),blur=22,op=0.28):
  a=im.split()[3].point(lambda v:int(v*op))
  sh=Image.new('RGBA',im.size,(0,0,0,255)); sh.putalpha(a)
  sh=sh.filter(ImageFilter.GaussianBlur(blur)); out=Image.new('RGBA',im.size,(0,0,0,0)); out.paste(sh,off,sh); return out
can=Image.alpha_composite(can,shadow(circ))
can=Image.alpha_composite(can,circ)
can=Image.alpha_composite(can,grc)
can=Image.alpha_composite(can,shadow(layer,(10,16),16,0.32))
can=Image.alpha_composite(can,layer)
can=can.crop(can.getbbox())
can.save(f'{S}/icone-fabio-2k.png')
bg=Image.new('RGBA',can.size,(46,58,74,255)); Image.alpha_composite(bg,can).convert('RGB').resize((can.width//3,can.height//3)).save(f'{S}/preview.jpg',quality=88)
print(can.size)
