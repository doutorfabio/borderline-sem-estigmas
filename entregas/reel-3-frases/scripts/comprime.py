import subprocess, re, sys
src,dst,KEEP,TEMPO=sys.argv[1],sys.argv[2],float(sys.argv[3]),float(sys.argv[4])
dur=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',src],capture_output=True,text=True).stdout)
out=subprocess.run(['ffmpeg','-hide_banner','-i',src,'-af','silencedetect=n=-55dB:d=0.30','-f','null','-'],capture_output=True,text=True).stderr
st=[float(x) for x in re.findall(r'silence_start: ([0-9.]+)',out)]; en=[float(x) for x in re.findall(r'silence_end: ([0-9.]+)',out)]
if len(en)<len(st): en.append(dur)
keep=[]; t=0.0
for s,e in zip(st,en):
    if s<=0.01: t=max(e-0.06,0); continue
    if e>=dur-0.02: keep.append((t,min(s+0.2,dur))); t=None; break
    keep.append((t,s+KEEP/2)); t=e-KEEP/2
if t is not None: keep.append((t,dur))
parts=''.join(f"[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.015,afade=t=out:st={b-a-0.015:.3f}:d=0.015[s{i}];" for i,(a,b) in enumerate(keep))
cat=''.join(f'[s{i}]' for i in range(len(keep)))+f'concat=n={len(keep)}:v=0:a=1,atempo={TEMPO}[o]'
subprocess.run(['ffmpeg','-v','error','-y','-i',src,'-filter_complex',parts+cat,'-map','[o]','-ar','48000',dst],check=True)
print(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',dst],capture_output=True,text=True).stdout.strip())
