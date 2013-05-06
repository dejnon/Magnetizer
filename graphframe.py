import numpy
import pylab
from matplotlib.widgets import Slider

data = numpy.random.rand(100,256,256) #3d-array with 100 frames 256x256

ax = pylab.subplot(111)
pylab.subplots_adjust(left=0.25, bottom=0.25)

frame = 0
l = pylab.imshow(data[frame,:,:]) #shows 256x256 image, i.e. 0th frame

axcolor = 'lightgoldenrodyellow'
axframe = pylab.axes([0.25, 0.1, 0.65, 0.03], axisbg=axcolor)
sframe = Slider(axframe, 'Frame', 0, 100, valinit=0)

def update(val):
    frame = numpy.around(sframe.val)
    l.set_data(data[frame,:,:])

sframe.on_changed(update)

pylab.show()


from scipy import *
from scipy.special import jn, jn_zeros
def drumhead_height(n, k, distance, angle, t):
    nth_zero = jn_zeros(n, k)
    return cos(t)*cos(n*angle)*\
        jn(n, distance*nth_zero)

theta = r_[0:2*pi:50j]
radius = r_[0:1:50j]
x = array([r*cos(theta) for r in radius])
y = array([r*sin(theta) for r in radius])
z = array([drumhead_height(1, 1, r, theta, 0.5) \
    for r in radius])

import pylab
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
fig = pylab.figure()
ax = Axes3D(fig)
ax.plot_surface(x, y, z, \
    rstride=1, cstride=1, cmap=cm.jet)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
pylab.show()
