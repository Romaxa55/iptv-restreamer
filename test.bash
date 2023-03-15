 #!/bin/bash
 VIDEO_IN="http://romaxa55.otttv.pw/iptv/Z258Z6P9EB74VZ/19183/index.m3u8"
 VIDEO_OUT=master
 HLS_TIME=4
 FPS=25
 GOP_SIZE=100
 CRF_P=21
 PRESET_P=veryslow
 V_SIZE_1=960x540
 V_SIZE_2=416x234
 V_SIZE_3=640x360
 V_SIZE_4=768x432
 V_SIZE_5=1280x720
 V_SIZE_6=1920x1080

 ffmpeg -i $VIDEO_IN \
     -preset $PRESET_P -keyint_min $GOP_SIZE -g $GOP_SIZE -sc_threshold 0 -r $FPS -c:v libx264 -pix_fmt yuv420p -crf $CRF_P \
     -map v:0 -s:0 $V_SIZE_1 -maxrate:0 2M -bufsize:0 4M \
     -map v:0 -s:1 $V_SIZE_2 -maxrate:1 145k -bufsize:1 290k \
     -map v:0 -s:2 $V_SIZE_3 -maxrate:2 365k -bufsize:2 730k \
     -map v:0 -s:3 $V_SIZE_4 -maxrate:3 730k -bufsize:3 1460k \
     -map v:0 -s:4 $V_SIZE_4 -maxrate:4 1.1M -bufsize:4 2.2M \
     -map v:0 -s:5 $V_SIZE_5 -maxrate:5 3M -bufsize:5 6M \
     -map v:0 -s:6 $V_SIZE_5 -maxrate:6 4.5M -bufsize:6 9M \
     -map v:0 -s:7 $V_SIZE_6 -maxrate:7 6M -bufsize:7 12M \
     -map v:0 -s:8 $V_SIZE_6 -maxrate:8 7.8M -bufsize:8 15.6M \
     -map a:0 -map a:0 -map a:0 -map a:0 -map a:0 -map a:0 -map a:0 -map a:0 -map a:0 -c:a aac -b:a 128k -ac 1 -ar 44100\
     -f hls -hls_time $HLS_TIME -hls_playlist_type vod \
     -var_stream_map "v:0,a:0 v:1,a:1 v:2,a:2 v:3,a:3 v:4,a:4 v:5,a:5 v:6,a:6 v:7,a:7 v:8,a:8" stream_%v.m3u8