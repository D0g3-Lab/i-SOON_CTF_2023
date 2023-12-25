#!/bin/sh
echo $D0g3CTF > /flag
chmod 444 /flag
unset D0g3CTF
iptables -P INPUT ACCEPT
iptables -F
iptables -X
iptables -Z
iptables -A INPUT -p tcp --dport 80 -j ACCEPT
iptables -A OUTPUT -m state --state RELATED,ESTABLISHED -j ACCEPT
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
iptables -A OUTPUT -m state --state NEW -j DROP
iptables -P OUTPUT DROP
iptables -n -L
java -jar /app/ezjava.jar
