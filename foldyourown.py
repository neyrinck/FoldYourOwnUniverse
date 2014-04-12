import sys,os
sys.path.append(os.path.realpath('..'))

import numpy as N, pylab as M
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

scale = 1.0
slider_scale = 1.0
psi = 1.0

def init():
    """ Set up the initial conditions """
    density=N.loadtxt(os.path.join(sys.path[0], './densmesh.txt'))
    # Real Fourier transform of "density" 
    density_k = N.fft.rfftn(density*1e3) # 1e3 to enhance contrast

    global psi
    psi = zeldovich(density_k)
    # Zel'dovich displacement field

    global scale
    global slider_scale
    
    scale = 1.0
    slider_scale = 50.0

    axcolor = 'lightgoldenrodyellow'
    axScale = plt.axes([0.25, 0.1, 0.65, 0.03], axisbg=axcolor)
    slider_scale = Slider(axScale, 'Scale', 0.0, 50.0, 1.0)
    slider_scale.on_changed(update)    

    plt.xticks([])
    plt.yticks([])        
    axgraph = plt.axes([0.15, 0.25, 0.7, 0.7])

    axgraph.spines['right'].set_color('none')
    axgraph.spines['top'].set_color('none')

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
    pos = psi2pos(psi*scale,boxsize=500.)
    
    #plot the vertices
    M.scatter(pos[:,:,0].flat,pos[:,:,1].flat,s=1,lw=0)
def update(val):
    global psi
    global scale
    global slider_scale
    scale = slider_scale.val
    M.cla()
    plotvertices(psi)
