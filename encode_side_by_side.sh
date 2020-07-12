#!/bin/bash

## encode with 24 fps
#ffmpeg -r 24 -f image2 -pattern_type glob -i "*?png" -vcodec libx264 -crf 20 -pix_fmt yuv420p output.mp4

# encode with 2 fps
ffmpeg -r 2 -f image2 -pattern_type glob -i "output/side_by_side/*?png" -vcodec libx264 -crf 20 -pix_fmt yuv420p output/side_by_side_2_fps.mp4 -y

# encode with 1 fps
ffmpeg -r 1 -f image2 -pattern_type glob -i "output/side_by_side/*?png" -vcodec libx264 -crf 20 -pix_fmt yuv420p output/side_by_side_1_fps.mp4 -y

