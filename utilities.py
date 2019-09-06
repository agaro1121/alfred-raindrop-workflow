import os
import os.path
import json
import datetime
from datetime import datetime

home=os.environ['HOME']
workflowPath=f'{home}/.raindrop'
credentialsFile=f'{workflowPath}/.credentials'
cookieFile=f'{workflowPath}/.cookie'

def createWorkFlowPath():
    if not os.path.exists(workflowPath):
        return os.makedirs(workflowPath)

def createFile(fileName):
    return open(fileName, "w")

def deleteFile(fileName):
    if os.path.exists(fileName):
        os.remove(fileName)
    else:
        print("The file does not exist")

def readFile(fileName):
    return open(fileName, "r")

def loadJsonFromFile(fileName):
    try:
        f = readFile(fileName)
        return json.load(f)
    except json.decoder.JSONDecodeError:
        print(f'No JSON in file or cant parse it. FileName:{fileName}') 

def createCredentialsFile():
    return createFile(credentialsFile)

def deleteCredentialsFile():
    return deleteFile(credentialsFile)

def loadCredentialsFile():
    return loadJsonFromFile(credentialsFile)

def createCookieFile():
    return createFile(cookieFile)

def deleteCookieFile():
    return deleteFile(cookieFile)

def loadCookieFile():
    return loadJsonFromFile(cookieFile)

def bootstrap():
        createWorkFlowPath()
        createCredentialsFile()
        createCookieFile()

def upsertCredentialsFile(email, password):
    deleteCredentialsFile()
    f = createCredentialsFile()
    return f.write(json.dumps({'email': email, 'password': password}))

def upsertCookieFile(cookie):
    """
    Parameters
    ----------
    cookie: Dictionary
        Contains 'connect.sid' and 'expires'
        Example: expires=1575607444
    """
    deleteCookieFile()
    f = createCookieFile()
    return f.write(json.dumps(cookie))

def parseExpires(expires):
    return datetime.fromtimestamp(expires)

def isCookieExpired(cookie):
    timestampString=cookie['expires']
    d = datetime.fromtimestamp(timestampString)
    return d <= datetime.today()

