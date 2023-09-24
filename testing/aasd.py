import numpy as np


def golden(n,lim = 3*np.pi):

    #Creates a base accourding to the golden ratio spiral
    t = np.linspace(0,lim,n)
    g  = (1 + 5 ** 0.5) / 2 #golden ratio
    f = g**(t*g/(2*np.pi)) #factor
    x = np.cos(t)*f
    y = np.sin(t)*f
    return(x,y)
print(golden(11))
