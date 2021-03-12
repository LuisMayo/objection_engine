### Windows
#### Unable to install polyglot of pip dependencies
You may need to manually install PyICU.whl y PyCLD2.whl. Download the appropiate version for your python version and arch from https://www.lfd.uci.edu/~gohlke/pythonlibs/

### Linux(Debian-like)

#### ModuleNotFoundError: No module named 'tkinter'
Install it using `sudo apt-get install python3-tk`

#### Problems installing libICU
Install aditional dependencies
```bash
sudo apt-get install libicu-dev pkg-config
```

#### Can't find codec
In Linux it may be a bit harder to set the enviorenment properly. More specifically it may be hard to install required codecs.
If having a codec problem (like "couldn't find codec for id 27") you may need to compile ffmpeg and opencv by yourself.
You should be good using these guides (tested on Ubuntu with success and on Debian without success)
  - [FFMPEG compilation guide](https://trac.ffmpeg.org/wiki/CompilationGuide/Ubuntu). In Ubuntu 20.04 the compilation may throw some problems. Solve it using `sudo apt-get install libunistring-dev`
  - [Opencv compilation guide](https://docs.opencv.org/master/d2/de6/tutorial_py_setup_in_ubuntu.html)
