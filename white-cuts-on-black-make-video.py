#!/usr/bin/env python3

import numpy as np
from PIL import Image, ImageDraw, ImageChops, ImageOps, ImageFilter, ImageEnhance
import os, shutil

size=800
blankimg = Image.new('L', (size, size), color=0)
shutil.rmtree("vidcuts", ignore_errors=True)
os.makedirs("vidcuts")
img = blankimg.copy()

cuts, reps = 20, 8
for cut in range(cuts * reps):
    rand = np.random.RandomState(cut % cuts + 100)
    anglerotate = np.exp(rand.uniform(0, np.pi) * 2j)
    angleshift = np.array([anglerotate * 1j]).view(float)
    offset = rand.uniform(0.05, 0.4)
    randomwalk = np.cumsum(rand.uniform(-0.0015, 0.0015, 2*size))
    smoothline = np.convolve(randomwalk,np.ones(10)/10,'same')
    centeredline = (smoothline - smoothline[len(smoothline) // 2])
    offsetline = centeredline + offset
    complexline = offsetline * 1j + np.linspace(-1, 1, len(offsetline))
    maskbox =  [1 -2j, -1 -2j]
    rotatedline = np.hstack((maskbox, complexline)) * anglerotate
    linelist = list(((rotatedline.view(float) + 0.5) * size).astype(int))
    imgline = blankimg.copy()
    ImageDraw.Draw(imgline).line(linelist, fill=255, width=2)
    mask1 = imgline.copy()
    ImageDraw.Draw(mask1).polygon(linelist, fill=255)
    mask2 = ImageChops.lighter(imgline, ImageChops.invert(mask1))

    img = ImageChops.lighter(img, imgline)
    split1 = ImageChops.darker(img, mask1)
    split2 = ImageChops.darker(img, mask2)
    
    splitsize = rand.randint(10, 20)
    lineblur = imgline.filter(ImageFilter.GaussianBlur(radius=10))
    
    for step in range(10):
        shift = 2 + splitsize * step / 10 
        splitstep = (angleshift * shift).astype(int)
    
        shifted1 =  ImageChops.offset(split1, *-splitstep)
        shifted2 =  ImageChops.offset(split2, *splitstep)
        img = ImageChops.lighter(shifted1, shifted2)
        
        flash = ImageEnhance.Contrast(lineblur).enhance(10 - 2 * step)
        flashimg = ImageChops.lighter(img, flash)
        cropimg = ImageOps.crop(flashimg, border=size*.05)
        cropimg.save('vidcuts/file{:04d}.png'.format(cut % cuts * 10 + step))

os.system("ffmpeg -y -framerate 20 -i vidcuts/file%04d.png " +
          "-loglevel warning -pix_fmt yuv420p cuts-anim.mp4")


