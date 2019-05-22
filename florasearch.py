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

async def floraSearch(client,message,msg):
    args = msg.split(" ",2)
    if not args[1] == "search": #parse command
        await client.send_message(message.channel,"```json\nraising volume. SYNTAX IS 'static search [query]'.```")
        return
    if "or" in args[2]: #flavor text
        await client.send_message(message.channel,"```json\nraising volume. DO NOT ATTEMPT TO USE THIS FEATURE FOR SEARCHING OUTSIDE OF FLORAVERSE.COM.```")
        return
    await client.send_message(message.channel, "```json\nraising volume. SEARCHING FLORAVERSE FOR QUERY '{q}'...```".format(q=args[2]))
    try: 
        res = None
        s = googlesearch.search('site:floraverse.com {a}'.format(a=args[2]), stop=5)
        for item in s:
            res = item
            break
        await client.send_message(message.channel, "```json\nSEARCH SUCCESSFUL. RETREAVING HYPERLINK.\n``` {l}".format(l=res))
    except:
        await client.send_message(message.channel,"```json\nSEARCH UNSUCCESSFUL. PLEASE TRY A DIFFERENT QUERY.```")

def linkMinusDate(href): #Gets the link  and removes the date (date confuses searcher)
    sects = href.split("/")
    blank = sects.pop()
    pkg = sects.pop()
    prs = pkg.split("-")
    try:
        int(prs[0])
        return '-'.join(prs[1:])
    except:
        return pkg

async def search(msg): #SEARCH
    #ill be real with you, I wrote this so long ago I barely remember how it works.
    #But it works kinda like this:
    #Search archive page, see what matches best
    #search what matches best, repeat for a few layers
    #I know it's really badly written. great job, 6 or so months ago me
    args = msg.split(" ",2)
    queryparsed = args[2].split(" ") #parse query
    poss_links = {}
    try:
        queryparsed.remove(" ")
    except:
        pass
    http = urllib3.PoolManager()
    wl = []
    for link in searchlinks:
        try:
            res = http.request('GET', link)
            pagedown = BeautifulSoup(res.data,"lxml")
            a = pagedown.find_all("a",href=True)
            for l in a:
                wl.append(l)
            
        except Exception as e:
            print("can't get",e)
            
    possibleh = [] #possibleh = "Possible Header"
    for link in wl:
        if not "floraverse.com/" in link['href']:
            continue
        validity = 0
        title = linkMinusDate(link["href"])
        for l in queryparsed:
            if validity == len(queryparsed):
                return link
            if l in title:
                validity+=1
                possibleh.append(link)
                print(link)
                poss_links[link["href"]] = validity

    print(poss_links)
    possible = []
    for link in possibleh:
        res = http.request('GET', link['href'])
        pagedown = BeautifulSoup(res.data,"lxml")
        a = pagedown.find_all("a",href=True) 
        for l in a:
                print(l)
                possible.append(l)
                
    for link in possible:
        if not "floraverse.com/" in link['href']:
            continue
        validity = 0
        title = linkMinusDate(link["href"])
        for l in queryparsed:
            if l in title:
                validity+=1
            if validity == len(queryparsed):
                return "```json\nI HAVE FOUND WHAT I BELIEVE TO BE THE MOST ACCURATE RESULT.```"+link['href']
            else:
                poss_links[link["href"]] = validity

    return "```json\nI WAS NOT ABLE TO FIND A PAGE WITH THE QUERY {q}. TRY BEING MORE SPECIFIC. IF YOU ARE LOOKING FOR A CHARACTER SHEET, IT HELPS TO INCLUDE 'character' IN YOUR SEARCH.```}".format(q = args[2])

###TRY TRY AGAIN###

def findFile(name):
   return os.path.join(cwd,name) 

def getURLS(wl,query,cache):
    out = []
    http = urllib3.PoolManager()
    for w in wl:
        res = http.request('GET', w)
        pg = BeautifulSoup(res.data,"lxml")
        a = pg.find_all("a",href=True)
        for l in a:
            if not "https://floraverse.com/comic/" in l["href"]: #keeps links to floraverse.com, no patreon or whatever
                continue
            validity = 0
            title = linkMinusDate(l["href"])
            for q in query: #"Validity" means that it matcches 1 of the query words
                if q in title:
                    validity+=1
                if validity == len(query):
                    return wl,True,l["href"] #Return line

            if not l["href"] in cache: #might remove duplicates?
                out.append(l["href"])

    return out, False, None


def supersearch(msg):
    cache = []

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


    for i in range(0,depth): #Pull From Site
        wl,found,link = getURLS(wl,queryparsed,cache)
        if found:
            return "```json\nRETURNING MOST ACCURATE SEARCH RESULT.```\n"+link

    
    return "```JSON\nNONE FOUND. APOLOGIES FOR ANY INCONVENIENCE.```"
    


if __name__ == "__main__":
    print(supersearch("static search practice run")) #test
