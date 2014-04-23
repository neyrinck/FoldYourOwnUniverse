import sys,os
sys.path.append(os.path.realpath('..'))

import numpy as N, pylab as M
import matplotlib.image as MI
from matplotlib.widgets import Slider, RadioButtons

def convertimage(filename):
    """ uses native matplotlib functionality. only works for PNG's """
    img = MI.imread(filename)
    # grayscale it, then return the 2D array
    return N.transpose(N.mean(img[:,:,:3],axis=2))[:,::-1]

def getkgrid(ng=64):
    """ ng = number of particles in each dim """

    thirdim=ng/2+1
    sk = (ng,thirdim)

    kx = N.fromfunction(lambda x,y:x, sk).astype(N.float32)
    kx[N.where(kx > ng/2)] -= ng
    ky = N.fromfunction(lambda x,y:y, sk).astype(N.float32)
    ky[N.where(ky > ng/2)] -= ng

    k2 = kx**2+ky**2
    k2[0,0] = 1.
    return kx/k2, ky/k2

def zeldovich(dk,boxsize=None):
    """ implements the Zel'dovich approximation to move particles """

    sk = dk.shape #shape of the Fourier-space density field
    ng = sk[0] #number of particles in each dimension

    kx, ky = getkgrid(ng)

    # psi = displacement of each particle from initial conditions.
    psi = N.empty((ng,ng,2),dtype=N.float32)
    psi[:,:,0] = N.fft.irfftn(-1j*dk*kx)
    psi[:,:,1] = N.fft.irfftn(-1j*dk*ky)
    return psi

def psi2pos(psi,boxsize=500.):
    """ 
    displacement field to positions 
    (adding displacement to a regular lattice)
    """
    ng = psi.shape[0] # number of particles in each dimension

    x=boxsize/ng*N.fromfunction(lambda x,y:x, (ng,ng)) 
    # x positions on a regular lattice

    pos = 1.*psi
    pos[:,:,0] += x
    pos[:,:,1] += N.transpose(x)
    return pos

def plotvertices(psi,scale,init=False):
    global radio_mode
    
    M.cla()
    boxsize = 500.
    pos = psi2pos(psi*scale,boxsize)
    
    ax = M.axes([0.15, 0.15, 0.7, 0.7])
    M.xticks([])
    M.yticks([])           
    
    M.xlim((boxsize * -0.2), (boxsize * 1.2))
    M.ylim((boxsize * -0.2), (boxsize * 1.2))
    
    #N.savetxt('test.pos',pos.reshape(64**2,2),fmt='%f')
    c = N.zeros((pos.shape[0]-1,pos.shape[0]-1),dtype=N.float32)

    #plot the vertices
    if radio_mode == "Points":
        ax.scatter(pos[:,:,0].flat,pos[:,:,1].flat,s=1,lw=0)
    elif radio_mode == "Mesh":
        ax.pcolorfast(pos[:,:,0],pos[:,:,1],c,alpha=0.1,vmin=0.,vmax=1.)
        #M.pcolor(pos[:,:,0],pos[:,:,1],c,alpha=0.3,vmin=0.,vmax=1.)

# When the slider is changed, redraw the screen with the updated scale
def update(scale,init=False):
    global psi
    plotvertices(psi,scale,init=init)
    M.draw()

def sliderUpdate(val):
    global scale
    global slider_scale
    scale = slider_scale.val
    update(scale)

def radioUpdate(button):
    global radio_mode
    global scale
    radio_mode = button
    update(scale)



scale = 1.0
slider_scale = 1.0

radio_mode = "Points"
radio_buttons = 1

psi = 1.0

# Sets up initial dimensions
M.figure(figsize=(8,8))
    
if (len(sys.argv) > 1):
    #density = N.loadtxt(os.path.join(sys.path[0], sys.argv[1]))        
    density = convertimage(os.path.join(sys.path[0], sys.argv[1]))

        
else:
    density=N.loadtxt(os.path.join(sys.path[0], './densmesh.txt'))

density -= N.min(density)
density = density/N.mean(density) - 1.
density *= density.shape[0]/N.std(density)

# Real Fourier transform of "density" 
density_k = N.fft.rfftn(density)  
psi = zeldovich(density_k)
# Zel'dovich displacement field

scale = 1.0
slider_scale = 20.0

axcolor = 'lightgoldenrodyellow'
axScale = M.axes([0.15, 0.1, 0.7, 0.03], axisbg=axcolor)
    
slider_scale = Slider(axScale, 'Scale', 0.0, 2.0, 1.0)
slider_scale.on_changed(sliderUpdate)    

radio_buttons = RadioButtons(M.axes([0.425, 0.85, 0.15, 0.15]), ("Points", "Mesh"))
radio_buttons.on_clicked(radioUpdate)

M.axes([0.15, 0.15, 0.7, 0.7])
M.xticks([])
M.yticks([])        

update(scale)
M.show()
