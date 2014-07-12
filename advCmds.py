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

def skinCode(a=[-1]):
#    codes = ["RWWNH74XF3DUKM","RW6DGGL96FUGQ6","RWWP77FD3JD64A","RWTCH9HDVCNUYX","RW9QJUFCXPCXG2","RW6ME4KV49LURC","WWPPL4D3K4P3AM","WW93CDWU9TFNWW","WWGQC4LT346AWM","MYGGEG6P9AM2","YQG273CXKUPF","RTHGGXWPAQ62","E6A6V47EUCHF","NF72KKGXXUAF","HU3LUFAGLU96","CRL2YLJVDQTF","MXWYYGDU9J4R"]
    codes = []
    a[0]+=1

    if a[0] < len(codes):
        return codes[a[0]]
    else:
        return "No more codes kids"

advCmds["!skincode"]=skinCode
