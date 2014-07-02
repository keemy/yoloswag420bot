import socket
import sys
import urllib2
import json
from cPickle import load, dump

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
f=open("msgs.pcl","rb")
messageDict=load(f)
f.close()
print messageDict
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
	  
    if text.find(':,tell') !=-1: #check for tell msgs
        to = body.split()[1] #get the desired recipiant of the message
        msg = " ".join(body.split()[2:]) # get the body of the message
        # print sender
        # print to
        # print msg
        if to in messageDict:
            messageDict[to].append("Hey " + to + ", " + sender + " left you the message " + '"' + msg + '" \r\n')
        else:
            messageDict[to]= [sender + " left you the message " + '"' + msg + '" \r\n']
		
        f=open("msgs.pcl","wb")
        dump(messageDict,f)
        f.close()
        irc.send('PRIVchMSG '+channel+' :Noted. \r\n')
 
    if sender in messageDict and command=="PRIVMSG":
        msgs= messageDict[sender]
        del messageDict[sender]
        irc.send('PRIVMSG '+channel+' :'+ sender+ ' you have ' +str(len(msgs))+ ' message(s). \r\n')
        for msg in msgs:
            irc.send('PRIVMSG '+channel+' :'+msg)
        f=open("msgs.pcl","wb")
        dump(messageDict,f)
        f.close()
	
    if text.find(':,search') !=-1:

        query="+".join(body.split()[1:])
        result=json.loads(urllib2.urlopen("https://www.hackerrank.com/rest/contests/master/challenges?query="+query).read())
        output=[prob["name"]+": "+"https://www.hackerrank.com/challenges/"+prob["slug"] for prob in result["models"]]

        if len(output)==0:
            irc.send('PRIVMSG '+channel+' :No results found. \r\n')
        else:
            for result in output:
                irc.send('PRIVMSG '+channel+' :' + result + ' \r\n')
