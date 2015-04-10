## Pinger

Dette skriptet pinger ip-adresser og presenterer resultatene i en html-fil som er tilgjengelig fra nettleser.

Mappen inneholder følgende filer:


'maskiner'

Formatet er "ip-adresse maskinnavn". For windowspcer er det enkelt å finne maskinnavn, da vil
"nt-0XXXX.win.ntnu.no" gi "kXXXX" som maskinnavn. Ubuntumaskinene kjører et litt annet løp, der kan man ikke 
dedusere maskinnavn fra adresse, slik at man må hente inn denne listen fra et annet sted på serveren. TODO:
hent ubuntuinfo fra listen som gir opphav til pridewatcher.


'datasaler'

Formatet er "salnavn nedre_grense øvre_grense". Maskinnummerne (altså "XXXX") er lagt inn i serie, slik at
hver datasal har et lukket intervall som bestemmer hvilke maskiner som hører hjemme der.


'adrgen.py'

Skriptet åpner 'maskiner' og henter ut ip-adressene og lagrer dette i en fil kalt 'adr' som kan benyttes av
fping.


'adr'

Inneholder adressene fra 'maskiner', generert av 'adrgen.py'.


'pinger.sh'

Dette shell-skriptet tilsvarer en serie med kommandolinjeinstrukser som serveren kjører. Første linje (se
bort i fra linjen med "#!bin..") sier at python skal kjøre 'adrgen.py' skriptet. Denne kommandoen lager som
sagt 'adr', og i andre linje vil fping-kommandoen bruke adressene fra 'adr' (<adr) og deretter  sende én 
pakke (-c1) og maks vente 300ms (-t300) og lagre feil (-u) og putte alt i filen 'output' (>output). 2>&1 
forteller at STDERR skal sende sitt output til STDOUT. Dette er fordi adresser som ikke finnes vil generere
en errormelding, og denne vil vi behandle/catche. I tredje linje blir 'html.gen' kallet. Denne lager en htmlfil. 
'pinger.sh' blir kjørt av serveren hver natt klokken 04:00 (kan endres) vha en cron-jobb. Cron- jobber er 
oppgaver/skript som serveren skal kjøre ved bestemte tidspunkter. Root sine crontabs kan øynes ved "sudo crontab
-l" og dine egne fremkommer ved "crontab -l". "crontab -e" brukes for å endre/opprette cron-jobber. Sjekk 
dokumentasjon for syntaks. Det skal merkes at cronjobben kjører en snarvei(soft symlink)  til pinger. Denne 
ligger i /usr/local/bin/. 


'output'

Dette er filen som fremkommer av fping-kommandoen, denne benyttes av 'htmlgen.py' for å lage htmltabeller.


'htmlgen.py'

Denne henter inn 'maskiner' og oppretter en dictionary for adresser -> maskinnavn. Deretter finner den
disse adressene i 'output' og plasserer resultatet i riktig datasal, spesifisert av filen 'datasal'. Resultatene
havner i en pythonliste, som blir samlet til en enkelt streng som lagres i filen 'index.html'.


'index.html'

Denne filen er soft symlinket fra /var/www/pinger/ . Når det uten videre er spesifisert når man f.eks går inn 
på curie.nt.ntnu.no/pinger gjennom nettleser, så vil serveren finne 'index.html' i denne mappen og vise denne.
Da behøver man ikke å skrive ut fullstendig sti (curie.nt.ntnu.no/pinger/index.html) for å nå målet. Gjelder 
forøvrig også printstat og andre skript.

'index.css'

Filen inneholder stilene for htmltabellene brukt i 'index.html'.
