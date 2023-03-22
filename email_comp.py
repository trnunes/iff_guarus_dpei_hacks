import csv
from io import StringIO

def readcsv(file):
    csv_reader = csv.reader(open(file), delimiter=",")

    count = 0
    n_iter = False
    l = []
    for row in csv_reader:
        
        if row:
            print(row[0])
            l.append(row[0].strip())
    return l

r1 = readcsv('disc1.csv')
r2 = readcsv('disc2.csv')

r3 = [e for e in r1 if e not in r2]
import pdb;pdb.set_trace()
print(r3)