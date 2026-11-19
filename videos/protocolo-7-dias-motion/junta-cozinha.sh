#!/bin/bash
# uso: junta.sh RUIM BOA MOTION_V MOTION_A SAIDA
set -e
R=$1; B=$2; MV=$3; MA=$4; O=$5
V='scale=1080:1920:flags=lanczos,setsar=1,fps=30,format=yuv420p'
ffmpeg -v error -y -i "$R" -i "$B" -i "$MV" -i "$MA" -filter_complex "
[0:v]trim=0:9.6,setpts=PTS-STARTPTS,$V,split[r1][r2];
[r2]reverse,setpts=PTS/7,fps=30[rw];
[1:v]trim=0:10.0,setpts=PTS-STARTPTS,$V[b];
[2:v]$V[m];
[0:a]atrim=0:9.6,asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,volume=10dB,asplit[ra1][ra2];
[ra2]areverse,asetrate=48000*7,aresample=48000,highpass=f=300,volume=-14dB,apad=whole_dur=1.3714,atrim=0:1.3714[rwa];
[1:a]atrim=0:10.0,asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,volume=11.5dB,afade=t=out:st=9.85:d=0.15[ba];
[3:a]aresample=48000,aformat=channel_layouts=stereo,volume=2.2dB[ma];
[r1][ra1][rw][rwa][b][ba][m][ma]concat=n=4:v=1:a=1[v][a0];
[a0]alimiter=limit=0.79:attack=1:release=50:level=disabled[a]" -map "[v]" -map "[a]" -c:v libx264 -crf 16 -preset slow -pix_fmt yuv420p -c:a aac -b:a 256k -movflags +faststart "$O"
