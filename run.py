import foldyourown
import sys
import pylab as M

dk, psi = foldyourown.init()

if len(sys.argv) == 2:
    foldyourown.plotvertices(psi,scale=float(sys.argv[1]))
    M.show()
else:
    print 'Usage: python run.py AgeOfUniverse'
    print 'Valid Range for AgeOfUniverse: 0 - 100'
    print 'AgeOfUniverse 1 is ~ 14B years'
