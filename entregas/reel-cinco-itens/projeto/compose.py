import subprocess, numpy as np, cv2, sys
W,H,FPS=1080,1920,24
N1,N=576,1193
def reader(src, skip, count):
    cmd=['ffmpeg','-v','error','-i',src,'-vf','fps=24,scale=in_color_matrix=bt709:in_range=tv:out_range=pc,format=rgb24','-f','rawvideo','-pix_fmt','rgb24','-']
    p=subprocess.Popen(cmd,stdout=subprocess.PIPE,bufsize=W*H*3*4)
    i=0; got=0
    while got<count:
        b=p.stdout.read(W*H*3)
        if len(b)<W*H*3: break
        if i>=skip: yield np.frombuffer(b,np.uint8).reshape(H,W,3); got+=1
        i+=1
    p.kill()
# zoom keyframes: (start, end, z0, z1)
SEG=[(0,3.75,1.00,1.05),(3.75,6.125,1.06,1.09),(6.125,9.167,1.12,1.15),(9.167,11.083,1.02,1.05),(11.083,13.583,1.08,1.12),
     (13.583,16.875,1.04,1.04),(16.875,18.75,1.03,1.06),(18.75,20.0,1.09,1.11),(20.0,24.042,1.06,1.06),(24.042,28.458,1.05,1.09),
     (28.458,29.667,1.10,1.13),(29.667,33.167,1.02,1.06),(33.167,36.167,1.13,1.16),(36.167,39.50,1.05,1.05),(39.50,41.333,1.06,1.09),
     (41.333,45.042,1.04,1.04),(45.042,47.292,1.03,1.06),(47.292,50.0,1.11,1.14)]
def zoom(t):
    for a,b,z0,z1 in SEG:
        if a<=t<b: p=(t-a)/(b-a); return z0+(z1-z0)*p
    return 1.0
AX,AY=560,700
WX,WY,WW,WH=173,614,734,1306          # opening window (footage at 68%), bottom edge flush with the frame
_m=np.zeros((WH*4,WW*4),np.uint8); cv2.rectangle(_m,(0,34*4),(WW*4,WH*4),255,-1); cv2.rectangle(_m,(34*4,0),(WW*4-34*4,WH*4),255,-1)
cv2.circle(_m,(34*4,34*4),34*4,255,-1); cv2.circle(_m,(WW*4-34*4,34*4),34*4,255,-1)
WMASK=(cv2.resize(_m,(WW,WH),interpolation=cv2.INTER_AREA).astype(np.float32)/255.0)[...,None]
T_OPEN=3.75
def _lut(g):
    x=np.arange(256)/255.0*g
    y=np.where(x>0.75, 0.75+0.25*np.tanh((x-0.75)/0.25), x)
    return np.clip(y*255+0.5,0,255).astype(np.uint8)
LUT=[_lut(1.14*0.985),_lut(1.14),_lut(1.14*1.008)]   # light exposure lift with soft shoulder, a hair less red
enc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r','24','-i','-','-i','audio_final4.wav',
  '-vf','scale=in_range=pc:out_range=tv:out_color_matrix=bt709,format=yuv420p',
  '-c:v','libx264','-preset','slow','-crf','19','-maxrate','4300k','-bufsize','8600k','-profile:v','high',
  '-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-color_range','tv',
  '-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart','reel_final2.mp4'],stdin=subprocess.PIPE)
def frames():
    yield from reader('src/p1.mov',0,N1)
    yield from reader('src/p2.mov',7,N-N1)
k=0
for fr in frames():
    t=k/FPS; z=zoom(t)
    fr=np.stack([LUT[c][fr[...,c]] for c in range(3)],-1)
    if abs(z-1)>1e-4:
        M=np.float32([[z,0,AX*(1-z)],[0,z,AY*(1-z)]])
        fr=cv2.warpAffine(fr,M,(W,H),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_REFLECT)
    if t<T_OPEN-1e-6:
        small=cv2.resize(fr,(WW,WH),interpolation=cv2.INTER_AREA).astype(np.float32)
        canvas=np.full((H,W,3),13,np.float32)
        canvas[WY:WY+WH,WX:WX+WW]=small*WMASK+13*(1-WMASK)
        fr=canvas.astype(np.uint8)
    ov=cv2.imread(f'ovl/f_{k:05d}.png',cv2.IMREAD_UNCHANGED)
    if ov is not None and ov.shape[2]==3:
        fr=np.ascontiguousarray(ov[...,::-1])
    elif ov is not None and ov[...,3].max()>0:
        a=ov[...,3:4].astype(np.float32)/255.0; rgb=ov[...,2::-1].astype(np.float32)
        fr=(fr.astype(np.float32)*(1-a)+rgb*a).astype(np.uint8)
    if t>N/FPS-0.1:  # fade to black last ~0.1 s
        fr=(fr.astype(np.float32)*max(0,(N/FPS-t)/0.1)).astype(np.uint8)
    enc.stdin.write(np.ascontiguousarray(fr).tobytes()); k+=1
enc.stdin.close(); enc.wait(); print('frames',k)
