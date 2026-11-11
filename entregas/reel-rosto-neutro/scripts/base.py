import subprocess, sys
src=sys.argv[1]
SRC=[(0,5.583),(5.583,8.958),(8.958,11.0),(11.0,15.958),(15.958,20.04)]
DST=[(0,5.75),(5.75,9.35),(9.35,12.50),(12.50,16.90),(16.90,20.0)]
v=[];a=[]
for i,((s0,s1),(d0,d1)) in enumerate(zip(SRC,DST)):
    f=(d1-d0)/(s1-s0)
    v.append(f"[0:v]trim={s0}:{s1},setpts={f:.5f}*(PTS-STARTPTS),scale=1080:1920:flags=lanczos,fps=30,trim=duration={d1-d0:.4f},setpts=PTS-STARTPTS[v{i}];")
    a.append(f"[0:a]atrim={s0}:{s1},asetpts=PTS-STARTPTS,atempo={1/f:.5f},atrim=duration={d1-d0:.4f},asetpts=PTS-STARTPTS[a{i}];")
n=len(SRC)
fc=''.join(v)+''.join(a)+''.join(f'[v{i}]' for i in range(n))+f'concat=n={n}:v=1:a=0[vo];'+''.join(f'[a{i}]' for i in range(n))+f'concat=n={n}:v=0:a=1[ao]'
subprocess.run(['ffmpeg','-v','error','-y','-i',src,'-filter_complex',fc,'-map','[vo]','-c:v','libx264','-crf','12','-preset','medium','-pix_fmt','yuv420p','base.mp4','-map','[ao]','-ar','48000','bed.wav'],check=True)
print(subprocess.run(['ffprobe','-v','error','-show_entries','stream=width,height,nb_frames,duration','-of','compact','base.mp4'],capture_output=True,text=True).stdout)
