import feedparser
#import webbrowser
from pathlib import Path
import os

#TODO: Subscribe, Unsubscribe, any new(Requires file of last known rss, compare)?

feeds = []
cwd = os.path.realpath(os.path.join(os.getcwd(),os.path.dirname(__file__)))
def findFile(name):
   return os.path.join(cwd,name)
   #Does windows/linux paths 

def readSubscriptions():
    path = Path(findFile("subscriptions.txt"))
    links = []
    
    if not path.is_file():
        print("ERROR: Subscription file not found!")
        #quit if no cache.txt file

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
            #Parses rss feed
        except:
            raise ConnectionError 
    return outlist

def compareCache():
    #Compares links from rss feed and cache, to try to see if any are "unread"
    upToDate = True
    path = Path(findFile("cache.txt"))
    file = []
    f =  open(findFile("cache.txt"))
    file = f.read().splitlines()
    NewFeeds = readOne()
    i = 0
    for article,entry in NewFeeds.items():
        if file == []:
            upToDate = False
            break
        if i > len(file)-1:
            break
        line = file[i]
        if not line == entry["link"]:
            upToDate = False
        i += 1
    return upToDate

def saveCache():
    #saves links to cache file- cache.txt
    print("Saving Cache Data...")
    #print(feeds[0]).href
    f = open(findFile("cache.txt"), 'r+')
    f.truncate(0)
    f.close()
    f = open(findFile("cache.txt"),"w+")
    #for feed in feeds:
    links = []
    for entry in feeds[0].entries:
        #print(entry.link)
        links.append(entry.link)
        #print(links)
    print(links[0])
    f.write(str(links[0])+"\n")
    f.close()

def setup(save = True):
    getFeeds(readSubscriptions())
    upToDate=compareCache()
    if save:
       saveCache()
    return upToDate

