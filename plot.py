#!/usr/bin/env python3
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.ticker as plticker
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.lines import Line2D
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle
from scipy.interpolate import InterpolatedUnivariateSpline

my_rcParams={
    "text.usetex": True,
    "font.family": "Georgia",
    "font.size": 25,
    "lines.linewidth": 4,
    "xtick.direction": "in",
    "ytick.direction": "in",
    "xtick.minor.visible": True,
    "ytick.minor.visible": True,
    "xtick.major.size" : 12,
    "ytick.major.size" : 12,
    "xtick.minor.size" : 6,
    "ytick.minor.size" : 6,
    "axes.spines.right": False,
    "axes.spines.top" : False,
    "legend.frameon":False
}
plt.rcParams.update(my_rcParams)

def read_file(fname):
    data = []
    neta, nx, ny, dx, dy, deta = 0,0,0,0,0,0
    with open(fname,'r') as f:
        line = f.readline().split(' ')
        neta, nx, ny, deta, dx, dy = [float(e) for e in [line[1], line[3], line[5], line[7], line[9], line[11]]]
        nx, ny, neta = int(nx), int(ny), int(neta)
        data = np.zeros(shape=(nx, ny))
        integral = 0
        for i in range(nx+1):
            for j in range(ny+1):
                line = f.readline().strip('\n').split(' ')
                if len(line) < 4 : continue
                temp = float(line[3])
                integral += temp
                data[i][j] = temp
        data = np.array(data)
        data /= integral
    return data, nx, ny, dx, dy

                
data, nx, ny, dx, dy = read_file('u_field_1.dat')
xmin = -1.*nx*dx/2.
xmax = nx*dx/2.
x = np.linspace(xmin, xmax, nx)
y = np.linspace(xmin, xmax, ny)
XX, YY = np.meshgrid(x, y)

fig, ax = plt.subplots(1,1)
#fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
im      = ax.pcolormesh(XX, YY, data, cmap='inferno', rasterized=True)
#ax.plot_surface(XX, YY, data, cmap='inferno', rasterized=True)
#divider = make_axes_locatable(ax)
#cax     = divider.append_axes('right', size='5%', pad=0.03)
#cbar    = fig.colorbar(im, cax=cax, orientation='vertical')
ax.set_ylabel('y (fm)')
ax.set_xlabel('x (fm)')

ax.set_title(r'Energy Density (normalized, arb units) at $\tau=0.4$ fm/$c$')

plt.show()
