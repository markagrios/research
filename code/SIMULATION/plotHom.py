import numpy as np
import cPickle as pickle
import matplotlib.pyplot as plt



betas = pickle.load(open("storeddata/betas.p","rb"))

# beta1 = [46,44,44,43,42,41,40,39,38,37,36,35,30,28,24,21,20,19,18,17,13,12,9,6,4,2]



simulation = plt.figure(figsize=(17,10))
title = "betti numbers 0,1,2"
simulation.subplots_adjust(wspace=0.1,hspace=0.25)

for i in range(len(betas)):
    simulation.add_subplot(3,1,i+1)
    plt.ylabel("beta " + str(2-i))
    plt.yticks(np.arange(min(betas[2-i]), max(betas[2-i])+1, 5.0))
    plt.xlabel("ablations")
    plt.plot(betas[2-i], linestyle='--', marker='o', color='b')


plt.show()
