import sys,os
sys.path.append(os.path.realpath('..'))

import numpy as N, pylab as M
import matplotlib.image as MI
from matplotlib.widgets import Slider, RadioButtons


def convertimage(filename,maxres=128):
    """ uses native matplotlib functionality. only works for PNG's """
    img = MI.imread(filename)
    # grayscale it, then return the 2D array
    img = N.transpose(N.mean(img[:,:,:3],axis=2))[:,::-1]

    if max(img.shape) > maxres:
        f = int(max(img.shape)/maxres)
    else:
        f = 1

    if f > 1:
        newimg = N.empty((img.shape[0]/f,img.shape[1]/f),N.float32)
        for i in N.arange(img.shape[0]/f):
            for j in N.arange(img.shape[1]/f):
                newimg[i,j] = N.mean(img[f*i:f*(i+1),f*j:f*(j+1)])
        return newimg
    else:
        return img
        

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
    ng = sk[0] #number of particles in each dimension

    kx, ky = getkgrid(sk)

    # psi = displacement of each particle from initial conditions.
    nx = sk[0]
    ny = 2*(sk[1]-1)
    psi = N.empty((nx,ny,2),dtype=N.float32)
    psi[:,:,0] = N.fft.irfftn(-1j*dk*kx)
    psi[:,:,1] = N.fft.irfftn(-1j*dk*ky)
    return psi

def collapse(dzeld,boxsize=None):

    wgt2 = N.where(dzeld > -2)
    wle2 = N.where(dzeld <= -2)

    divpsi = N.empty(dzeld.shape)
    divpsi[wgt2] = dzeld[wgt2]
    divpsi[wle2] = -2

    dk = N.fft.rfftn(divpsi)

    sk = dk.shape #shape of the Fourier-space density field
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

    x=N.fromfunction(lambda x,y:x, (psi.shape[0],psi.shape[1])) 
    # x positions on a regular lattice
    y=N.fromfunction(lambda x,y:y, (psi.shape[0],psi.shape[1]))

    pos = 1.*psi
    pos[:,:,0] += x
    pos[:,:,1] += y
    return pos

def plotvertices(pos,init=False):
    global radio_mode
    global radio_mode_physics
    global density
    global viewaxes
    
    M.cla()
    
    ax = M.axes(viewaxes)
    M.xticks([])
    M.yticks([])           
    
    boxsize = N.max(pos.shape[:2])
    #M.axis(boxsize*N.array([-0.2,1.2,-0.2,1.2]))
    M.axis('equal')
    
    c = N.zeros((pos.shape[0]-1,pos.shape[1]-1),dtype=N.float32)

    #plot the vertices
    if radio_mode == "Points":
        ax.scatter(pos[:,:,0].flat,pos[:,:,1].flat,s=1,lw=0)
    elif radio_mode == "Mesh":
        ax.pcolorfast(pos[:,:,0],pos[:,:,1],density[:pos.shape[0]-1,:pos.shape[1]-1],alpha=0.1,cmap=M.get_cmap('winter'),vmin = N.min(density), vmax = 1.5*N.max(density)-0.5*N.min(density))
        #ax.pcolorfast(pos[:,:,0],pos[:,:,1],c,alpha=0.1,vmin = 0.,vmax=1.)
        #M.pcolor(pos[:,:,0],pos[:,:,1],c,alpha=0.15,vmin=0.,vmax=1.)

# When the slider is changed, redraw the screen with the updated scale
def update(scale):
    global psi
    global density
    global radio_mode_physics

    if radio_mode_physics == 'Zeldovich':
        pos = psi2pos(psi*scale)
    elif radio_mode_physics == 'NoCollapse':
        pos = psi2pos(collapse(density*scale))   
        
    plotvertices(pos,scale)
    M.title('Fold Your Own Universe',fontsize=25)
    M.draw()


def sliderUpdate(val):
    global scale
    global radio_mode_physics
    global slider_scale
    scale = slider_scale.val
    update(scale)

def radioUpdate(button):
    global radio_mode
    global radio_mode_physics
    global scale
    radio_mode = button
    update(scale)

def radioUpdate_physics(button_physics):
    global radio_mode
    global radio_mode_physics
    global scale
    radio_mode_physics = button_physics
    update(scale)



scale = 1.0
slider_scale = 1.0

radio_mode = "Mesh"
radio_buttons = 1

radio_mode_physics = "Zeldovich"
radio_buttons = 1

# Sets up initial dimensions
M.figure()#figsize=(18,10))
    
if len(sys.argv) == 2:
    #density = N.loadtxt(os.path.join(sys.path[0], sys.argv[1]))        
    density = convertimage(os.path.join(sys.path[0], sys.argv[1]))
elif len(sys.argv) == 3:
    density = convertimage(os.path.join(sys.path[0], sys.argv[1]),maxres=float(sys.argv[2]))
else:
    density=N.loadtxt(os.path.join(sys.path[0], './densmesh.txt'))

density -= N.min(density)
density = density/N.mean(density) - 1.
density *= 8./N.std(density)

# Real Fourier transform of "density" 
density_k = N.fft.rfftn(density)  
psi = zeldovich(density_k)
# Zel'dovich displacement field

scale = 1.0
slider_scale = 20.0

axcolor = 'lightgoldenrodyellow'

viewaxes = [0.02, 0.05, 0.95, 0.85]

axScale = M.axes([viewaxes[0]+0.05, 0.01, viewaxes[2]-0.1, 0.03])
    
slider_scale = Slider(axScale, 'Time', 0.0, 8.0, 1.0)
slider_scale.on_changed(sliderUpdate)
#axScale.text(0.,0.,'Cosmic Growth Factor (time)',ha='left',va='bottom')

buttonwidth = 0.15
buttonAxes = M.axes([viewaxes[0]+viewaxes[2]-buttonwidth, viewaxes[1]+viewaxes[3], buttonwidth, 1-viewaxes[1]-viewaxes[3]])
radio_buttons = RadioButtons(buttonAxes, ("Mesh", "Points"))
radio_buttons.on_clicked(radioUpdate)

buttonAxes_physics = M.axes([viewaxes[0], viewaxes[1]+viewaxes[3], buttonwidth, 1-viewaxes[1]-viewaxes[3]])
radio_buttons_physics = RadioButtons(buttonAxes_physics, ("Zeldovich", "NoCollapse"))
radio_buttons_physics.on_clicked(radioUpdate_physics)

M.axes(viewaxes)
M.xticks([])
M.yticks([])        

update(scale)
M.show()
