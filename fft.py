from math import log2, e, pi, sin, cos
import numpy as np

def fft(T: list):
    t = [T[len(T) - i - 1] for i in range(len(T))]
    
    for s in range(1, int(log2(len(T))) + 1):
        m = 2**s
        Wm = e**(-2j*pi/m)
        
        for k in range(0, len(T), m):
            W = 1

            for j in range(0, m // 2):
                v = W * t[k + j + m // 2]
                u = t[k + j]
                t[k + j] = u + v
                t[k + j + m // 2] = u - v
                W *= Wm

    return [x/len(T) for x in t]


def dft(T: list):
    return [sum([T[n]*(cos(2*pi * k * n / len(T)) -1j * sin(2*pi * k * n / len(T))) for n in range(len(T))])/len(T) for k in range(len(T))]

def fftrec(x):
    N = len(x)
    
    if N == 1:
        return x
    else:
        X_even = fftrec(x[::2])
        X_odd = fftrec(x[1::2])
        factor = np.exp(-2j*np.pi*np.arange(N)/ N)
        
        X = np.concatenate([X_even+factor[:int(N/2)]*X_odd,X_even+factor[int(N/2):]*X_odd])

        return X