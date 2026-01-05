import networkx as nx
import matplotlib.pyplot as plt
import csv

graph = []
with open('grafo_25nos.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        graph.append([int(x) for x in row])

N = len(graph)

G = nx.Graph()
for i in range(N):
    G.add_node(i)
    for j in range(i+1, N):
        if graph[i][j]:
            G.add_edge(i, j)


colors = []
with open('coresguloso.txt') as f:
    for line in f:
        colors.append(int(line.strip()))

color_map = ['red','green','blue','yellow','orange','purple','cyan','pink']
node_colors = [color_map[(c-1) % len(color_map)] for c in colors]

plt.figure(figsize=(10,10))
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=700, font_size=10)
plt.show()
