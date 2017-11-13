import networkx as nx


G=nx.DiGraph()
G.add_edges_from([ [0,1],[1,0],[1,2],[2,3] ])

Gcliques = list(nx.find_cliques(G.to_undirected()))


print(list(nx.simple_cycles(G)))
