import os
import sys
import random
import numpy as np
import cPickle as pickle
from mogutda import SimplicialComplex


###############################################################################



print("---")

os.system(command + " q []")
os.system(command + " cont []")


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
