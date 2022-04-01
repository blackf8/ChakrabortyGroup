import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import timeit

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

def fourier_helper(k_x, k_y, N_x, N_y, i , j, matrix):
    df_x = pd.DataFrame(columns = k_x)
    df_y = pd.DataFrame(columns = k_y)
    for row in k_x:
        tmp_x = []
        tmp_y = []
        for column in k_y:
            tmp_x.append((2*math.pi*row/N_x))
            tmp_y.append((2*math.pi*column/N_y))

        df_x = df_x.append(pd.DataFrame([tmp_x]))
        df_y = df_y.append(pd.DataFrame([tmp_y]))


    df_x = df_x.multiply(i).reset_index().drop('index', axis = 1)
    df_y = df_y.multiply(j).reset_index().drop('index', axis = 1)

    sum = df_x.add(df_y, fill_value=0)
    sum = sum.multiply(-1).to_numpy()
    val = ((np.cos(sum) + complex(0,1)*np.sin(sum))*np.array(matrix)).sum()
    return val

def inverse_fourier_transform_pd(matrix, n_x, n_y, k_x, k_y, N_x, N_y):
    const = 1 / math.sqrt(N_x*N_y)
    new_df = pd.DataFrame(columns = k_x)
    counter = 0

    for i in n_x:
        tmp = []
        for j in n_y:
            if(counter % 10 == 0):
                print(counter)
            counter = counter + 1
            #look through each point
            summation = fourier_helper(k_x, k_y, N_x, N_y, i , j, pd.DataFrame(matrix))
            tmp.append(const*summation)
        tmp = pd.DataFrame([tmp])
        new_df = new_df.append(tmp)
    return new_df.reset_index().drop('index', axis = 1)

def fourier_test_pd(matrix):
    N_x = matrix.shape[0]
    N_y = matrix.shape[1]
    n_x = range(1, N_x + 1)
    n_y = range(1, N_y + 1)
    k_x = range(N_x)
    k_y = range(N_y)
    print("Starting")
    new_df = inverse_fourier_transform_pd(matrix, n_x, n_y, k_x, k_y, N_x, N_y)
    #new_df = fourier_transform_pd(new_df, n_x, n_y, k_x, k_y, N_x, N_y)
    return new_df


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

    #matrix = [[21,13,2], [3,46,1], [3,3,3]]

    matrix = np.random.randint(-10,10,size=(3,3))
    df = pd.DataFrame(matrix)
    print(matrix)
    matrix2 = R("xx",qx,qy,a11,a12,a21,a22,a33,L)


    start1 = timeit.default_timer()
    new_df = fourier_test_pd(df)
    stop1 = timeit.default_timer()

    #main()
    #start = timeit.default_timer()
    #a = fourier_test(matrix)
    #stop = timeit.default_timer()
    #print(len(R("xx" , qx,qy,a11,a12,a21,a22,a33,L)), len(R("xx" , qx,qy,a11,a12,a21,a22,a33,L)[0]))



    print()
    print('Time: ', stop1 - start1)
    #print(new_df)
    #print('Time: ', stop - start)
    #print(a)

t()
