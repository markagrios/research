
simMinlist = []
simMaxlist = []

for i in range(N):
    simMinlist.append(np.min(Z[i][(duration/2):]))
    simMaxlist.append(np.max(Z[i][(duration/2):]))

simMin = np.min(simMinlist)
simMax = np.max(simMaxlist)
# print(simMin,simMax)                            # I think we should sample from like halfway through the simulation to the end because having the network synchronize screws up the min and max
# print(scaleToInterval(0,simMin,simMax))

scaledM = []

for i in range(0,N):
    scaledM.append([])
    for j in range(0, duration/10):
        # scaledM[i].append(scaleToInterval(M[i].z[10*j], simMin, simMax))
        scaledM[i].append(scaleToInterval(Z[i][10*j], simMin, simMax))


phasic = []
for i in range(0,len(scaledM[0])):
    phasic.append(0)
    for j in range(0,N):
         phasic[i] += cmath.exp(complex(scaledM[j][i],0)*complex(0,1))

    phasic[i] = abs(phasic[i])/N


h = phasic[len(phasic)/3:]
dhdt = []
for i in range(1,len(h)):
    dhdt.append(abs(h[i] - h[i-1]) * 1000)

averagesync = sum(dhdt)/len(dhdt)
print("Synchronization value: " + str(averagesync))
title += str('%.4f'%(averagesync))

##########################
# for i in range(duration/singlerun):
#     section = []
#     for j in range(singlerun):
#         step = (singlerun*i)+j
#         for k in range(N):
#
#             section.append(Z[k][step])
#
#     runningsync.append(section)
