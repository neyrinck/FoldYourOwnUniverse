import sys,os
sys.path.append(os.path.realpath('..'))

import numpy as N, pylab as M
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons

# These variables are global, so they're defined up here first
scale = 1.0
slider_scale = 1.0

radio_mode = "points"
radio_buttons = 0

psi = 1.0

def init():
    """ Set up the initial conditions """
    # Sets up initial dimensions
    M.figure(figsize=(8,8))
    
    if (len(sys.argv) > 1):
        density = N.loadtxt(os.path.join(sys.path[0], sys.argv[1]))        
        # Use a smaller scale for alterate files so the initial image is easier to see 
        density_k = N.fft.rfftn(density*1e2)  
        
    else:
        density=N.loadtxt(os.path.join(sys.path[0], './densmesh.txt'))
        # Real Fourier transform of "density" 
        density_k = N.fft.rfftn(density*3e3) # 3e3 to enhance contrast    

    global psi
    psi = zeldovich(density_k)
    # Zel'dovich displacement field

    global scale
    global slider_scale
    global radio_mode
    global radio_buttons
    
    scale = 1.0
    slider_scale = 20.0

    axcolor = 'lightgoldenrodyellow'
    axScale = plt.axes([0.15, 0.1, 0.7, 0.03], axisbg=axcolor)
    
    slider_scale = Slider(axScale, 'Scale', 0.0, 20.0, 1.0)
    slider_scale.on_changed(sliderUpdate)    

    radio_buttons = RadioButtons(plt.axes([0.425, 0.85, 0.15, 0.15]), ("points", "quadmesh"))
    radio_buttons.on_clicked(radioUpdate)

    # Attempting to removed axes from the graph
    plt.axes([0.15, 0.15, 0.7, 0.7])
    plt.xticks([])
    plt.yticks([])        

    return density_k, psi    
            
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

def plotvertices(psi):
    global radio_mode
    
    boxsize = 500.
    pos = psi2pos(psi*scale,boxsize)
    
    plt.axes([0.15, 0.15, 0.7, 0.7])
    plt.xticks([])
    plt.yticks([])           
    
    plt.xlim((boxsize * -0.2), (boxsize * 1.2))
    plt.ylim((boxsize * -0.2), (boxsize * 1.2))
    
    #plot the vertices
    if radio_mode == "points":
        M.scatter(pos[:,:,0].flat,pos[:,:,1].flat,s=1,lw=0)
    elif radio_mode == "quadmesh":
        M.pcolor(pos[:,:,0],pos[:,:,1],0.*pos[:,:,0],alpha=0.3,vmin=0.,vmax=1.)

# When the slider is changed, redraw the screen with the updated scale
def update():
    global psi
    
    M.cla()
    plotvertices(psi)

def sliderUpdate(val):
    global scale
    global slider_scale
    scale = slider_scale.val
    update()

def radioUpdate(button):
    global radio_mode
    radio_mode = button
    update()