import simplicial

def getsimps(simpfile):
    simpfile = simpfile + "_dlist.csv"
    simps = []
    for line in open("../connection_matrices/simp_lists/" + simpfile):
        simps.append(line.split())

    # print(simps)
    # print("---")

    synapses = []
    for i in range(len(simps)):
        if(len(simps[i]) == 2):
            synapses.append(simps[i])

    return(simps)

print(getsimps(ER_n330p0125))
