import numpy as np
import csv

x = [[1,2,3,4,5],[6,7,8,9,10],[11,12,13,14,15]]
y = [[1,2,3,4,5],[6,7,8,9,10],[11,12,13,14,15]]
z = [[1,2,3,4,5],[6,7,8,9,10],[11,12,13,14,15]]

a = [[0,2,0,4,5],[6,0,8,0,0],[0,12,0,14,0]]
b = [[0,2,0,4,5],[6,0,8,0,0],[0,12,0,14,0]]
c = [[0,2,0,4,5],[6,0,8,0,0],[0,12,0,14,0]]


np.savetxt("test" + "-x" + ".csv", x, delimiter=",", fmt="%s")
np.savetxt("test" + "-y" + ".csv", x, delimiter=",", fmt="%s")
np.savetxt("test" + "-z" + ".csv", x, delimiter=",", fmt="%s")

with open("test-x.csv") as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    q = list(readCSV)

print(q)
print("---")

for i in range(len(q)):
    for j in range(len(a[i])):
        q[i].append(str(a[i][j]))


np.savetxt("test" + "-x" + ".csv", q, delimiter=",", fmt="%s")
