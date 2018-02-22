FoldYourOwnUniverse
===================
Python module to set the initial conditions of a 2D universe, and see approximately how that would evolve gravitationally.

An image such as the Mona Lisa

![Mona Lisa](monalisa_small.png?raw=true "Mona Lisa")

morphs gravitationally to 

![Mona Lisa (folded)](monalisa_folded.png?raw=true "Mona Lisa (Folded)")

# Usage:

Random cosmological initial conditions:
python foldyourown.py

Use NASA logo for initial conditions:
python foldyourown.py NASA_logo.png

Use Mona Lisa logo for initial conditions:
python foldyourown.py monalisa.png

Input .png can be arbitrary; to specify approximate resolution, use the optional third argument, e.g.

python foldyourown.py NASA_logo.png 96

# Science:

The radio button 'Zeldovich' refers to the Zeldovich approximation (Zeldovich, 1970), which returns a qualitatively accruate description of the cosmic web.

'NoCollapse' inhibits overcrossing, returning a 2D version of the spherical (circular, in 2D) collapse approximation (Neyrinck M., 2013, MNRAS, 428, 141, arXiv:1204.1326).

Project started at NASA's Space Apps hackathon event:
https://2014.spaceappschallenge.org/project/fold-your-own-universe/
