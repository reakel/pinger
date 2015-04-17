#!/bin/bash

sqlite3 /usr/local/share/innloggingslogging/innlogging.db "select ip from  maskiner" | fping -c1 -t300 -u 2>&1 | awk '{
 if ( $5 == "1/1/0%," ) {
 print "update maskiner set pingerstatus = \x27Ok\x27 where ip = \x27" $1 "\x27" ";"  
}
 else if ( $5 == "1/0/100%" ) {
 print "update maskiner set pingerstatus = \x27Av/timeout\x27 where ip = \x27" $1 "\x27" ";" 
}
 else if ( $2 == "address" ) {
 print "update maskiner set pingerstatus = \x27-\x27 where ip = \x27" $1 "\x27" ";"  
} 
}' | sudo sqlite3 /usr/local/share/innloggingslogging/innlogging.db

