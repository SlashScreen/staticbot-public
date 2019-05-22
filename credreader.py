import json

def read():
    f = open("private.json","r")
    creds = json.loads(f.read())
    print(creds)
    return creds

#reads the credential file in order to get like keys and stuff without them being hardcoded
