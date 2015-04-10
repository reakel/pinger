#!/bin/sh

# Generating IP addresses
python /usr/local/share/pinger/adrgen.py

# Running the ping command
fping -c1 -t300 -u < /usr/local/share/pinger/adr \
			> /usr/local/share/pinger/output 2>&1

# Generating the html page
python /usr/local/share/pinger/htmlgen.py
