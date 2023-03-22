import csv
from io import StringIO
s = "abcedfsdf@efgh.com"

def mask(s):
    lo = s.find('@')
    if lo > 0:
        
        return s.replace(s[int(lo*0.3):lo], "#####")
    return ""


csv_reader = csv.reader(open("votantes_sup.csv"), delimiter=",")

count = 0
n_iter = False
result_list = []
for row in csv_reader:

    print(row)
    # import pdb; pdb.set_trace()
    # import pdb; pdb.set_trace()
    # if not row[2]:
        # result_list.append(row)
        # continue
    nome = row[0]
    # matricula = row[1]
    email = row[1]
    result_list.append((nome, mask(email)))

with open('votantes_superior_final_email_mascarado.csv', 'w') as csvfile:
    spamwriter = csv.writer(csvfile)
    [spamwriter.writerow(r) for r in result_list]
    

print(mask(s))