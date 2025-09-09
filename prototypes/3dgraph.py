import networkx as nx
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Example graph
G = nx.Graph()
G.add_edges_from([(0, 1), (0, 2), (1, 2), (2, 3)])

# Random 3D positions
pos = {node: np.random.rand(3) for node in G.nodes()}

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Draw nodes
for node, (x, y, z) in pos.items():
    ax.scatter(x, y, z, s=100, c="blue")
    ax.text(x, y, z, str(node), color="black")

# Draw edges
for u, v in G.edges():
    x = [pos[u][0], pos[v][0]]
    y = [pos[u][1], pos[v][1]]
    z = [pos[u][2], pos[v][2]]
    ax.plot(x, y, z, c="gray")

plt.show()