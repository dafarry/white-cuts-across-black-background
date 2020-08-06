#!/usr/bin/env python3

import tkinter as tk
import numpy as np
from PIL import Image, ImageDraw, ImageChops, ImageOps, ImageFilter, ImageEnhance
from PIL import ImageTk
import time

size=800
cuts, reps = 20, 8

blankimg = Image.new('L', (size, size), color=0)
root = tk.Tk()
label = tk.Label(root)
label.pack()
img = blankimg.copy()

cut, step = 0, 0
while True:
    if step == 0:
        cut = (cut + 1) % (cuts * reps)
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

    shift = 2 + splitsize * step / 10 
    splitstep = (angleshift * shift).astype(int)

    shifted1 =  ImageChops.offset(split1, *-splitstep)
    shifted2 =  ImageChops.offset(split2, *splitstep)
    img = ImageChops.lighter(shifted1, shifted2)
    
    flash = ImageEnhance.Contrast(lineblur).enhance(10 - 2 * step)
    flashimg = ImageChops.lighter(img, flash)
    cropimg = ImageOps.crop(flashimg, border=size*.05)
    
    tkimg = ImageTk.PhotoImage(cropimg)
    label.config(image=tkimg)
    step = (step + 1) % 10

    # just crash out when window closed, terrible I know
    root.update()
    time.sleep(0.04)



