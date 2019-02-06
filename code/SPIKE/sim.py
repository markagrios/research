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

os.system("python ablate.py " + matrix + " q []")
os.system("python ablate.py " + matrix + " cont []")



for g in range(len(ablate_groups)):
    os.system("python ablate.py " + matrix + " cont " + ",".join(ablate_groups[:g+1]))


os.system("python plot.py " + matrix)
