#! /usr/bin/env python


path = "/usr/local/share/pinger/"

data = []
data2 = []

with open(path+"winmaskiner") as fil:
    for l in fil.readlines():
        data.append("%s\n" % l.split()[0])

with open(path+"ubuntuadr") as fil2:
    for l in fil2.readlines():
        data2.append("%s\n" % l.split()[0])

data.extend(data2)

with open(path+"adr","w") as adresser:
    for l in data:
        adresser.write(l)

