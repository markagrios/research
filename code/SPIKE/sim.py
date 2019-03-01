import os
import sys
import random
import numpy as np
import cPickle as pickle
from mogutda import SimplicialComplex


###############################################################################

matrix = sys.argv[1]
ablation_list = sys.argv[2]
ablate_groups = ablation_list.split("-")


print("---")

os.chdir("neurotop/src")
os.system("./directed  ../../../connection_matrices/" + matrix +".csv 1 1")
os.chdir("../../../connection_matrices")
os.rename(matrix+".csv_simplices_dimension_.txt", matrix+"_dlist.csv")
os.chdir("../SPIKE")



os.system("python hom.py " + matrix + " " + ",".join(ablate_groups))

run = raw_input("Continue with this ablation sequence? ")

if(run == 'y'):
    os.system("python ablate.py " + matrix + " q []")
    os.system("python ablate.py " + matrix + " cont []")



    for g in range(len(ablate_groups)):
        os.system("python ablate.py " + matrix + " cont " + ",".join(ablate_groups[:g+1]))

    # os.system('spd-say "beep boop its a joop"')
    os.system("python plot.py " + matrix)
