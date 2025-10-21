#!/bin/sh

dir=./
path=v1

echo $dir
echo $path


instaloader --login=bernardhp :saved \
    --dirname-pattern=$path \
    --filename-pattern={shortcode}/item \
    --no-compress-json \
    --no-videos --no-video-thumbnails \
    --no-pictures --no-caption \
    --slide=1 \
    --geotags \
    --count 10