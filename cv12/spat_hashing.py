from math import *
from time import *
from matplotlib.pyplot import *
from numpy import * 

def loadPoints(file):
    #Load file
    X, Y, Z = [], [], [] ;
    
    with open(file) as f:
        
        for line in f:
            x, y, z = line.split('\t')
            
            X.append(float(x))
            Y.append(float(y))
            Z.append(float(z))
    
    return X, Y, Z

def  getNN(xq, yq, zq, X, Y, Z):
    #Find nearest point and its distance
    dmin = inf
    xn, yn, zn = X[0], Y[0], Z[0]
    
    for i in range(len(X)):
        #Compute distance
        dx, dy, dz = xq - X[i], yq - Y[i], zq - Z[i]
        d = (dx*dx + dy*dy + dz * dz)**0.5
        
        #Actualize minimum: distance + coordinates
        if d < dmin:
            dmin = d
            xn, yn, zn = X[i], Y[i], Z[i]
    return xn, yn, zn, dmin

def drawPoints(X, Y, Z, bx):
    # Create figure
    fig = figure()
    ax = axes(projection = '3d')
    ax.set_aspect('equal')

    #Compute sphere scale: 1 pix = 25.4 mm
    scale = 1
    if bx > 0:
        scale = int(bx * bx * 40 * 40)
        
    #Plot points
    ax.scatter(X, Y, Z, s=scale, alpha = 0.2)

    show()