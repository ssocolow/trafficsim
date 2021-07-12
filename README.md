# trafficsim
Traffic simulation

<! --- ![Example of GUI simulation](https://github.com/ssocolow/trafficsim/blob/master/trafficsimguisample.png) --->
<img align="center" width=100 height=100 src="https://github.com/ssocolow/trafficsim/blob/master/trafficsimguisample.png">

This is a traffic simulation of the Stillwater - Broadway intersection in Bangor, Maine.
Algorithms like neural network agents and conventional algorithms like first come first serve and clock timed
use the simulation to control the lights and then collect data like car throughput and wait time
which are metrics by which to evalute different algorithms.
By Simon Socolow and Nhan Ngo

The presentation of this project is now on youtube:
https://youtu.be/Gt9PwPbdT-0

A visualization of the first come first serve algorithm using the library is also on youtube:
https://www.youtube.com/watch?v=jWmylUEwOsA

The (outdated but still useful to learn about the project) research paper can be found here:
https://drive.google.com/file/d/1PqmWoTthooViPLWQH_-LLIsqouMrHyIQ/view?usp=sharing

or here if you don't want to use google drive:
https://github.com/ssocolow/Pastebin/blob/master/Ngo_Nhan_Socolow_Simon_Research_Paper.pdf

## Dependencies
Many files require the Neural-Network-Python-Lib library for neural network functionality

https://github.com/ssocolow/Neural-Network-Python-Lib

Also make sure to change the sys.path.insert function at the top of some files to the path on your computer to the directory
containing the neural network library.  This is a very common source of errors.

---

If you want to see the graphical representation of the intersection (functionality which resides in showsim.py)
you need to download the py5 graphics library

https://github.com/ssocolow/py5

The py5 library uses tkinter (the python graphics module) which usually comes preinstalled on systems.  
If it isn't installed, you will need to get it.  
If you are on debian or ubuntu based linux systems with the apt package manager you can get tkinter using this command:

`sudo apt-get install python-tk`


## Files
### Module Files

Car.py contains car functionality

Lane.py conatains lane functionality

Intersection.py contains intersection functionality

showsim.py contains graphical visualization functionality

---

### Running files
(files meant to be run)

simulation.py can be used to collect data on or visualize the first come first serve and clock timed algorithms as well as loading in a neural network to look at what it is doing using the graphical representation of the intersection.

NeuroevolutionTrafficControl.py can be used to do and collect data on the neuroevolution process as well as save the best neural net at the end

### Curent Status

There seems to either be a bug or a glitch where sometimes cars dissapear or appear or move where they aren't supposed to be.  Probably one of the checks if a car
can do a right turn or a left turn is slightly off.
