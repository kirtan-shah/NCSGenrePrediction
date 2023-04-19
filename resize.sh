
mkdir -p specgrams128 && gfind specgrams -type f -printf "%f\0" | xargs -0 -P 16 -Iinfile ffmpeg -hide_banner -loglevel error -i "specgrams/infile" -vf scale=128:128 "specgrams128/infile"
