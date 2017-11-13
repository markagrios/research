import sys
sys.path.append('/home/mark/gudhi/build/cython')
import gudhi

simpcomp = gudhi.SimplexTree()

simpcomp.set_dimension(3)

# simpcomp.insert([1],-1.5)
# simpcomp.insert([2],-1.4)
# simpcomp.insert([3],-1.3)
# simpcomp.insert([4],-1.2)
# simpcomp.insert([1,2],-1.1)
# simpcomp.insert([1,3],-1.0)
# simpcomp.insert([1,4],-0.9)
# simpcomp.insert([2,3],-0.8)
# simpcomp.insert([2,4],-0.7)
# simpcomp.insert([3,4],-0.6)
# simpcomp.insert([1,2,3],-0.5)
# simpcomp.insert([1,2,4],-0.4)
# simpcomp.insert([1,3,4],-0.3)
# simpcomp.insert([2,3,4],-0.2)
# simpcomp.insert([1,2,3,4],0.1)

simpcomp.insert([1],0.1)
simpcomp.insert([2],0.1)
simpcomp.insert([3],0.1)
simpcomp.insert([4],0.1)
simpcomp.insert([1,2],0.12)
simpcomp.insert([1,3],0.12)
simpcomp.insert([1,4],0.12)
simpcomp.insert([2,3],0.12)
simpcomp.insert([2,4],0.12)
simpcomp.insert([3,4],0.12)
simpcomp.insert([1,2,3],0.9)
simpcomp.insert([1,2,4],0.9)
simpcomp.insert([1,3,4],0.9)
simpcomp.insert([2,3,4],0.9)
simpcomp.insert([1,2,3,4],1.5)

simpcomp.initialize_filtration()

p = simpcomp.persistence()

print("Filtration:")
for i in range(len(simpcomp.get_filtration())):
    print(simpcomp.get_filtration()[i])


print("---")
for dim in range(len(simpcomp.get_filtration()[-1])+3):
    print("Persistence of dim " + str(dim) + ": ")
    for i in simpcomp.persistence_intervals_in_dimension(dim):
        print("   " + str(i))

gudhi.plot_persistence_diagram(p)
