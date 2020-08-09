# White Cuts Across Black Background

A similar version to this interesting effect has been posted to
social media sites before but not as a seamless loop.
I couldn't trace its source so I've
coded up a seamless-loop version myself in Python.
Apologies to whoever originated the similar effect.

This file is about 50 lines of Python, using the Numpy and Pillow
libraries and ffmpeg to create the video:

[white-cuts-on-black-make-video.py](white-cuts-on-black-make-video.py)

This file is another version that uses Tkinter to display the video
to your screen in real time rather than making a video.

[white-cuts-on-black-display.py](white-cuts-on-black-display.py)

A short explanation of how the loop was achieved, and installation
instructions for the Python libraries are below the animation.

![White Cuts on Black Background](gif/cuts-anim.gif)

## How it works

The original inspiration was
[a post on Reddit](https://v.redd.it/sia4zssc80f21).
I don't know the origin but some commenters said they thought it originated
as a "[Milkdrop](https://en.wikipedia.org/wiki/MilkDrop)" effect.

My version started as an experimental exercise in generating a similar randomly
wavy line with random rotation and offset using Numpy array processing.
Once that looked OK, Pillow could be used to create masks either side of
the line to create split halves of the previous image frame then
move those halves away from the line.

My version here is a seamless loop.
The random number generator is seeded in a way that makes it repeat every
20 cuts. That sequence runs for eight repetitions and only the last is saved.
The first seven repetitions are enough to populate the background in a way
that gets repeated exactly the eighth time.

I did this as a "quick" coding challenge, hence the rather dense
uncommented Python code. I must admit that it proved
more difficult than I expected. I had to import nearly all of the various
graphics modules from the "pillow" image library to get enough features to
make it work. I consider it to be time reasonably well spent though, since
I now know a lot more about that image library than I did before.


## Installation instructions for Python libraries

**Windows**

Download & install the latest Python from python.org  
Then at the Windows Command Prompt, install the libraries like so:

    python -m pip install --upgrade pip
    python -m pip install --upgrade wheel setuptools
    python -m pip install numpy
    python -m pip install pillow

Download FFMpeg from ffmpeg.org  
Version 4.2.1 of FFMpeg was used at the time of writing.  
Only needed for making the mpeg video with the "makevideo" python script.  
Unzip the file, and put ffmpeg.exe somewhere on your PATH, e.g.: 
in C:\WINDOWS

**Ubuntu and Debian**

Works fine with system Python3, version 3.8.2, at the time of writing  
Install the following packages with `sudo apt install`

    python3-numpy python3-tk python3-pil python3-pil.imagetk ffmpeg

(Unlike PIL in PyPI, the "imagetk" is split off into a separate
package, which is a bit of a "gotcha".)



