import socket
import sys
import urllib2
import json
from collections import defaultdict

from advCmds import advCmds


config = json.load(open("config"))

#settings
api_key = config["api_key"]
server = config["server"]
channel = config["channel"]
botnick = config["botnick"]
password = config["password"]

def connect():
    global irc
    irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #defines the socket
    print "connecting to:"+server
    irc.connect((server, 6667))  #connects to the server

    irc.send("PASS " + password + "\r\n")
    irc.send("USER "+ botnick +" "+ botnick +" "+ botnick +" :This is a fun bot!\n") #user authentication
    irc.send("NICK "+ botnick +"\n")                            #sets nick
    #irc.send("PRIVMSG nickserv :identify thisisapw\r\n")    #auth yolo
    irc.send("JOIN "+ channel +"\n")        #join the chan

connect()	

basicCmds = json.load(open("basicCommands"))


def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)

while 1:    #puts it in a loop
    text = irc.recv(2040)  #receive the text
    text = removeNonAscii(text)
    print text   #print text to console
	
    sender = text.split("!")[0][1:] #who sent message
    body=(channel+" :").join(text.split(channel+" :")[1:]) #message text
    body=body.strip() 
    command = text.split()[1] #get the command should be PRIVMSG JOIN PART QUIT 


    if len(text)==0:
        print "Disconnected!"
        connect()
	
    if text.find('PING') != -1: #check if 'PING' is found
        irc.send('PONG ' + text.split() [1] + '\r\n') #returns 'PONG' back to the server (prevents pinging out!)

    if body and body.split()[0] == "!commands":
        irc.send("PRIVMSG " + channel + " :" +  ", ".join(basicCmds.keys()+advCmds.keys()) + "\r\n")

    if body and body.split()[0] in basicCmds:
        irc.send("PRIVMSG " + channel + " :" + basicCmds[body.split()[0]] + "\r\n")

    if body and body.split()[0] in advCmds:
        irc.send("PRIVMSG " + channel + " :" + advCmds[body.split()[0]]() + "\r\n")
