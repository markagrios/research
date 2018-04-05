import networkx as nx
import numpy as np
import math
import csv
import matplotlib.pyplot as plt
import sys
sys.path.append('/home/mark/gudhi/build/cython')
import gudhi

def raiseton(matrix,n):
    return np.linalg.matrix_power(matrix,n)

def takeminpaths(matrix1,matrix2):     # creates a new matrix by taking the min of each entry of two matrices
    newmatrix = matrix1

    for i in range(len(matrix1[0])):
        for j in range(len(matrix1[0])):
            newmatrix[i][j] = min(matrix1[i][j],matrix2[i][j])

    return newmatrix

def getnextpower(matrix):
    # iterate through to some number and then add to array to get sequence of min path length matrices
    return mywilltolive

M = []

reader = csv.reader(open("test.csv", "rb"), delimiter=",")
x = list(reader)
M.append(np.array(x).astype("int"))

# print("matrix is:")
# print(M[0])
#
# print("matrix squared:")
# print(np.matmul(M[0],M[0]))
#
# print("function trying to raise it to 2:")
# print(raiseton(M[0],2))

a = [[1, 6], [9, 1]]
b = [[4, 2], [21, 2]]
print(takeminpaths(a,b))
