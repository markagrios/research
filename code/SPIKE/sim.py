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


# qcontinue = raw_input("continue with this ablation sequence? ")
# if(qcontinue == "y"):
#     os.system(command + " q []")           # just to stabilize the network
#     os.system(command + " cont []")        # just to run it once
#
#     for i in range(len(ablation_list)):
#         argpassed = "python ablate.py " + network + " cont " + ",".join(ablation_list[:i+1])
#         print("Now ablating neuron: " + ablation_list[i])
#         os.system(argpassed)
#
#
#     os.system("python spikeplot.py " + network)
