FoldYourOwnUniverse
===================
Python module to set the initial conditions of a 2D universe, and see approximately how that would evolve gravitationally.
Using realistically random initial conditions:
!(Origami-Universe-O.png)

An image such as the Mona Lisa
![Mona Lisa](monalisa.png?raw=true "Mona Lisa")
morphs gravitationally to 
![Mona Lisa (folded)](monalisa_folded.png?raw=true "Mona Lisa (Folded)")

#Usage:

Initial data is as in cosmology:
python foldyourown.py

Initial data is the NASA logo:
python foldyourown.py NASA_logo.png

Initial data consists of (movie) stars
python foldyourown.py Stars.png

Input .png can be arbitrary; to specify approximate resolution, use the optional third argument, e.g.

python foldyourown.py NASA_logo.png 96

#Science:

The radio button 'Zeldovich' refers to the Zeldovich approximation (Zeldovich, 1970), which returns a qualitatively accruate description of the cosmic web.

'NoCollapse' inhibits overcrossing, returning a 2D version of the spherical (circular, in 2D) collapse approximation (Neyrinck M., 2013, MNRAS, 428, 141, arXiv:1204.1326).

Project started at NASA's Space Apps hackathon event:
https://2014.spaceappschallenge.org/project/fold-your-own-universe/
