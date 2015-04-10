# -*- coding: utf-8 -*- 
#oppdatert 20/3/14 med tilkobling til innlogging.db, Erik
import re
import time
import sys
import sqlite3 as lite

dbcon = lite.connect('/usr/local/share/innloggingslogging/innlogging.db')
dbcon.text_factory = str

p = "/usr/local/share/pinger/"
html = []

html.append("<html>\n<head>\n<title>Maskinstatus</title>\n<meta charset='utf8'>\n"
            +"<link rel='stylesheet' type='text/css' href='index.css'</link></head>"
            +"\n<body>\n")
html.append("<h3>Statusliste</h3>\n")
html.append(" <h1>Pinger er skrudd av! Bruk db-systemet istedet!</h1><br><p>Husk at denne oversikten sier ikke noe ytterligere enn hvorvidt "
            +"maskinen svarte på pakkeforespørselen.\ Dette betyr at tabellene "
            +"ikke gir informasjon om hvilke programmer som er installert, "
            +"eller hvordan det står til med\ skjerm, mus og tastatur osv. Det "
            +"mest kritiske er om de ikke er meldt inn, da vil maskinen i hvert "
            +"fall være\ ubrukelig.<br><br>HUSK ogsaa at scriptet for "
            +"windowsmaskinene sin del antar at pcnavnet kan deduseres fra "
            "adressen.\
	Dersom en maskin er meldt inn med feil navn vil pinginfoen til maskinens adresse gi feilsvar (eller meldingen fra en\
	annen maskin dersom deres navn er blitt swappet ved innmelding)<br><br>\
	Sist kjørt: "+time.asctime(time.localtime(time.time()))+"</p>\n")

class datasal:
    ''''''
    def __init__(self,name,lower,upper):
        self.name = name
	self.starttable = "<table width='1000px'>\n<th>%s</th><th>Adresse</th><th>Registrert</th><th>Maskinstatus</th>\n" % self.name
        self.middle = [] #""
        self.endtable = "</table>\n<br>\n"
        self.lower = int(lower)
        self.upper = int(upper)
    def maketable(self):
        return "".join([self.starttable,"".join(self.middle),self.endtable])

def makedatasalholder():
    
    try:
        with open(p+"datasaler") as tmp:
	    saler = tmp.readlines()
    except:
	sys.exit(0)

    salholder = []
    
    for line in saler:
	salholder.append(datasal(*(line.strip().split())))
    
    return salholder

def makecomputerdict():
    ''' 
    Makes a python dictionary of the computer addresses and names,
    and has the form key: value, where key will be the address, and
    value will be the name.
    '''

    try:
        with open(p+"winmaskiner") as tmp:
            maskiner = tmp.readlines()
        with open(p+"ubuntuadr") as tmp2:
            maskiner.extend(tmp2.readlines())
    except:
	sys.exit(0)

    dic = {}
    
    for info in maskiner:
	dic[info.split()[0]] = info.split()[1].strip()

    return dic

def computerstatus(linje):
    ''' Checks the status of a computer when given a line from the pinger
	output file. Uses regex'''

    if re.search(r'1/1/0%',linje):
        return "Ja","Ok"," class='ok'"
    elif re.search(r'1/0/100%',linje):
        return "Ja","Avslått/timeout"," class='kanskje'" 
    elif re.search(r'address not found',linje):
        return "Nei","-"," class='dass'"
    else:
        return "Ukjent","Ukjent"," class='wtf'"

salholder = makedatasalholder() 
compdict = makecomputerdict()

with open(p+"output") as data:
    output = data.readlines()

for line in output:
    adresse = line.split()[0]
    navn = compdict.get(adresse)
    
    if not navn:
	continue
   
    if navn[0] == "n":
	navn = "k"+navn[4:8]
	
    num = int(navn[1:])
    innmeldt, stat, stil = computerstatus(line)
    for sal in salholder:
        if sal.lower <= num <=sal.upper:
		sal.middle.append("<tr%s><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>\n" % (stil,navn,adresse,innmeldt,stat))
		#maskinnr og status for sql-database
		#print num
		mnavn='NT-0'+str(num)
		#pstatus=stat
		#insert sql
		with dbcon:
			cur=dbcon.cursor()
			cur.execute("UPDATE maskiner SET pingerstatus = ? WHERE maskinnavn = ?",(stat,mnavn))
		break

for sal in salholder:
    #sal.middle.sort()
    html.append(sal.maketable())

html.append("</body>\n</html>")

try:
    with open(p+"index.html","w") as status:
        status.write(''.join(html))
except IOError:
    sys.exit(0)
