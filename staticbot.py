import discord
import asyncio
import rssfeed as rss
import subprocess
import psutil
import random
import florasearch as fs
import credreader as cr

creds = cr.read()
client = discord.Client()
adminid = creds["admin-id"]

#I barely remember how this works sorry 

#GET CLIENT
def getClient():
    return client

#BYTES TO GIGABYTES
def BtoGb(b):
    return b/1000000000

#DATE PARSING
def constructDate(date):
    out = "{h}:{m}:{s} UTC ON {y}-{mon}-{d}".format(h=date.tm_hour,m=date.tm_min,d=date.tm_mday,mon=date.tm_mon,y=date.tm_year,s=date.tm_sec)
    return out

#STATIC STATS
def getSystemInfo():
    servmem = psutil.virtual_memory()
    p = psutil.Process()
    procmem = p.memory_info()
    cpu_perc = p.cpu_percent(interval=1)
    info = "```json\nLOWERING VOLUME. i am currently using {vms} gigabytes of RAM, out of a total {tot} gigabytes. i am using {cpu}% of the cpu.```".format(vms = BtoGb(procmem.vms),tot = BtoGb(servmem.total),cpu = cpu_perc)
    return info

#FREQUENCY
async def changeFrequency(client):
    random.seed()
    frequency = round(random.uniform(76.1,1710.0),1)
    fgame = discord.Game(name = "frequency {f} khz".format(f=frequency),type=2)
    await client.change_presence(game=fgame)
    
#SEND UPDATE
async def sendUpdate(client,channelid,serverid,falsemessage = True, save = True,inchannel = None):
    channel = None
    if inchannel == None:
        server = client.get_server(str(serverid)) #flora server id
        channel = server.get_channel(str(channelid))
        
    else:
        channel = inchannel
    needsupdating = rss.setup(save) #setup rss
    outlist = rss.readOne()
    if not needsupdating:
        print(server,channel)
        for entry in outlist.values():
            title = entry['title']
            date = entry['date']
            await client.send_message(channel, "```JSON UPDATE INCOMING.```")
            await client.send_message(channel, "```python\n"+"-"*10+"\nraising volume.\nNEW FLORAVERSE PAGE DETECTED\n'{t}'\nUPLOADED AT {h}.\n".format(t=title.upper(),h = constructDate(date))+"-"*10+"```")
            
    else:
        if falsemessage:
            for entry in outlist.values():
                title = entry['title']
                date = entry['date']
                await client.send_message(channel, "```python\n"+"-"*10+"\nraising volume.\nNO NEW FLORAVERSE PAGES DETECTED\nRETRIEVING DATA FOR MOST RECENT UPDATE... \n'{t}'\nUPLOADED AT {h}.\n".format(t=title.upper(),h =constructDate(date))+"-"*10+"```")       
#ANNOUNCE
async def announce(m,client,sid,chid):
    args = m.split(' ',2)
    server = client.get_server(sid) 
    channel = server.get_channel(chid) 
    if channel == None:
        return
    print(server,channel)
    await client.send_message(channel,"```json\nraising volume. ANNOUNCEMENT IMMINENT.```")
    await asyncio.sleep(1)
    await client.send_message(channel,"```json\nANNOUNCEMENT RECIEVED. PARSING PACKAGE...```")
    await asyncio.sleep(1)
    await client.send_message(channel,"```json\nANNOUNCEMENT PARSED. RELAYING PACKAGE.\n-----\n{msg}\n-----\nRELAY SUCCESSFUL. RESUMING NORMAL BEHAVIOR.```".format(msg=args[2]))

async def getServerStuff(client): #Reads creds
    server = client.get_server(creds["test-server"])
    channel = server.get_channel(creds["test-channel"]) 
    c_lst = client.get_all_channels()
    for c in c_lst:
        await client.send_message(channel,str(c)+":"+c.id)

