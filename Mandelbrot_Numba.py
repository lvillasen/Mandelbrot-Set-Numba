# Interactive Mandelbrot Set Accelerated with Numba
# Classical Iteration Method
# Luis Villasenor
# lvillasen@gmail.com
# 2/8/2016
# Licence: GPLv3

# Usage

# The mouse/trackpad is used to control the various modes of operation

# Point and click with the right buttom to magnify by a factor of 10

# Use the left buttom to draw a square to zoom into 

# Click with the left button on the rigth side of the 
# image at medium height to randomly change the colormap

# Click with right button on the right side of the image at 
# medium height to set the default colormap

# Click on the left side of the image at medium height 
# to reset to the full Mandelbrot set

# Click in the upper/lower left corner of the canvas 
# to increase/decrease the maximum number of iterations

# Click in the upper/lower right corner of the canvas 
# to increase/decrease the number of pixels

# Click in the upper/lower center of the canvas to 
# increase/decrease the power index of the iteration formula

import numpy as np
from pylab import cm as cm
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector
import numba  
global N,x0,y0,side,L,M,power
L=400;N=800
x0=-.5;y0=0.
side=3.0
i_cmap=49
power=2
fig = plt.figure(figsize=(12,12))
fig.suptitle('Interactive Mandelbrot Set, Accelerated with Numba')
ax = fig.add_subplot(111)
cmaps=[m for m in cm.datad if not m.endswith("_r")]
@numba.autojit
def mandelbrot(N,x0,y0,side,L,power):
    R=2.
    M = np.zeros((N,N))
    delta = side/N
    for i in range(N):
        for j in range(N):
            c = x0-side/2.+delta*i+(y0-side/2.+delta*j)*1j
            z, h = 0+0*1j, 0
            while (h<L) and (abs(z)<R):
                z = z**power+c
                h+=1  
            M[j,i]=h
    return M
def zoom_on_square(eclick, erelease):
    'eclick and erelease are the press and release events'
    global N,side,x0,y0,myobj,M,power
    x1, y1 = eclick.xdata, eclick.ydata
    x2, y2 = erelease.xdata, erelease.ydata
    #print(" The button you used were: %s %s" % (eclick.button, erelease.button))
    #print ' Nx=%d, Ny=%d, x0=%f, y0=%f'%(x1, y1, x0,y0)
    x_1=x0+side*(x1-N/2.)/N
    y_1=y0+side*(y1-N/2.)/N
    x_2=x0+side*(x2-N/2.)/N
    y_2=y0+side*(y2-N/2.)/N
    x0=(x_2+x_1)/2.
    y0=(y_2+y_1)/2.
    side=side*(x2-x1+y2-y1)/N/2 # Average of the 2 rectangle sides
    M=mandelbrot(N,x0,y0,side,L,power)
    myobj = plt.imshow(M,origin='lower',cmap=cmaps[i_cmap])
    myobj.set_data(M)
    ax.set_title('Side=%.2e, x=%.2e, y=%.2e, %s, L=%d'%(side,x0,y0,cmaps[i_cmap],L))
    plt.draw()
#def change_properties(event):
#    global N,side,x0,y0,myobj,L,M,i_cmap,power
    
zoom_on_square.RS = RectangleSelector(ax, zoom_on_square,
    drawtype='box', useblit=True,button=[1, 3],  # don't use middle button
    minspanx=5, minspany=5,spancoords='pixels',
    interactive=False)
