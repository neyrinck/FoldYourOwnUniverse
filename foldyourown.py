import numpy as N, pylab as M

def init():
    d=N.loadtxt('/Users/neyrinck/plog/densmesh.txt')
    dk = N.fft.rfftn(d*1e3)
    
    return dk

def zeldovich(dk,boxsize=None):
    sk = dk.shape
    ng = sk[0]
    kx = N.fromfunction(lambda x,y:x, sk).astype(N.float32)
    kx[N.where(kx > ng/2)] -= ng
    ky = N.fromfunction(lambda x,y:y, sk).astype(N.float32)
    ky[N.where(ky > ng/2)] -= ng

    k2 = kx*kx + ky*ky
    k2[0,0] = 1.
    kx /= k2
    ky /= k2
    pos = N.empty((ng,ng,2),dtype=N.float32)

    x=boxsize/ng*N.fromfunction(lambda x,y:x, (ng,ng))
    #Inverse divergence; then displacement -> position
    pos[:,:,0] = N.fft.irfftn(-1j*dk*kx) + x
    pos[:,:,1] = N.fft.irfftn(-1j*dk*ky) + x.swapaxes(0,1)
    return pos

def psi2pos(psi,boxsize=500.):
    x=boxsize/ng*N.fromfunction(lambda x,y:x, (ng,ng))
    pos = 1.*psi
    pos[:,:,0] += x
    pos[:,:,1] += N.transpose(x)

def invdiv(dk,boxsize=None):
    sk = dk.shape
    ng = sk[0]
    kx = N.fromfunction(lambda x,y:x, sk).astype(N.float32)
    kx[N.where(kx > ng/2)] -= ng
    ky = N.fromfunction(lambda x,y:y, sk).astype(N.float32)
    ky[N.where(ky > ng/2)] -= ng

    k2 = kx*kx + ky*ky
    k2[0,0] = 1.
    kx /= k2
    ky /= k2
    pos = N.empty((ng,ng,2),dtype=N.float32)

    x=boxsize/ng*N.fromfunction(lambda x,y:x, (ng,ng))
    #Inverse divergence; then displacement -> position
    pos[:,:,0] = N.fft.irfftn(-1j*dk*kx) + x
    pos[:,:,1] = N.fft.irfftn(-1j*dk*ky) + x.swapaxes(0,1)
    return pos

def plotvertices(dk,scale=1.):
    pos = invdiv(dk*scale,boxsize=500.)
    
    M.scatter(pos[:,:,0].flat,pos[:,:,1].flat,s=1,lw=0)