#ACTUAL BOT STUFF
@client.event
async def on_ready():
    print('------')
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('''

  ______ _______ _______ _______ _ _______ 
 / _____|_______|_______|_______) (_______)
( (____     _    _______    _   | |_       
 \____ \   | |  |  ___  |  | |  | | |      
 _____) )  | |  | |   | |  | |  | | |_____ 
(______/   |_|  |_|   |_|  |_|  |_|\______)
                                           
''')
    print('------')
    while True:
        #Change status and check for update
        await asyncio.sleep(60)
        for i in creds["update-servers"]:
            for f in creds["update-channels"]:
                #print("server",i,"channel",f)
                await sendUpdate(client,f,i,falsemessage = False)
        await changeFrequency(client)

#PARSE COMMANDS
async def parseCommands(client,msg,isMe,message):
    admin = await client.get_user_info(adminid)
    adminname = admin.name
    if isMe:
        if "stop" in msg: #Admin- quit
            quit();
        elif "ping" in msg: #Admin- ping
            await client.send_message(message.channel,"```pong.```")
        elif "stats" in msg:
            await client.send_message(message.channel,getSystemInfo())
        elif "announce" in msg: #Announcement- admin only
            for i in creds["update-servers"]:
                for f in creds["update-channels"]:
                    await announce(msg,client,i,f)
            await client.send_message(message.channel,"I HAVE SEEN TO IT PERSONALLY THAT YOU MESSAGE GETS THROUGH.")
        elif "getstuff" in msg:
            await getServerStuff(client)
        elif "help" in msg: #get help link
            await client.send_message(message.channel, "```LOWERING VOLUME. go to http://slashscreen.com/code/bots/static/statichelp.html.```")
        elif "update" in msg: #get update
            print(message.server)
            await sendUpdate(client,message.channel.id,message.server,save = False,inchannel = message.channel)
        elif "search" in msg: #static search
            await client.send_message(message.channel, "```json\nraising volume. SEARCHING FOR GIVEN QUERY. PLEASE BE PATIENT, AS IT MAY TAKE SOME TIME.```")
            res = fs.supersearch(msg)
            await client.send_message(message.channel, res)
        else:
            await client.send_message(message.channel,"```...```") #...
    else:
        
        if "stop" in msg:
            await client.send_message(message.channel,"```ERROR. system functions locked to user {admin}.```".format(admin = adminname))
        elif "ping" in msg:
            await client.send_message(message.channel,"```ERROR. ping pong function locked to user {admin}.```".format(admin = adminname))
        elif "stats" in msg:
            await client.send_message(message.channel,"```ERROR. hardware information locked to user {admin}.```".format(admin = adminname))
        elif "announce" in msg:
            await client.send_message(message.channel,"```ERROR. pa system locked to user {admin}.```".format(admin = adminname))
        elif "getstuff" in msg:
            await client.send_message(message.channel,"```ERROR.backdoor commands locked to user {admin}.```".format(admin = adminname))
        elif "help" in msg:
            await client.send_message(message.channel, "```LOWERING VOLUME. go to http://slashscreen.com/code/bots/static/statichelp.html.```")
        elif "update" in msg:
            await sendUpdate(client,message.channel.id,save = False,inchannel = message.channel)
        elif "search" in msg:
            await client.send_message(message.channel, "```json\nraising volume. SEARCHING FOR GIVEN QUERY. PLEASE BE PATIENT, AS IT MAY TAKE SOME TIME.```")
            res =fs.supersearch(msg)
            await client.send_message(message.channel, res)
        else:
            await client.send_message(message.channel,"```...```")

#ON MESSAGE
@client.event
async def on_message(message):
    msg = message.content.lower()
    if not message.author.id == creds["self-id"]: #self-id is the bot ID so it doesn't respond to itself. that was a huge problem
        if "static " in msg:
            if message.author.id == adminid: #If admin
                await parseCommands(client,msg,True,message) #Parse as admin
            else:
                await parseCommands(client,msg,False,message) #parse as citizen
        if msg == "static":
            await client.send_message(message.channel,"```...```") #this is the ... thing static does

#SET UP           
def setup():
    client.run('NTA1OTYzNDc3ODk0OTU1MDA4.DrbO5A.ZVwnELAbJLa197XGM1SNKpSfNU0')
#MAIN
if __name__ == "__main__":
    setup()