def zoom_on_point(event):
    global N,side,x0,y0,myobj,L,M,i_cmap,power
    #print(" Button pressed: %d" % (event.button))
    #print(' event.x= %f, event.y= %f '%(event.x,event.y))
    if event.button==3 and event.inaxes: # Zoom on clicked point; new side=10% of old side
        x1, y1 = event.xdata, event.ydata
        x0=x0+side*(x1-N/2.)/N
        y0=y0+side*(y1-N/2.)/N
        side=side*.1
        M=mandelbrot(N,x0,y0,side,L,power)
        myobj = plt.imshow(M,origin='lower',cmap=cmaps[i_cmap])
        ax.set_title('Side=%.2e, x=%.2e, y=%.2e, %s, L=%d'%(side,x0,y0,cmaps[i_cmap],L))
        plt.draw()
    if not event.inaxes and event.x<.3*N and event.y>.3*N and event.y<.7*N: # Click center left side to reset to full fractal
        power=2; side=3.0; x0=-.5;y0=0.;i_cmap=49
        M=mandelbrot(N,x0,y0,side,L,power)
        myobj = plt.imshow(M,cmap=cmaps[i_cmap],origin='lower')
        ax.set_title('Side=%.2e, x=%.2e, y=%.2e, %s, L=%d'%(side,x0,y0,cmaps[i_cmap],L))
        plt.draw()
    if event.button==1 and not event.inaxes and event.x>.7*N and event.y>.3*N and event.y<.7*N: # Left click center right side to set a random colormap
        i_cmap_current=i_cmap
        i_cmap=np.random.randint(len(cmaps))
        if i_cmap==i_cmap_current:
            i_cmap-=1
            if i_cmap< 0 : i_cmap=len(cmaps)-1
        #print("color=",i_cmap) 
        myobj = plt.imshow(M,origin='lower',cmap=cmaps[i_cmap])
        ax.set_title('Side=%.2e, x=%.2e, y=%.2e, %s, L=%d'%(side,x0,y0,cmaps[i_cmap],L))
        plt.draw() 
    if event.button==3 and not event.inaxes and event.x>.7*N and event.y>.3*N and event.y<.7*N: # Right click center right side to set mapolormap='flag' 
        i_cmap=49
        myobj = plt.imshow(M,origin='lower',cmap=cmaps[i_cmap])
        ax.set_title('Side=%.2e, x=%.2e, y=%.2e, %s, L=%d'%(side,x0,y0,cmaps[i_cmap],L))
        plt.draw() 
    if not event.inaxes and event.x>.7*N and event.y>.7*N: # Increase max number of iterations
        L=int(L*1.2);
        M=mandelbrot(N,x0,y0,side,L,power)
        myobj = plt.imshow(M,cmap=cmaps[i_cmap],origin='lower')
        ax.set_title('Side=%.2e, x=%.2e, y=%.2e, %s, L=%d'%(side,x0,y0,cmaps[i_cmap],L))
        plt.draw()
    if not event.inaxes and event.x>.7*N and event.y<.3*N: # Decrease max number of iterations
        L=int(L/1.2);
        M=mandelbrot(N,x0,y0,side,L,power)
        myobj = plt.imshow(M,cmap=cmaps[i_cmap],origin='lower')
        ax.set_title('Side=%.2e, x=%.2e, y=%.2e, %s, L=%d'%(side,x0,y0,cmaps[i_cmap],L))
        plt.draw()

    if not event.inaxes and event.x<.3*N and event.y>.7*N: # Increase number of pixels
        N=int(N*1.2);
        M=mandelbrot(N,x0,y0,side,L,power)
        myobj = plt.imshow(M,cmap=cmaps[i_cmap],origin='lower')
        ax.set_title('Side=%.2e, x=%.2e, y=%.2e, %s, L=%d'%(side,x0,y0,cmaps[i_cmap],L))
        plt.draw()
    
    if not event.inaxes and event.x<.3*N and event.y<.3*N: # Decrease number of pixels
        N=int(N/1.2);
        M=mandelbrot(N,x0,y0,side,L,power)
        myobj = plt.imshow(M,cmap=cmaps[i_cmap],origin='lower')
        ax.set_title('Side=%.2e, x=%.2e, y=%.2e, %s, L=%d'%(side,x0,y0,cmaps[i_cmap],L))
        plt.draw()
    
    if not event.inaxes and event.y>.7*N and event.x<.7*N and event.x>.3* N: # Increase power index by 1
        if power <9 : 
            power += 1
        else: 
            power=2
        print("Power index set to %d" % power)
        i_cmap=49
        side=3.0; x0=-.5;y0=0.;L=200;
        M=mandelbrot(N,x0,y0,side,L,power)
        myobj = plt.imshow(M,cmap=cmaps[i_cmap],origin='lower')
        ax.set_title('Side=%.2e, x=%.2e, y=%.2e, %s, L=%d'%(side,x0,y0,cmaps[i_cmap],L))
        plt.draw()
    if not event.inaxes and event.y<.3*N and event.x<.7*N and event.x>.3* N: # Decrease power index by 1
        if power > 1 : 
            power -= 1
        else: 
            power=2
        print("Power index set to %d" % power)
        i_cmap=49
        side=3.0; x0=-.5;y0=0.;L=200;
        M=mandelbrot(N,x0,y0,side,L,power)
        myobj = plt.imshow(M,cmap=cmaps[i_cmap],origin='lower')
        ax.set_title('Side=%.2e, x=%.2e, y=%.2e, %s, L=%d'%(side,x0,y0,cmaps[i_cmap],L))
        plt.draw()
cid = fig.canvas.mpl_connect('button_press_event', zoom_on_point)
plt.connect('key_press_event', zoom_on_square)
M=mandelbrot(N,x0,y0,side,L,power)
ax.set_title('Side=%.2e, x=%.2e, y=%.2e, %s, L=%d'%(side,x0,y0,cmaps[i_cmap],L))
plt.imshow(M,origin='lower',cmap=cmaps[i_cmap])


