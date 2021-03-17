from mpl_toolkits import mplot3d
import numpy as np
import math
import matplotlib.pyplot as plt


def f1(x, y):
    return (-x**2 - y**2 + 2*x*y)


def f(x, y):
    return ( -np.sqrt((x-y)**2+0.1))


x = np.linspace(-1, 1, 30)
y = np.linspace(-1, 1, 30)

X, Y = np.meshgrid(x, y)
Z = f(X, Y)

# dx = 1
# dy = -1

#dx + dy = 0
#dx - dy = -x-y

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.contour3D(X, Y, Z, 300, cmap='binary')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

fig.show()
input()