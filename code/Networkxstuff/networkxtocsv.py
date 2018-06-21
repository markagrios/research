from __future__ import division

import networkx as nx
import matplotlib.pyplot as plt
import csv

N=277

print("binomial random graph")

# r_p = 0.028               # this painfully arbitrary and only works for 277, I should figure out how to get this number nicely...
# # print(p)
# randG = nx.erdos_renyi_graph(N,r_p,None,True)
# # print(count_simplicies(randG))
# # print(nx.adjacency_matrix(randG))
# # print(randG.edges())
# print(len(randG.edges()))

b_p = 0.028
bG = nx.binomial_graph(N,b_p,None,True)

print(len(bG.edges()))


with open('binrand131.csv', 'wb') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for i in range(N):
        x = ""
        for j in range(N):
            if(bG.has_edge(i,j)):
                x+=str(1)
            else:
                x+=str(0)

        filewriter.writerow(x)
