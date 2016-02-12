# Interactive Mandelbrot Set Accelerated using Numba
# Classical Iteration Method
# Luis Villasenor
# lvillasen@gmail.com
# 2/8/2016
# Licence: GPLv3

# Usage

# Use the left buttom to draw a square to zoom into 

# Point and click with the right buttom to magnify by a factor of 10

# Click with the left button on the rigth side of the 
# image to randomly change the colormap

# Click with right button on the right side of the image to set the default colormap

# Click on the left side of the image to restart with the full Mandelbrot set

# Press the up/down arrow to increase/decrease the maximum number of iterations

# Press the right/left arrow to increase/decrease the number of pixels

# Type a number from 1-9 to set power index of the iteration formula

# Type 'f' to toggle full-screen mode

# Type 's' to save the image

import numpy as np
from pylab import cm as cm
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector
from matplotlib.patches import Rectangle
import numba  
global N,x0,y0,side,L,M,power
L=400;N=800
x0=-.5;y0=0.
side=3.0
i_cmap=49
power=2
fig = plt.figure(figsize=(12,12))
fig.suptitle('Interactive Mandelbrot Set Accelerated using Numba')
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
    x1, y1 = min(eclick.xdata,erelease.xdata),min( eclick.ydata,erelease.ydata)
    x2, y2 = max(eclick.xdata,erelease.xdata),max( eclick.ydata,erelease.ydata)
    #print(" The button you used were: %s %s" % (eclick.button, erelease.button))
    #print ' Nx=%d, Ny=%d, x0=%f, y0=%f'%(x1, y1, x0,y0)
    #print ' Nx=%d, Ny=%d, x0=%f, y0=%f'%(x2, y2, x0,y0)
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
    ax.add_patch(Rectangle((1 - .1, 1 - .1), 0.2, 0.2,alpha=1, facecolor='none',fill=None, ))
    ax.set_title('Side=%.2e, x=%.2e, y=%.2e, %s, L=%d'%(side,x0,y0,cmaps[i_cmap],L))
    plt.draw()

def key_selector(event):
    global N,side,x0,y0,myobj,M,power,L,i_cmap
    #print(' Key pressed.')
    if event.key == u'up':  # Increase max number of iterations
        L=int(L*1.2);
        M=mandelbrot(N,x0,y0,side,L,power)
        myobj = plt.imshow(M,cmap=cmaps[i_cmap],origin='lower')
        ax.set_title('Side=%.2e, x=%.2e, y=%.2e, %s, L=%d'%(side,x0,y0,cmaps[i_cmap],L))
        plt.draw()
    if event.key == u'down':  # Decrease max number of iterations
        L=int(L/1.2);
        M=mandelbrot(N,x0,y0,side,L,power)
        myobj = plt.imshow(M,cmap=cmaps[i_cmap],origin='lower')
        ax.set_title('Side=%.2e, x=%.2e, y=%.2e, %s, L=%d'%(side,x0,y0,cmaps[i_cmap],L))
        plt.draw()
    if event.key == u'right':  # Increase  number of pixels
        N=int(N*1.2);
        M=mandelbrot(N,x0,y0,side,L,power)
        myobj = plt.imshow(M,cmap=cmaps[i_cmap],origin='lower')
        ax.set_title('Side=%.2e, x=%.2e, y=%.2e, %s, L=%d'%(side,x0,y0,cmaps[i_cmap],L))
        plt.draw()
    if event.key == u'left':  # Decrease  number of pixels
        N=int(N/1.2);
        M=mandelbrot(N,x0,y0,side,L,power)
        myobj = plt.imshow(M,cmap=cmaps[i_cmap],origin='lower')
        ax.set_title('Side=%.2e, x=%.2e, y=%.2e, %s, L=%d'%(side,x0,y0,cmaps[i_cmap],L))
        plt.draw()
    if event.key in ['1','2','3','4','5','6','7','8','9'] :  # Decrease  number of pixels
        power=int(event.key)
        if power <10 and power >0 : 
            print("Power index set to %d" % power)
            i_cmap=49
            side=3.0; x0=-.5;y0=0.;L=200;
            M=mandelbrot(N,x0,y0,side,L,power)
            myobj = plt.imshow(M,cmap=cmaps[i_cmap],origin='lower')
            ax.set_title('Side=%.2e, x=%.2e, y=%.2e, %s, L=%d'%(side,x0,y0,cmaps[i_cmap],L))
            plt.draw()

key_selector.RS = RectangleSelector(ax, zoom_on_square,
                                       drawtype='box', useblit=True,
                                       button=[1, 3],  # don't use middle button
                                       minspanx=5, minspany=5,
                                       spancoords='pixels')
#                                     interactive=False)
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
    if not event.inaxes and event.x<.3*N : # Click on left side of image to reset to full fractal
        power=2; side=3.0; x0=-.5;y0=0.;i_cmap=49
        M=mandelbrot(N,x0,y0,side,L,power)
        myobj = plt.imshow(M,cmap=cmaps[i_cmap],origin='lower')
        ax.set_title('Side=%.2e, x=%.2e, y=%.2e, %s, L=%d'%(side,x0,y0,cmaps[i_cmap],L))
        plt.draw()
    if event.button==1 and not event.inaxes and event.x>.7*N : # Left click on right side of image to set a random colormap
        i_cmap_current=i_cmap
        i_cmap=np.random.randint(len(cmaps))
        if i_cmap==i_cmap_current:
            i_cmap-=1
            if i_cmap< 0 : i_cmap=len(cmaps)-1
        #print("color=",i_cmap) 
        myobj = plt.imshow(M,origin='lower',cmap=cmaps[i_cmap])
        ax.set_title('Side=%.2e, x=%.2e, y=%.2e, %s, L=%d'%(side,x0,y0,cmaps[i_cmap],L))
        plt.draw() 
    if event.button==3 and not event.inaxes and event.x>.7*N : # Right click on right side to set mapolormap='flag' 
        i_cmap=49
        myobj = plt.imshow(M,origin='lower',cmap=cmaps[i_cmap])
        ax.set_title('Side=%.2e, x=%.2e, y=%.2e, %s, L=%d'%(side,x0,y0,cmaps[i_cmap],L))
        plt.draw()   
fig.canvas.mpl_connect('button_press_event', zoom_on_point)
fig.canvas.mpl_connect('key_press_event', key_selector)
M=mandelbrot(N,x0,y0,side,L,power)
ax.set_title('Side=%.2e, x=%.2e, y=%.2e, %s, L=%d'%(side,x0,y0,cmaps[i_cmap],L))
plt.imshow(M,origin='lower',cmap=cmaps[i_cmap])
plt.show()

