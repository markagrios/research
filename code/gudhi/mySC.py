import csv
import sys
sys.path.append('/home/osboxes/gudhi/build/cython/')
import gudhi

def csv_to_SC(matrix):
    simpcomp = gudhi.SimplexTree()

    with open("connection_matrices/"+matrix) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        a = list(readCSV)

    for ri in range(len(a[0])):
        for ci in range(len(a[0])):
            if(a[ri][ci] != "0"):
                simpcomp.insert([ri,ci],0.1)

    return(simpcomp)
################################################################################

#
# matrix = "di-sixclique.csv"
#
# st = gudhi.SimplexTree()
# connect_from_Matrix(matrix)
#
#
# # rips = gudhi.RipsComplex(points=[[0, 0], [1, 0], [0, 1], [1, 1]],max_edge_length=42)
# # rips = gudhi.RipsComplex(points=[[0, 0], [1, 0], [0, 1], [1, 1], [2,7]])
# rips = gudhi.RipsComplex(points=[[0, 0], [1, 0], [0, 1], [1, 1], [2,7]], max_edge_length=42)
#
# simplex_tree = rips.create_simplex_tree(max_dimension=1)
#
# print("Filtration:")
# print(simplex_tree.get_filtration())
# print("---")
# simplex_tree.set_filtration(0)
# print(simplex_tree.get_filtration())
# print("---")
# print(simplex_tree.num_vertices(), simplex_tree.num_simplices())
# print("---")
#
#
# # result_str = 'Rips complex is of dimension ' + repr(simplex_tree.dimension()) + ' - ' + \
# #     repr(simplex_tree.num_simplices()) + ' simplices - ' + \
# #     repr(simplex_tree.num_vertices()) + ' vertices.'
# # print(result_str)
# # fmt = '%s -> %.2f'
# # for filtered_value in simplex_tree.get_filtration():
# #     print(fmt % tuple(filtered_value))
#
#
# diag = simplex_tree.persistence(homology_coeff_field=2, min_persistence=0)
# print(diag)
#
# # gudhi.plot_persistence_diagram(diag)

############# THEIR EXAMPLE FOR CSV ############################################

# rips_complex = gudhi.RipsComplex(csv_file='connection_matrices/di-sixclique.csv', max_edge_length=12)
# simplex_tree = rips_complex.create_simplex_tree(max_dimension=1)
simplex_tree = csv_to_SC("di-sixclique.csv")

print("Filtration:")
print(simplex_tree.get_filtration())
print("---")
print(simplex_tree.num_vertices(), simplex_tree.num_simplices())
print("---")




# result_str = 'Rips complex is of dimension ' + repr(simplex_tree.dimension()) + ' - ' + \
#     repr(simplex_tree.num_simplices()) + ' simplices - ' + \
#     repr(simplex_tree.num_vertices()) + ' vertices.'
# print(result_str)
# fmt = '%s -> %.2f'
# for filtered_value in simplex_tree.get_filtration():
#     print(fmt % tuple(filtered_value))


diag = simplex_tree.persistence(homology_coeff_field=2, min_persistence=0)
print(diag)

# gudhi.plot_persistence_diagram(diag)
