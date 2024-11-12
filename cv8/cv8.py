from math import *
from queue import *

#Graph 1, Dijkstra
G = {
    1 : {2:8, 3:4, 5:2},
    2 : {1:8, 3:5, 4:2, 7:6, 8:7},
    3 : {1:4, 2:5, 6:3, 7:4},
    4 : {2:2, 9:3},
    5 : {1:2, 6:5},
    6 : {3:3, 5:5, 7:5, 8:7, 9:10},
    7 : {2:6, 3:4, 6:5, 8:3},
    8 : {2:7, 6:7, 7:3, 9:1},
    9 : {4:3, 6:10, 8:1}
}

#Graph 2, kruskal
V = [1, 2, 3, 4, 5, 6, 7, 8, 9]

E = [
    [1, 2, 8], 
    [1, 3, 4], 
    [1, 5, 2], 
    [2, 1, 8], 
    [2, 3, 5], 
    [2, 4, 2], 
    [2, 7, 6], 
    [2, 8, 7], 
    [3, 1, 4],  
    [3, 2, 5], 
    [3, 6, 3], 
    [3, 7, 4], 
    [4, 2, 2], 
    [4, 9, 3], 
    [5, 1, 2], 
    [5, 6, 5], 
    [6, 3, 3], 
    [6, 5, 5], 
    [6, 7, 5], 
    [6, 8, 7], 
    [6, 9, 10], 
    [7, 2, 6], 
    [7, 3, 4], 
    [7, 6, 5], 
    [7, 8, 3], 
    [8, 2, 7], 
    [8, 6, 7], 
    [8, 7, 3], 
    [8, 9, 1], 
    [9, 4, 3], 
    [9, 6, 10], 
    [9, 8, 1]
    ]

def rec(u,v,P):
    path = []
    
    # Path shortening
    while v != u and v !=-1:
        path.append(v)
        v = P[v]
        
    path.append(v)
    if v != u:
        print('Incorrect path')
    return (path)

def dijkstra(G, u, v):
    #Input data structures
    n = len(G)
    P = [-1]*(n+1)
    D = [inf]*(n+1)
    PQ = PriorityQueue()
    
    # Starting node, add to PQ
    PQ.put((0,u))
    D[u] = 0
    
    #Until PQ is empty
    while not PQ.empty():
        
        #Remove node u with the lowest D[u] estimation
        du,u = PQ.get()
        
        #Iterate through neighbours
        for v, wuv in G[u].items():
        
            # Edge relaxation: path to v through u is better
            if D[v] > D[u] + wuv:
                
                #Actualize D[v] estimation
                D[v] = D[u] + wuv
                
                #Store v predecessor (u)
                P[v] = u
                
                #Add v to PQ
                PQ.put((D[v],v))
                
    return P, D[v]

def find(u,P):
    # find parent node for u
    while P[u] != u:
        #Traverse to predecessor
        u = P[u]
        
    return u

def union(u,v,P):
    #Union-Find
    
    #Find root node for u
    root_u = find(u,P)
    
    #Find root node for v
    root_v = find(v,P)
    
    #Union: connect rv to ru
    if root_u != root_v:
        P[root_v] = root_u
        
def make_set(u,P):
    #Init all trees
    P[u] = u

def min_span_tree(V, E):
    #MInimum spanning tree (Boruvka's method)
    T = []  # tree
    wt = 0  # line weight
    n = len(V)
    P = [-1]*(n+1)
    
    #Initialize trees
    for v in V:
        make_set(v,P)

    #Sort edges
    ES = sorted(E, key=lambda it:it[2])
    
    #Process sorted edges
    for e in ES:
        
        #Get edge
        u, v, w = e
        
        #Find root node for u
        root_u = find(u,P)
        
        #Find root node for v
        root_v = find(v,P)
        
        #Union
        if root_u != root_v:
            
            #Connect rv to ru
            P[root_v] = root_u
            
            #Add e to T
            T.append(e)
            
            #Update weight of T
            wt = wt + w
        
    return T, wt

#Dijkstra
P, dmin = dijkstra(G,1,9)
    
#Backward path reconstruction
path = rec(1, 9, P)
print(path, dmin)

#Boruvka MST
T, wt = min_span_tree(V, E)
print(T, wt)



