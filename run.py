import foldyourown
import sys
import pylab as M

dk, psi = foldyourown.init()
foldyourown.plotvertices(psi,scale=float(sys.argv[1]))
M.show()
