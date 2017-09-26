from itertools import groupby 

f = open('train_words.csv', 'r')
s = []
for line in f.readlines():
    items = line.split(",")
    s.append(items)
f.close()

srs = []
for key, grp in groupby(s, lambda x: x[0]):
    sr = "".join(g[2] + " " for g in grp)
    print (sr) 

