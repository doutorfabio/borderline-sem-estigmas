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
SEG=[(0,6.02,1.00,1.04),(6.02,8.26,1.12,1.13),(8.26,13.40,1.02,1.06),(13.40,16.45,1.04,1.04),(16.45,19.85,1.04,1.08),(19.85,23.958,1.06,1.06),
     (23.958,25.15,1.06,1.07),(25.15,28.25,1.02,1.02),(28.25,33.03,1.02,1.06),(33.03,35.82,1.14,1.16),(35.82,39.29,1.05,1.05),(39.29,41.64,1.05,1.08),
     (41.64,44.80,1.02,1.02),(44.80,47.17,1.02,1.05),(47.17,50.0,1.12,1.14)]
def zoom(t):
    for a,b,z0,z1 in SEG:
        if a<=t<b: p=(t-a)/(b-a); p=p*p*(3-2*p); return z0+(z1-z0)*p
    return 1.0
AX,AY=560,700
enc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r','24','-i','-','-i','audio_final.wav',
  '-vf','scale=in_range=pc:out_range=tv:out_color_matrix=bt709,format=yuv420p',
  '-c:v','libx264','-preset','slow','-crf','19','-maxrate','4300k','-bufsize','8600k','-profile:v','high',
  '-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-color_range','tv',
  '-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart','reel_v2.mp4'],stdin=subprocess.PIPE)
def frames():
    yield from reader('src/p1.mov',0,N1)
    yield from reader('src/p2.mov',7,N-N1)
k=0
for fr in frames():
    t=k/FPS; z=zoom(t)
    if abs(z-1)>1e-4:
        M=np.float32([[z,0,AX*(1-z)],[0,z,AY*(1-z)]])
        fr=cv2.warpAffine(fr,M,(W,H),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_REFLECT)
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
