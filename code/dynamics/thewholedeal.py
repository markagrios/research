import os
import sys

network = sys.argv[1]
ablation_list = sys.argv[2]

ablation_list = ablation_list.split(",")

command = "python ablate.py " + network

os.system(command + " q 0-0")           # just to stabilize the network
os.system(command + " cont 0-0")        # just to run it once

for i in range(1,len(ablation_list)):
    argpassed = "python ablate.py " + network + " cont " + ",".join(ablation_list[:i])
    # print(argpassed)
    os.system(argpassed)


os.system("python plot.py " + network)
