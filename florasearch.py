import googlesearch
import asyncio
import urllib3
from bs4 import BeautifulSoup
import operator
import os
urllib3.disable_warnings()
cwd = os.path.realpath(os.path.join(os.getcwd(),os.path.dirname(__file__)))

searchlinks = [
    "https://floraverse.com/comic/seeds",
    "https://floraverse.com/comic/interludes/",
    "https://floraverse.com/comic/oneshots/",
    "https://floraverse.com/comic/references/"
    ]

def linkMinusDate(href):
    sects = href.split("/")
    blank = sects.pop()
    pkg = sects.pop()
    prs = pkg.split("-")
    try:
        int(prs[0])
        return '-'.join(prs[1:])
    except:
        return pkg

###TRY TRY AGAIN###

def findFile(name):
   return os.path.join(cwd,name) 

def getURLS(wl,query,cache):
    out = []
    http = urllib3.PoolManager()
    for w in wl:
        #print(w)
        res = http.request('GET', w)
        pg = BeautifulSoup(res.data,"lxml")
        a = pg.find_all("a",href=True)
        for l in a:
            if not "https://floraverse.com/comic/" in l["href"]:
                continue
            
            validity = 0
            title = linkMinusDate(l["href"])
            for q in query:
                #print(len(query))
                if q in title:
                    validity+=1
                    #print(l["href"],validity)
                if validity == len(query):
                    #print("-------------FOUND IT")
                    return wl,True,l["href"] #Return line

            if not l["href"] in cache: #might remove duplicates?
                out.append(l["href"])

    return out, False, None


def supersearch(msg):
    cache = []
 #   c = open(findFile("search-cache.txt"),"r+")
 #   print (c.read())
 #   cache=c.read().split("\n")
  #  try:
 #       cache.remove("")
 #   except:
 #      pass
    #print(cache)
 #   c = open(findFile("search-cache.txt"),"w+")
    depth = 4
    urls = []
    wl = ["https://floraverse.com/comic/"]
    
    args = msg.split(" ",2)
    queryparsed = args[2].split(" ")
    print(queryparsed)
    try:
        queryparsed.remove(" ")
    except:
        pass

    '''print(cache)
    for line in cache: #Is it in cache? if so, return. else, continue
        validity = 0
        title = linkMinusDate(line)
        print(title,queryparsed)
        for l in queryparsed:
            if validity == len(queryparsed):
                print("by cache")
                print(cache)
                out = "\n"+"\n".join(cache)
                c.write(out)
                return line
            if l in title:
                validity+=1'''

    for i in range(0,depth): #Pull From Site
        wl,found,link = getURLS(wl,queryparsed,cache)
        if found:
            #print("-----------------HERE")
            print("by search")
            #print(cache)
 #          out = "\n"+"\n".join(cache)
 #           c.write(out)
 #           c.close()
            return "```json\nRETURNING MOST ACCURATE SEARCH RESULT.```\n"+link

    
 #   c.close()
    return "```JSON\nNONE FOUND. APOLOGIES FOR ANY INCONVENIENCE.```"
    







if __name__ == "__main__":
    print(supersearch("static search practice run"))
