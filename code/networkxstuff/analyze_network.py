from __future__ import division

import networkx as nx
import matplotlib.pyplot as plt
import csv

############### UTILITY FUNCTIONS ##############################################

def connect_from_Matrix(matrix):
    with open("bio_connection_matrices/celegans277/"+matrix) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        a = list(readCSV)

    for ri in range(len(a[0])):
        for ci in range(len(a[0])):
            if(a[ri][ci] != "0"):
                G.add_edge(ri,ci)

def count_simplicies(graph):
    H = graph.to_undirected()
    cliques = list(nx.find_cliques(H))
    # print(cliques)
    simplices_of_dimension = [graph.number_of_nodes(),graph.number_of_edges(),0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]       # are the really simplices_of_dimension though...?
    for i in cliques:
        if(len(i) != 0):
            simplices_of_dimension[len(i)] += 1

    return(simplices_of_dimension)


def count_directed_cliques(G):
    Gcliques = list(nx.find_cliques(G.to_undirected()))
    # print(Gcliques)
    directed_cliques_of_dimension = ["nope","nope",0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    for num in range(len(Gcliques)):
        # print(Gcliques[num])
        sub = G.subgraph(Gcliques[num])
        # print(Gcliques[num])
        if(len(list(nx.simple_cycles(sub))) == 0):
            directed_cliques_of_dimension[len(Gcliques[num])] += 1


    return(directed_cliques_of_dimension)
    # return("nothing to see here")

################################################################################

matrix = "celegans277matrix.csv"
# matrix = "macaque.csv"
print(matrix)



G = nx.DiGraph()

connect_from_Matrix(matrix)
# G.add_edges_from([[0,1],[0,2],[0,3],[0,4],[1,2],[1,3],[1,4],[2,3],[2,4],[3,4],[0,5],[5,6],[6,0]])     # just a test
# G.add_edges_from([
#                 [0,1],[0,2],[0,3],[0,4],[0,5],
#                 [1,3],[1,4],[1,5],
#                 [2,1],[2,4],[2,5],[2,6],
#                 [3,2],[3,5],
#                 [4,3],[4,5]])     # just a test

N = G.number_of_nodes()
N_syn = G.number_of_edges()


dicliques = count_directed_cliques(G)
simp = count_simplicies(G)


print("simplices/cliques whatever: ")
print(simp)
print("directed cliques: ")
print(dicliques)



for i in range(2,len(simp)):
    if(simp[i] != 0):
        print("of the " + str(simp[i]) + " " + str(i-1) + "-dimensional cliques, " + str(dicliques[i]) + " of them are directed")



########### COMPARING TO OTHER GENERATED GRAPHS #################################
#
# print("ER random graph")
#
# r_p = 0.0275               # this painfully arbitrary and only works for 277, I should figure out how to get this number nicely...
# # print(p)
# randG = nx.erdos_renyi_graph(N,r_p,None,True)
# # print(count_simplicies(randG))
#
# dicliques = count_directed_cliques(randG)
# simp = count_simplicies(randG)
# print("simplices/cliques whatever: ")
# print(simp)
# print("directed cliques: ")
# print(dicliques)
#
#
# for i in range(2,len(simp)):
#     if(simp[i] != 0):
#         print("of the " + str(simp[i]) + " " + str(i-1) + "-dimensional cliques, " + str(dicliques[i]) + " of them are directed")
# #
# #
# # # b_p = 0.0275
# # # bG = nx.binomial_graph(N,b_p,None,True)
# # # print(count_simplicies(bG))
