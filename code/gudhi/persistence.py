import csv
import networkx as nx
import sys
sys.path.append('/home/mark/gudhi/build/cython')
import gudhi

def csv_to_graph(matrix):
    G = nx.DiGraph()

    with open("connection_matrices/"+matrix) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        a = list(readCSV)

    for ri in range(len(a[0])):
        for ci in range(len(a[0])):
            if(a[ri][ci] != "0"):
                G.add_edge(ri,ci)

    return(G)


def graph_to_sc(graph):

    for ri in range(len(graph.edges())):
        for ci in range(len(graph.edges())):
            if(graph.has_edge(ri,ci)):
                st.insert([ri,ci])

    cliques = list(nx.find_cliques(G.to_undirected()))
    for i in cliques:
        st.insert(i)

################################################################################

matrix = "celegans131matrix.csv"

rc = gudhi.RipsComplex()
# st = rc.create_simplex_tree()

st = gudhi.SimplexTree()

G = csv_to_graph(matrix)
# print(G.edges())
# print(list(nx.find_cliques(G.to_undirected())))

graph_to_sc(G)

print(st.num_vertices(), st.num_simplices())           # yay, this matches neurotop's output!



p = st.persistence()
gudhi.plot_persistence_diagram(p,0.5)


# print(st.get_skeleton(3))      # ugh, I guess I need to make all the cliques into simplices..
# gudhi.show_palette_values(1)
