import json
import os

cwd = os.path.realpath(os.path.join(os.getcwd(),os.path.dirname(__file__)))
def findFile(name):
   return os.path.join(cwd,name) 

def read():
    f = open(findFile("private.json"),"r")
    creds = json.loads(f.read())
    print(creds)
    return creds

#read()
