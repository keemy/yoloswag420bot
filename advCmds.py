import socket
import sys
import urllib2
import json
from collections import defaultdict

config = json.load(open("config"))

#settings
api_key = config["api_key"]
server = config["server"]
channel = config["channel"]
botnick = config["botnick"]
password = config["password"]
summonerId = config["summonerId"]


runes = json.load(open("runeData"))["data"]



advCmds = {}
def currentRunes():
    pages = json.load(urllib2.urlopen("https://na.api.pvp.net/api/lol/na/v1.4/summoner/"+summonerId+"/runes?"+api_key))["20097656"]["pages"]
    cur = [page for page in pages if page["current"]][0]["slots"]

    stats = defaultdict(float)
    for rune in cur:
        runeStats = runes[str(rune["runeId"])]["stats"]
        for stat, value in runeStats.iteritems():
            stats[stat]+=value
    stats = dict(stats)
    output=""
    for stat,value in stats.iteritems():
        output+= str(stat[:-3])+": "+str(value)+", "

    return output
advCmds["!runes"] = currentRunes

def currentMasteries():
    pages = json.load(urllib2.urlopen("https://na.api.pvp.net/api/lol/na/v1.4/summoner/"+summonerId+"/masteries?"+api_key))["20097656"]["pages"]
    cur = [page for page in pages if page["current"]][0]
    
    dist = [0]*3

    for mastery in cur["masteries"]:
        dist[ (mastery["id"]-4100)//100 ] += mastery["rank"]

    return cur["name"] + " - " + "/".join([str(i) for i in dist])
advCmds["!masteries"] = currentMasteries

