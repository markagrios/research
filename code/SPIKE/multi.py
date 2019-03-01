import os
import sys

matrix = sys.argv[1]

os.system("python ablate.py " + matrix + " q []")
os.system("python ablate.py " + matrix + " cont []")
os.system("python plotspikehist.py " + matrix)
