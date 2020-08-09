# Mandelbrot multibrot animation

This is a Python-3 script for creating a multibrot gif animation. It
uses the "numpy" and "pillow" libraries to generate a sequence of gif
images, then calls the "gifsicle" command-line app to assemble them
into an animation.

[multibrot-make-gif.py](multibrot-make-gif.py)

Installation instructions for the Python libraries and gifsicle are below.

![Mandelbrot multibrot animation](multibrot.gif)

Installation instructions for Python libraries
----------------------------------------------

Ubuntu and Debian
-----------------
Works fine with system Python3, version 3.7.5, at the time of writing.
Install the required packages:

    sudo apt install python3-numpy python3-pil gifsicle

Windows
-------
Download & install the latest Python from python.org
Then at the Windows Command Prompt, install the libraries like so:

    python -m pip install --upgrade pip
    python -m pip install --upgrade wheel setuptools
    python -m pip install numpy
    python -m pip install pillow

Download the gifsicle zipfile from: https://eternallybored.org/misc/gifsicle/

Unzip the file, and put "gifsicle.exe" either in the same directory as
the Python script or place it somewhere on your PATH, e.g.: 
in C:\WINDOWS

Change line 6 of multibrot-make-gif.py to:

    ttf = "consolab.ttf" 

Change line 43 to:

    txt = "Z = Z " + ' ' * len(pow) + " + C"

Run the script with:

    python multibrot-make-gif.py

