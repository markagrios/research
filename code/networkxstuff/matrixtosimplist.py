import networkx as nx
import numpy as np
import csv

# with open("connection_matrices/"+matrix) as csvfile:
matrix = "fivecyclewithacross.csv"
with open(matrix) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    a = list(readCSV)

for ri in range(len(a[0])):
    for ci in range(len(a[0])):
        if(a[ri][ci] != "0"):
            print(ri,ci)
