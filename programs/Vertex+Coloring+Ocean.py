
# coding: utf-8

# In[63]:


# Import the library
import matplotlib.pyplot as plt
import networkx as nx

import dwave_qbsolv
# Set the graph configuration by setting nodes and neighbours 
nodes=[0,1,2,3,4] 
neighbours=[(0,4),(1,2),(1,3),(1,4)] 
# Turn the two dimension index to one dimension
def d2tod1(n, k, K):  
 return n * K + k  
pallete = {0: 'r', 1: 'c', 2:'m', 3:'y'}
# Function to color the final configuration
def get_color(n, sol, K): 
 z = d2tod1(n, 0, K) 
 k = 0 
 for k in range(K): 
  if sol[z + k]==1: 
   break 
 return pallete[k] 
# Construct the quadratic equation
N = 5 
K = 4
qubo = BinaryQuadraticModel.empty(dimod.BINARY)
for n in range(N): 
 qubo.add_offset(1) 
 for k1 in range(K):
    for k2 in range(K):
        if k1!=k2:
            qubo.add_interaction(d2tod1(n,k1,K),d2tod1(n,k2,K),1)
 for k in range(K):
   qubo.add_variable(d2tod1(n,k,K),-1)  
for (u,v) in neighbours:
    for k in range(K): 
        qubo.add_interaction(d2tod1(u,k,K), d2tod1(v,k,K),1)
print(qubo) 
# Set up the solver
sampler = dimod.SimulatedAnnealingSampler()
solver = dwave_qbsolv.QBSolv()
# Solve for the minimum energy configuration
response=solver.sample(qubo,num_reads=300)
sol=list(response.samples())
# Draw the final coloring configuration
# Multiple possible minimum configurations are given as the output, here we take one of them to draw the graph
s=sol[0]
print(s)
g=nx.Graph() 
g.add_nodes_from(nodes) 
g.add_edges_from(neighbours) 
pos = nx.spring_layout(g) 
nx.draw(g, pos=pos, with_labels=True, nodelist=nodes,  
node_color=[get_color(n,s,K) for n in nodes],node_size=1000) 
plt.show() 

