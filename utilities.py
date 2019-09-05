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

def createCredentialsFile():
    return createFile(credentialsFile)

def deleteCredentialsFile():
    return deleteFile(credentialsFile)

def createCookieFile():
    return createFile(cookieFile)

def deleteCookieFile():
    return deleteFile(cookieFile)


def bootstrap():
        createWorkFlowPath()
        createCredentialsFile()
        createCookieFile()

def upsertCredentialsFile(username, password):
    deleteCredentialsFile()
    f = createCredentialsFile()
    return f.write(json.dumps({'username': username, 'password': password}))

def upsertCookieFile(cookie):
    """
    Parameters
    ----------
    cookie: Dictionary
        Contains 'connect.sid' and 'Expires'
        Example: Expires=Fri, 06 Dec 2019 03:12:21
    """
    deleteCookieFile()
    f = createCookieFile()
    return f.write(json.dumps(cookie))

def parseExpires(expires):
    return datetime.strptime(expires, '%a, %d %b %Y %H:%M:%S')

def isCookieExpired(cookie):
    timestampString=cookie['Expires']
    d = parseExpires(timestampString)
    return d <= datetime.today()