### Windows
#### Unable to install polyglot of pip dependencies
You may need to manually install PyICU.whl y PyCLD2.whl. Download the appropiate version for your python version and arch from https://www.lfd.uci.edu/~gohlke/pythonlibs/

### Linux

#### ModuleNotFoundError: No module named 'tkinter'
Install it using `sudo apt-get install python3-tk`

#### Can't find codec
In Linux it may be a bit harder to set the enviorenment properly. More specifically it may be hard to install required codecs.
If having a codec problem (like "couldn't find codec for id 27") you may need to compile ffmpeg and opencv by yourself.
You should be good using these guides (tested on Ubuntu with success and on Debian without success)
  - [FFMPEG compilation guide](https://trac.ffmpeg.org/wiki/CompilationGuide/Ubuntu)
  - [Opencv compilation guide](https://docs.opencv.org/master/d2/de6/tutorial_py_setup_in_ubuntu.html)