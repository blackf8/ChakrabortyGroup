import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import timeit
from sympy import ifft
from plot import *

def inverse_fourier_transform(matrix, matrix_dict, n_x, n_y, k_x, k_y, N_x, N_y):
    const = 1 / math.sqrt(N_x*N_y)
    new_data = []
    counter = 0
    for i in n_x:
        tmp = []
        if(counter % 10 == 0):
            print(counter)
        counter = counter + 1
        for j in n_y:
            #look through each point
            summation = 0
            for row in k_x:
                for column in k_y:
                    formula = ((2*math.pi*i*row/N_x)+(2*math.pi*j*column/N_y))
                    power = -1*formula
                    summation = summation + (math.cos(power)+complex(0,1)*math.sin(power))*matrix_dict[(row,column)]
            tmp.append(const*summation)
        new_data.append(tmp)
    return new_data

def fourier_transform(matrix, matrix_dict, n_x, n_y, k_x, k_y, N_x, N_y):
    const = 1 / math.sqrt(N_x*N_y)
    new_data = []
    for row in k_x:
        tmp = []
        for column in k_y:
            #look through each point
            summation = 0
            for i in n_x:
                for j in n_y:
                    formula = ((2*math.pi*i*row/N_x)+(2*math.pi*j*column/N_y))
                    power = formula
                    summation = summation + (math.cos(power)+complex(0,1)*math.sin(power))*matrix_dict[(i,j)]
            tmp.append(const*summation)
        new_data.append(tmp)
    return new_data

def round_2dlist(arr):
    new_arr = []
    for i in arr:
        tmp = []
        for j in i:
            tmp.append(round(j.real))
        new_arr.append(tmp)
    return new_arr

def fourier_test(matrix):
    N_x = len(matrix)
    N_y = len(matrix[0])
    n_x = range(1, N_x + 1)
    n_y = range(1, N_y + 1)
    k_x = range(N_x)
    k_y = range(N_y)
    print('Starting Inverse Fourier Transform...')
    #matrix_dict = {}
    #for i in k_x:
    #    for j in k_y:
    #        matrix_dict[(i,j)] = matrix[i][j]
    #real_matrix = inverse_fourier_transform(matrix, matrix_dict, n_x, n_y, k_x, k_y, len(matrix), len(matrix[0]))

    real_matrix = matrix #uncomment this if you want forier first, add a if statement to hav a parm that lets use dictate this behaviour
    real_matrix_dict = {}
    for i in n_x:
        for j in n_y:
            real_matrix_dict[(i,j)] = real_matrix[i-1][j-1]

    ori_matrix = fourier_transform(real_matrix, real_matrix_dict, n_x, n_y, k_x, k_y, len(real_matrix), len(real_matrix[0]))
    return ori_matrix


def sin_matrix(N,m,n):
    new_arr = np.zeros((N,N))
    x_val = 0
    y_val = 0
    for i in range(N):
        x_val = x_val + 1/N
        for j in range(N):
            y_val = y_val + 1/N
            new_arr[i][j] = math.sin((2*math.pi*m*x_val))*math.sin((2*math.pi*n*y_val))
    return new_arr



def peek_matrix(df):
    for i in range(2):
        for j in range(2):
            print(i,j,df[i][j])

def plot_3d(grid, m, n,x,y,z):
    fig = plt.figure(figsize = (12,10))
    ax = plt.axes(projection='3d')

    X = x
    Y = y
    Z = z
    #print(X.shape, Y.shape, Z.shape)
    #print(Y)
    surf = ax.plot_surface(X, Y, Z, cmap = plt.cm.cividis)

    # Set axes label
    ax.set_xlabel('x', labelpad=20)
    ax.set_ylabel('y', labelpad=20)
    ax.set_zlabel('z', labelpad=20)

    fig.colorbar(surf, shrink=0.5, aspect=8)
    plt.title('Grid Size: '+ str(grid) +' Coor: ' + str(m) + ', ' + str(n))
    plt.show()


def t():
    #Code to plot Rxx
    a = [[1,0,0],
         [0,1,0],
         [0,0,1]]

    a11 = a[0][0];
    a22 = a[1][1];
    a33 = a[2][2];
    a12 = a[0][1];
    a21 = a[1][0];
    qx = np.arange(-5,5,.1)
    qy = np.arange(-5,5,.1)
    L = 1


    #100^2 --> Time:  291.2791219
    #100^2 --> Time: 400
    #4-6 min

    #matrix = [[21,13,2], [3,46,1], [3,3,3]]

    grid = 16
    m = 4
    n = 4

    matrix = np.random.randint(-10,10,size=(100,100))
    matrix = R("xx",qx,qy,a11,a12,a21,a22,a33,L)
    matrix = sin_matrix(grid,m,n)

    #peek_matrix(matrix)
    #print(matrix)

    #main()
    start = timeit.default_timer()
    a = fourier_test(matrix)
    stop = timeit.default_timer()
    #print(len(R("xx" , qx,qy,a11,a12,a21,a22,a33,L)), len(R("xx" , qx,qy,a11,a12,a21,a22,a33,L)[0]))

    print()
    print('Time: ', stop - start)

    for i in range(len(a)):
        for j in range(len(a[0])):
            print(i,j,a[i][j].real)


    x = [list(range(len(a)))]

    plot_3d(grid,m,n,np.repeat(x,len(a),axis=0), np.repeat(x,len(a),axis=0).T, np.array(a).real)
t()


for i in range(10):
    print(i, math.sin((2*math.pi*2*(i/10))))

### Try sin function for input and test to see if it works properly
    ### in the resultant matrix there will be non
### then test on larger matrices, to see if current implementation doesnt have a long run time

#I will get an email to fill out, remember to ask to get added to bulbul's queue
#Michael: fast forier transform via python -->
