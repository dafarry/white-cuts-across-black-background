#!/bin/bash

# Linux shell commands to create animated GIF for display on github

# Uses imagemagick and gifsicle, which are in the repositories of
# most Linux distros 

for f in vidcuts/*.png; do
    convert $f ${f%.png}.gif
done

gifsicle -d5 -l0 vidcuts/file????.gif >cuts-anim.gif

