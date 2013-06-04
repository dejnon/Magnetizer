# Magnetizer #
==========

An application for modeling various spin dynamics (based on simplified Glauber algorithm) in 1D (Ising-like) ferromagnet grid.
For more information on the subject you can visit:
[Phase diagram for a zero-temperature Glauber dynamics under partially synchronous updates](http://pre.aps.org/abstract/PRE/v86/i5/e051113)
Or other publications on the subject.

## Running ##
Fork this repository. Navigate to project directory and run the file:
```
python main.py
```

## Features ##
* Seamles, runtime transition between different updating modes
* Set timestep lenght
* Save image file with simulation view (.png)
* Adjust simulation time
* Set boundaries conditions
* Adjust "ordering parameter" W0 (with python syntax)
* Start/Stop simulation

## Running into troubles ##
For this program to run you need:
* wxPython
* MatPlotLib
* NumPy
* SciPy
I used this link to get over dependencies:
[Install Python, NumPy, SciPy, and matplotlib on Mac OS X](http://penandpants.com/2012/02/24/install-python/)

## License ##
Magnetizer is MIT licensed. Do whatever you want.
