import feedparser
#import webbrowser
from pathlib import Path
import os

#TODO: Subscribe, Unsubscribe, any new(Requires file of last known rss, compare)?

feeds = []
cwd = os.path.realpath(os.path.join(os.getcwd(),os.path.dirname(__file__)))
def findFile(name):
   return os.path.join(cwd,name) 

def readSubscriptions():
    path = Path(findFile("subscriptions.txt"))
    links = []
    
    if not path.is_file():
        print("ERROR: Subscription file not found!")
        #quit()

    f = open(findFile("subscriptions.txt"))
    file = f.read().splitlines()
    links = file
    return links

def getFeeds(links):
    for x in links:
        feeds.append(feedparser.parse(x))

def getFeedsVar():
    return feeds

def readOne():
    i=0
    outlist = {}
    for feed in feeds:
        try:
            entry = feed.entries[0]
            i+= 1
            article_title = entry.title
            article_link = entry.link
            article_date = entry.published_parsed
            out = "{}: {} \n [{}]".format(i,article_title,article_link)
            outlist[article_title] = {}
            outlist[article_title]['link'] = article_link
            outlist[article_title]['title'] = article_title
            outlist[article_title]['date'] = article_date
            #print (out)
        except:
            raise ConnectionError 
    return outlist

def compareCache():
    upToDate = True
    path = Path(findFile("cache.txt"))
    file = []
    f =  open(findFile("cache.txt"))
    file = f.read().splitlines()
        
        #print(file)
    NewFeeds = readOne()
    i = 0
    for article,entry in NewFeeds.items():
        #print(file)
        if file == []:
            upToDate = False
            break
        #print (feed)
        if i > len(file)-1:
            break
        #print(i)
        line = file[i]
        if not line == entry["link"]:
            #print (entry["link"])
            #print (line)
            upToDate = False
        i += 1
    return upToDate

def saveCache():
    f = open(findFile("cache.txt"), 'r+')
    f.truncate(0)
    f.close()
    f = open(findFile("cache.txt"),"w+")
    #for feed in feeds:
    links = []
    for entry in feeds[0].entries:
        links.append(entry.link)
    f.write(str(links[0])+"\n")
    f.close()

def setup(save = True):
    getFeeds(readSubscriptions())
    upToDate=compareCache()
    if save:
       saveCache()
    return upToDate

