import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

G.add_node("Fortinet")
G.add_node("Switch")

G.add_edge("Fortinet", "Switch")

nx.draw(G, with_labels=True)

plt.show()