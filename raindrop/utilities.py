import os
import os.path
import json
import datetime
from datetime import datetime

home=os.environ['HOME']
workflowPath=home+"/.raindrop"
credentialsFile=workflowPath+"/.credentials"
cookieFile=workflowPath+"/.cookie"

def createWorkFlowPath():
    if not os.path.exists(workflowPath):
        return os.makedirs(workflowPath)

def createFile(fileName):
    return open(fileName, "w")

def deleteFile(fileName):
    if os.path.exists(fileName):
        os.remove(fileName)
    else:
        return None

def readFile(fileName):
    return open(fileName, "r")

def loadJsonFromFile(fileName):
    try:
        f = readFile(fileName)
        return json.load(f)
    # except json.decoder.JSONDecodeError:
    except:
        return None

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
    timestamp=cookie['expires']
    d = datetime.fromtimestamp(timestamp)
    return d <= datetime.today()

def hasCredentials():
    json = loadCredentialsFile()
    if json is None:
        return False
    else:
        return True

def hasValidCookie():
    json = loadCookieFile()
    if json is None:
        return False
    else:
        return not isCookieExpired(json)