# http://gudhi.gforge.inria.fr/python/latest/

import sys
sys.path.append('/home/mark/gudhi/build/cython')

import gudhi
# from /home/mark/gudhi/build/cython import gudhi

st = gudhi.SimplexTree()
if st.insert([0, 1]):
    print("[0, 1] inserted")
if st.insert([0, 1, 2], filtration=4.0):
    print("[0, 1, 2] inserted")
if st.find([0, 1]):
    print("[0, 1] found")
result_str = 'num_vertices=' + repr(st.num_vertices())
print(result_str)
result_str = 'num_simplices=' + repr(st.num_simplices())
print(result_str)
print("skeleton(2) =")
for sk_value in st.get_skeleton(2):
    print(sk_value)

print("----------------")
print(st.persistence(1))
print(st.persistence(2))
print(st.persistence(3))
# print(st.persistence(4))

# print(st.betti_numbers())
