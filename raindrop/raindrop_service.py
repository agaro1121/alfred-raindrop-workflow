import raindrop_client as raindrop_client
import utilities
import json
import itertools

import concurrent.futures
import time


# concurrent web calls
CONNECTIONS = 16
TIMEOUT = 5

def persistCookies():
    try:
        creds=utilities.loadCredentialsFile()
        cookies=raindrop_client.authenticate(creds)
        return utilities.upsertCookieFile(cookies)
    except:
        return None

def getCollectionIds():
    res = raindrop_client.getCollections()
    collections = res['items']
    return list(map(lambda collection: collection['_id'], collections))

def extractBookmarkInfo(bookmark):
    return { 'title': bookmark['title'],
        'link': bookmark['link'],
        'summary': bookmark['excerpt'],
        'icon': bookmark['cover'] }

def getAllBookmarks():
    ids = getCollectionIds()
    listOfCollections = list(map(lambda id: raindrop_client.getRaindrops(id)['items'], ids))
    collections = list(itertools.chain(*listOfCollections))
    return list(map(extractBookmarkInfo, collections))

def getAllBookmarksParallel():
    ids = getCollectionIds()
    with concurrent.futures.ThreadPoolExecutor(max_workers=CONNECTIONS) as executor:
        futures = map(lambda id: executor.submit(raindrop_client.getRaindrops, id), ids)
        results = map(lambda future: future.result()['items'], futures)
        flattenedResults = reduce(lambda r1,r2: r1 + r2, results)
        transformedResults = map(lambda item: extractBookmarkInfo(item), flattenedResults)
        return transformedResults

def search(term):
    results=raindrop_client.search(term)['items']
    return list(map(lambda result: extractBookmarkInfo(result), results))