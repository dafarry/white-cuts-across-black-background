#!/usr/bin/env python3

import numpy as np
from PIL import Image, ImageDraw, ImageChops, ImageOps, ImageFilter, ImageEnhance
import os, shutil

size=800
blankimg = Image.new('L', (size, size), color=0)
img = blankimg.copy()
shutil.rmtree("vidcuts", ignore_errors=True)
os.makedirs("vidcuts")

cuts = 20
for cut in range(cuts * 5):
    rand = np.random.RandomState(cut % cuts + 20)
    anglerotate = np.exp(rand.uniform(0, np.pi) * 1j)
    heading = np.array([anglerotate * 1j]).view(float)
    offset = rand.uniform(-0.4, 0.4)
    randomwalk = np.cumsum(rand.uniform(-0.0015, 0.0015, 2*size))
    smoothline = np.convolve(randomwalk,np.ones(10)/10,'same')
    centeredline = (smoothline - smoothline[len(smoothline) // 2])
    offsetline = centeredline + offset
    complexline = offsetline * 1j + np.linspace(-1, 1, len(offsetline))
    rotatedline = complexline * anglerotate
    linelist = list(((rotatedline.view(float) + 0.5) * size).astype(int))
    imgline = blankimg.copy()
    ImageDraw.Draw(imgline).line(linelist, fill=255, width=2)
    mask1 = ImageOps.expand(imgline, border=1, fill=255)
    floodpoint = (heading * (offset + 0.05) + 0.5) * size
    ImageDraw.floodfill(mask1,floodpoint,255)
    mask1 = ImageOps.crop(mask1, border=1)
    mask2 = ImageChops.lighter(imgline, ImageChops.invert(mask1))
    img = ImageChops.lighter(img, imgline)
    split1 = ImageChops.darker(img, mask1)
    split2 = ImageChops.darker(img, mask2)
    splitsize = rand.randint(10, 20)
    lineblur = imgline.filter(ImageFilter.GaussianBlur(radius=10))
    for step in range(10):
        shift = 2 + splitsize * step / 10 
        splitstep = (heading * shift).astype(int)
        shifted1 =  ImageChops.offset(split1, *splitstep)
        shifted2 =  ImageChops.offset(split2, *-splitstep)
        img = ImageChops.lighter(shifted1, shifted2)
        flash = ImageEnhance.Contrast(lineblur).enhance(10 - 2 * step)
        flashimg = ImageChops.lighter(img, flash)
        cropimg = ImageOps.crop(flashimg, border=size*.05)
        cropimg.save('vidcuts/file{:04d}.gif'.format(cut % cuts * 10 + step))

os.system("gifsicle -d5 -l0 vidcuts/file????.gif >cuts-anim.gif")


