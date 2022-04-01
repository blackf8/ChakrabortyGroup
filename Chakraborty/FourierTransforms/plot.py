import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import timeit
from sympy import ifft

def rxx(i, j, a11,a12,a21,a22,a33, sined):
    return i*(a11*a33*(i**2) + (2*a11*a22 - a12*(2*a21+a33))*(j**2))*sined
def rxy(i, j, a11,a12,a21,a22,a33, sined):
    return a33*j*(a22*(j**2) - a21*(i**2))*sined
def ryy(i, j, a11,a12,a21,a22,a33, sined):
    return a33*i*(a21*(i**2) - a22*(j**2))*sined

def R(Rtype, qx,qy,a11,a12,a21,a22,a33,L):
    data = []
    for j in qy:
        temp = []
        for i in qx:
            sined = math.sin(L*i)
            numerator = {"xx": rxx(i, j, a11,a12,a21,a22,a33, sined),
                      "xy": rxy(i, j, a11,a12,a21,a22,a33, sined),
                      "yy": ryy(i, j, a11,a12,a21,a22,a33, sined)}[Rtype]
            denominator = (a11*a33*(i**4) - (2*a12*a21 - 2*a11*a22 + (a12 + a21)*a33)*i**2*j**2 + a22*a33*j**4)
            temp.append((numerator/denominator)*-1)
        data.append(temp)
    return data

def make_range(min_val, max_val, div):
    tmp = min_val
    width = (max_val-min_val)/div
    arr = []
    while(tmp < max_val):
        arr.append(tmp)
        tmp = tmp + div
    return arr

def main():
    #Code to plot Rxx
    a = [[1,0,0],
         [0,1,0],
         [0,0,1]]

    a11 = a[0][0];
    a22 = a[1][1];
    a33 = a[2][2];
    a12 = a[0][1];
    a21 = a[1][0];
    qx = np.arange(-5,5,.01)
    qy = np.arange(-5,5,.01)
    L = 1
    data = R("xx" , qx,qy,a11,a12,a21,a22,a33,L)
    min_val = np.min(data)
    max_val = np.max(data)
    ranged = make_range(min_val, max_val, .01)

    #Testi  ng contour plots
    cs = plt.contourf(data, levels=ranged, extend='both')
    cs.changed()
    plt.colorbar()
    plt.show()
    plt.close()
