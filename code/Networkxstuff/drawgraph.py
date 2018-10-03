import networkx as nx
from networkx.drawing.nx_agraph import to_agraph
import sys
import csv
import matplotlib.pyplot as plt

matrix = sys.argv[1] + ".csv"

with open("../connection_matrices/"+matrix) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    a = list(readCSV)

G = nx.DiGraph()
for ri in range(len(a[0])):
    for ci in range(len(a[0])):
        if(a[ri][ci] != "0"):
            G.add_edge(ri,ci)


# nx.draw_kamada_kawai(G, with_labels=True, font_weight='bold')
# nx.draw_shell(G, with_labels=True, font_weight='bold')
nx.draw_kamada_kawai(G, with_labels=True)
plt.show()
