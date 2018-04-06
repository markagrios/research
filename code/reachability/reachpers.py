import networkx as nx
import numpy as np
import math
import csv
import matplotlib.pyplot as plt
import sys
sys.path.append('/home/mark/gudhi/build/cython')
import gudhi

# NEED TO MAKE FUNCTION THAT CONVERTS MATRIX TO SYMMETRIC !!!!!!!!!!!!!!!!!

def raiseton(matrix,n):
    Nmatrix = np.linalg.matrix_power(matrix,n)
    for i in range(len(Nmatrix[0])):
        Nmatrix[i][i] = 0

    for i in range(len(matrix[0])):
        for j in range(len(matrix[0])):
            if(Nmatrix[i][j] > 0):
                Nmatrix[i][j] = n

    return Nmatrix

def takeminpaths(matrix1,matrix2):     # creates a new matrix by taking the min of each entry of two matrices
    newmatrix = matrix1
    for i in range(len(matrix1[0])):
        for j in range(len(matrix1[0])):
            newmatrix[i][j] = min(matrix1[i][j],matrix2[i][j])

    return newmatrix

def getpowers(matrixarray):
    # iterate through to some number and then add to array to get sequence of min path length matrices
    M0 = matrixarray[0]

    for i in range(2,SIZE): # should change this to a while loop. while (matrix not complete graph...):
        newmatrix = raiseton(M0,i)
        newmatrix = np.multiply(matrixarray[-1],newmatrix)

        for i in range(ROWS):
            for j in range(COLUMNS):
                if(newmatrix[i][j] > 0):
                    newmatrix[i][j] = i

        matrixarray.append(newmatrix)

    return matrixarray[1:]

################################################################################

M = []

reader = csv.reader(open("test.csv", "rb"), delimiter=",")
x = list(reader)
M.append(np.array(x).astype("int"))

ROWS = len(M[0])
COLUMNS = len(M[0])
SIZE = len(M[0])

print(M[0])

list = getpowers(M)
for i in range(len(list)):
    print list[i]
