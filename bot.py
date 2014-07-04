import socket
import sys
import urllib2
import json





server = "irc.twitch.tv"       #settings
channel = "#apsona"
botnick = "yoloswag420bot"
password = "oauth:b5akraa6n4ort22sqiweqcxnzawgpf0"

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

while 1:    #puts it in a loop
    text=irc.recv(2040)  #receive the text
    print text   #print text to console
	
    sender = text.split("!")[0][1:] #who sent message
    body=(channel+" :").join(text.split(channel+" :")[1:]) #message text
    command = text.split()[1] #get the command should be PRIVMSG JOIN PART QUIT 
	
    if len(text)==0:
        print "Disconnected!"
        connect()
	
    if text.find('PING') != -1: #check if 'PING' is found
        irc.send('PONG ' + text.split() [1] + '\r\n') #returns 'PONG' back to the server (prevents pinging out!)

    if body and body.split()[0] == "!commands":
        irc.send("PRIVMSG " + channel + " :" +  ", ".join(basicCmds.keys()) + "\r\n")

    if body and body.split()[0] in basicCmds:
        irc.send("PRIVMSG " + channel + " :" + basicCmds[body.split()[0]] + "\r\n") 
