import csv
import sys
sys.path.append('/home/mark/gudhi/build/cython')
import gudhi

def listofsimps_to_SC(matrix):
    simpcomp = gudhi.SimplexTree()

    with open("connection_matrices/"+matrix, 'rU') as p:
        #reads csv into a list of lists
        simp_list = [list(map(int,rec)) for rec in csv.reader(p, delimiter=' ')]

    print(simp_list)
    for simp in simp_list:
        simpcomp.insert(simp)

    return(simpcomp)


matrix = "threecyclelist.csv"

simplex_tree = listofsimps_to_SC(matrix)

print(simplex_tree)

print("done")
