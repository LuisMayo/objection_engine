### Windows
#### Unable to install polyglot of pip dependencies
You may need to manually install PyICU.whl and PyCLD2.whl. Download the appropiate version for your python version and arch from https://www.lfd.uci.edu/~gohlke/pythonlibs/

### Linux(Debian-like)

#### ModuleNotFoundError: No module named 'tkinter'
Install it using `sudo apt-get install python3-tk`

#### Problems installing libICU
Install aditional dependencies
```bash
sudo apt-get install libicu-dev pkg-config
```
