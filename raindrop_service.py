import raindrop_client
import utilities
import json
import itertools

def persistCookies():
    try:
        creds=utilities.loadCredentialsFile()
        cookies=raindrop_client.authenticate(creds)
        return utilities.upsertCookieFile(cookies)
    except json.decoder.JSONDecodeError:
        print("No JSON in file or can't parse it") 

def getCollectionIds():
    collections = raindrop_client.getCollections()['items']
    return list(map(lambda collection: collection['_id'], collections))

def extractBookmarkInfo(bookmark):
    return { 'title': bookmark['title'],
        'link': bookmark['link'],
        'summary': bookmark['excerpt'] }

def getAllBookmarks():
    ids = getCollectionIds()
    listOfCollections = list(map(lambda id: raindrop_client.getRaindrops(id)['items'], ids))
    collections = list(itertools.chain(*listOfCollections))
    return list(map(extractBookmarkInfo, collections))

def search(term):
    results=raindrop_client.search(term)['items']
    return results#list(map(lambda result: extractBookmarkInfo(result), results))