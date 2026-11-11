# retime das 6 cenas do vídeo para casar com a narração; sai base 1080x1920 30 fps + bed de áudio
import subprocess, sys
src=sys.argv[1]
SRC=[(0,3.25),(3.25,6.375),(6.375,9.2083),(9.2083,12.375),(12.375,16.2083),(16.2083,20.04)]
DST=[(0,3.70),(3.70,7.15),(7.15,11.00),(11.00,13.98),(13.98,17.18),(17.18,20.02)]
v=[];a=[]
for i,((s0,s1),(d0,d1)) in enumerate(zip(SRC,DST)):
    f=(d1-d0)/(s1-s0)
    v.append(f"[0:v]trim={s0}:{s1},setpts={f:.5f}*(PTS-STARTPTS),scale=1080:1920:flags=lanczos,fps=30,trim=duration={d1-d0:.4f},setpts=PTS-STARTPTS[v{i}];")
    a.append(f"[0:a]atrim={s0}:{s1},asetpts=PTS-STARTPTS,atempo={1/f:.5f},atrim=duration={d1-d0:.4f},asetpts=PTS-STARTPTS[a{i}];")
fc=''.join(v)+''.join(a)+''.join(f'[v{i}]' for i in range(6))+'concat=n=6:v=1:a=0[vo];'+''.join(f'[a{i}]' for i in range(6))+'concat=n=6:v=0:a=1[ao]'
subprocess.run(['ffmpeg','-v','error','-y','-i',src,'-filter_complex',fc,'-map','[vo]','-c:v','libx264','-crf','12','-preset','medium','-pix_fmt','yuv420p','base.mp4','-map','[ao]','-ar','48000','bed.wav'],check=True)
print(subprocess.run(['ffprobe','-v','error','-show_entries','stream=width,height,r_frame_rate,nb_frames,duration','-of','compact','base.mp4'],capture_output=True,text=True).stdout)
