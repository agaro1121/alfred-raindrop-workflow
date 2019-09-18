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
    out = []
    # ids = [8226098, 7887436, 7887435, 7887434, 7887433, 7887432, 7887431, 7887430, 7887429, 7887428, 7887427, 7887426, 7887425, 7887424, 7887423, 7887422, 7887421, 7887420, 7887419, 7887418, 7887417, 7887416, 7887415, 7887414, 7887413, 7887412, 7887411]
    with concurrent.futures.ThreadPoolExecutor(max_workers=CONNECTIONS) as executor:
        for res in executor.map(raindrop_client.getRaindrops, ids):
            out += list(map(lambda item: extractBookmarkInfo(item), res['items']))
        return out

def getAllBookmarksParallel2():
    ids = getCollectionIds()
    out = []
    # ids = [8226098, 7887436, 7887435, 7887434, 7887433, 7887432, 7887431, 7887430, 7887429, 7887428, 7887427, 7887426, 7887425, 7887424, 7887423, 7887422, 7887421, 7887420, 7887419, 7887418, 7887417, 7887416, 7887415, 7887414, 7887413, 7887412, 7887411]
    # Start the load operations and mark each future with its URL
    with concurrent.futures.ThreadPoolExecutor(max_workers=CONNECTIONS) as executor:
        future_to_id = {executor.submit(raindrop_client.getRaindrops, id): id for id in ids}
        for future in concurrent.futures.as_completed(set(future_to_id)):
            id = future_to_id[future]
            try:
                data = future.result()
            except Exception as exc:
                print('%r generated an exception: %s' % (id, exc))
            else:
                out += list(map(lambda item: extractBookmarkInfo(item), data['items']))
    return out

def getAllBookmarksParallel3():
    def mapper(css):
        # print('***** css')
        # print(css)
        # print('***** css[items]')
        # print(css['items'])
        return list(map(lambda item: extractBookmarkInfo(item), css['items']))

    ids = getCollectionIds()
    with concurrent.futures.ThreadPoolExecutor(max_workers=CONNECTIONS) as executor:
        res = executor.map(raindrop_client.getRaindrops, ids)
        print('***** res')
        print(list(res))
        return reduce(
            lambda cs1, cs2:
                # print(cs1)
                mapper(cs1) + mapper(cs2)
            , list(res)
            )
        # collections = list(itertools.chain(*res))
        # return list(map(extractBookmarkInfo, collections))

def search(term):
    results=raindrop_client.search(term)['items']
    return list(map(lambda result: extractBookmarkInfo(result), results))