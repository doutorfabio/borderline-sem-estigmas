# Frase vermelha composta em Anton comprimida, com textura de tipo de madeira.
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFont
FONT='fonts/anton-latin-400-normal.ttf'
def word_mask(text, cap_h, xscale):
    """mascara 0..1 da palavra com altura de versal cap_h (px) e compressao horizontal xscale"""
    S=4; f=ImageFont.truetype(FONT, 400)
    bb=f.getbbox('H'); caph=bb[3]-bb[1]
    size=int(400*cap_h*S/caph); f=ImageFont.truetype(FONT,size)
    bb=f.getbbox(text); w=bb[2]-bb[0]; h=bb[3]-bb[1]
    im=Image.new('L',(w+8*S,h+8*S),0); ImageDraw.Draw(im).text((4*S-bb[0],4*S-bb[1]),text,font=f,fill=255)
    a=np.asarray(im).astype(np.float32)/255
    a=cv2.resize(a,(max(1,round(a.shape[1]*xscale/S)),round(a.shape[0]/S)),interpolation=cv2.INTER_AREA)
    return a
def ink(a, seed):
    """borda levemente irregular + falhas de tinta, como no bloco preto"""
    rng=np.random.default_rng(seed); h,w=a.shape
    n1=cv2.GaussianBlur(rng.normal(0,1,(h,w)).astype(np.float32),(0,0),1.6); n1/=n1.std()
    soft=cv2.GaussianBlur(a,(0,0),1.0)
    e=np.clip((soft+0.07*n1-0.42)/0.16,0,1)                       # borda roida
    sp=rng.random((h,w)).astype(np.float32)
    holes=cv2.GaussianBlur((sp>0.9965).astype(np.float32),(0,0),0.7)*3.0   # pontinhos sem tinta
    n2=cv2.GaussianBlur(rng.normal(0,1,(h,w)).astype(np.float32),(0,0),9); n2/=n2.std()
    dens=np.clip(0.96+0.035*n2,0.86,1.0)                          # carga de tinta desigual
    return np.clip(e*dens*(1-np.clip(holes,0,1)),0,1)
if __name__=='__main__':
    a=ink(word_mask('SEGUROU',100,0.8),1); cv2.imwrite('v_red.png',(255-a*255).astype(np.uint8)); print(a.shape)
