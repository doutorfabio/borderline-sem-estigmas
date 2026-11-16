#!/bin/bash
# Junta as partes, mistura narração + trilha baixa, normaliza em -14 LUFS e põe a legenda como faixa.
set -e
cd "$(dirname "$0")"
ls parte_*.mp4 | sort -V | sed "s/^/file '/;s/$/'/" > partes.txt
ffmpeg -y -v error -f concat -safe 0 -i partes.txt -c copy video_mudo.mp4
ffmpeg -y -v error -i audio/narracao.wav -i audio/trilha.wav -filter_complex \
 "[0]aformat=channel_layouts=mono[v];[1]volume=0.075[m];[v][m]amix=inputs=2:normalize=0,pan=stereo|c0=c0|c1=c0[a]" -map "[a]" audio/mix_bruto.wav
# loudnorm em duas passagens (linear) para chegar em -14 LUFS sem bombear
M=$(ffmpeg -hide_banner -i audio/mix_bruto.wav -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | python3 -c "import sys,json,re;d=json.loads(re.search(r'\{[^}]*\}',sys.stdin.read(),re.S).group());print(f\"measured_I={d['input_i']}:measured_TP={d['input_tp']}:measured_LRA={d['input_lra']}:measured_thresh={d['input_thresh']}:offset={d['target_offset']}\")")
ffmpeg -y -v error -i audio/mix_bruto.wav -af "loudnorm=I=-14:TP=-1.5:LRA=11:$M:linear=true,aresample=48000" audio/mix.wav
ffmpeg -y -v error -i video_mudo.mp4 -i audio/mix.wav -i legenda.srt -map 0:v -map 1:a -map 2:s \
 -c:v copy -c:a aac -b:a 192k -c:s mov_text -metadata:s:s:0 language=por -t $(ffprobe -v error -show_entries format=duration -of csv=p=0 video_mudo.mp4) -movflags +faststart zanarini-16-anos.mp4
ffprobe -v error -show_entries format=duration:stream=codec_type,codec_name,width,height,r_frame_rate -of compact zanarini-16-anos.mp4
