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

def getNN(xq, yq, zq, X, Y, Z):
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

def drawPoints(X, Y, Z, bx, transp = 0.2):
    # Create figure
    fig = figure()
    ax = axes(projection = '3d')
    ax.set_aspect('equal')

    #Compute sphere scale: 1 pix = 25.4 mm
    scale = 1
    if bx > 0:
        scale = int(bx * bx * 40 * 40)
        
    #Plot points
    ax.scatter(X, Y, Z, s=scale, alpha = transp)

    show()
    
def initIndex(X, Y, Z, n_r):
    #Initialize 3D index
    xmin = min(X)
    ymin = min(Y)
    zmin = min(Z)
    
    xmax = max(X)
    ymax = max(Y)
    zmax = max(Z)
    
    dx = xmax - xmin
    dy = ymax - ymin
    dz = zmax - zmin
    
    bx = dx/n_r
    by = dy/n_r
    bz = dz/n_r
    
    return xmin, ymin, zmin, dx, dy, dz, bx, by, bz

def get3DIndex(x, y, z, xmin, ymin, zmin, dx, dy, dz, n_r):
    #Get 3D index of a point [x, y, z]
    xr = (x - xmin)/dx
    yr = (y - ymin)/dy
    zr = (z - zmin)/dz
    
    #Compute 3D index
    c = 0.99
    jx = int(xr * n_r * c)
    jy = int(yr * n_r * c)
    jz = int(zr * n_r * c)
    
    #Query point outside the grid
    if (xr < 0 or xr > 1) or (yr < 0 or yr > 1) or (zr < 0 or zr > 1):
        return -1, -1, -1
    
    return jx, jy, jz

def hash(jx, jy, jz, n_r):
    # Convert 3D index to 1D
    return jx+jy*n_r+jz*n_r**2

def voxelize(X, Y, Z, xmin, ymin, zmin, dx, dy, dz, bx, by, bz, n_r):
    # Voxelization of point cloud
    VI = zeros((n_r, n_r, n_r))
    
    #Process all points
    for i in range(len(X)):
        
        # Get 3D Index
        jx, jy, jz = get3DIndex(X[i], Y[i], Z[i], xmin, ymin, zmin, dx, dy, dz, n_r)
        
        #Mark voxel [jx][jy][jz] as used
        VI[jx][jy][jz] = 1
        
    #List of voxels centroids
    VX, VY, VZ = [],[],[]
    
    #Process all voxels
    for i in range(n_r):
        for j in range(n_r):
            for k in range(n_r):
                
                #Is voxel [i][j][k] used
                if VI[i][j][k]:
                    VX.append(xmin + bx*i + bx/2)
                    VY.append(ymin + by*j + by/2)
                    VZ.append(zmin + bz*k + bz/2)
                    
    return VX, VY, VZ
    
#Load points
#X, Y, Z = loadPoints('s:/K155/Public/155YGEI/cv12/tree_18.txt')
X, Y, Z = loadPoints('tree_18.txt')

#Draw points
drawPoints(X, Y, Z, 0, 0.2)

#Initialization, number of points, bins, bins per a column
n = len(X)
n_bin = n**(1/3)
n_r = int(n_bin**(1/3))
print(n_r)
n_r = 2

#Initialize 3D index
xmin, ymin, zmin, dx, dy, dz, bx, by, bz = initIndex(X, Y, Z, n_r)

#Test query point
xq, yq, zq = 55, 570, 470
jx, jy, jz = get3DIndex(xq, yq, zq, xmin, ymin, zmin, dx, dy, dz, n_r)
print(jx, jy, jz)
h = hash(jx, jy, jz, n_r)
print(h)

#Voxelization
VX, VY, VZ = voxelize(X, Y, Z, xmin, ymin, zmin, dx, dy, dz, bx, by, bz, n_r)

#Draw points
drawPoints(VX, VY, VZ, (bx + by + bz)/3)
#drawPoints(VX, VY, VZ, 0.1, 1)
#print(bx, by, bz) 


                    
                
    