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

def getkgrid(sk):
    """ sk = shape of k-space array """

    ny = (sk[1]-1)*2
    kx = N.fromfunction(lambda x,y:x, sk).astype(N.float32)
    kx[N.where(kx > sk[0]/2)] -= sk[0]
    ky = N.fromfunction(lambda x,y:y, sk).astype(N.float32)
    ky[N.where(ky > ny)] -= ny

    k2 = kx**2+ky**2
    k2[0,0] = 1.
    return kx/k2, ky/k2

def zeldovich(dk,boxsize=None):
    """ implements the Zel'dovich approximation to move particles """

    sk = dk.shape #shape of the Fourier-space density field
    print sk
    ng = sk[0] #number of particles in each dimension

    kx, ky = getkgrid(sk)

    # psi = displacement of each particle from initial conditions.
    nx = sk[0]
    ny = 2*(sk[1]-1)
    psi = N.empty((nx,ny,2),dtype=N.float32)
    psi[:,:,0] = N.fft.irfftn(-1j*dk*kx)
    psi[:,:,1] = N.fft.irfftn(-1j*dk*ky)
    return psi

def psi2pos(psi,boxsize=None):
    """ 
    displacement field to positions 
    (adding displacement to a regular lattice)
    """
    ng = psi.shape[0] # number of particles in each dimension

    if boxsize == None:
        boxsize = N.max(psi.shape[:2])

    x=boxsize/float(psi.shape[0])*N.fromfunction(lambda x,y:x, (psi.shape[0],psi.shape[1])) 
    # x positions on a regular lattice
    y=boxsize/float(psi.shape[1])*N.fromfunction(lambda x,y:y, (psi.shape[0],psi.shape[1]))

    pos = 1.*psi
    pos[:,:,0] += x
    pos[:,:,1] += y
    return pos

def plotvertices(psi,scale,init=False):
    global radio_mode
    
    M.cla()
    pos = psi2pos(psi*scale)
    
    ax = M.axes([0.15, 0.15, 0.7, 0.7])
    M.xticks([])
    M.yticks([])           
    
    boxsize = N.max(pos.shape[:2])
    M.axis(boxsize*N.array([-0.2,1.2,-0.2,1.2]))
    #M.xlim((pos.shape[1] * -0.2), (pos.shape[0] * 1.2))
    #M.ylim((pos.shape[] * -0.2), (pos.shape[1] * 1.2))
    
    #N.savetxt('test.pos',pos.reshape(64**2,2),fmt='%f')
    c = N.zeros((pos.shape[0]-1,pos.shape[1]-1),dtype=N.float32)

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
density *= 15./N.std(density)

# Real Fourier transform of "density" 
density_k = N.fft.rfftn(density)  
psi = zeldovich(density_k)
# Zel'dovich displacement field

scale = 1.0
slider_scale = 20.0

axcolor = 'lightgoldenrodyellow'
axScale = M.axes([0.15, 0.1, 0.7, 0.03], axisbg=axcolor)
    
slider_scale = Slider(axScale, 'Scale', 0.0, 3.0, 1.0)
slider_scale.on_changed(sliderUpdate)    

radio_buttons = RadioButtons(M.axes([0.425, 0.85, 0.15, 0.15]), ("Points", "Mesh"))
radio_buttons.on_clicked(radioUpdate)

M.axes([0.15, 0.15, 0.7, 0.7])
M.xticks([])
M.yticks([])        

update(scale)
M.show()
