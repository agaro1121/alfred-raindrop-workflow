import requests
import json
import utilities

base='https://api.raindrop.io/v1'
auth=f'{base}/auth/login'
collectionsApi=f'{base}/collections'
raindropsApi=f'{base}/raindrops'

cookie=utilities.loadCookieFile()

def authenticate(credentials):
    """
    Parameters
    __________
    credentials: Dictionary
        Contains username and password
    """
    response = requests.post(url=auth, json=credentials)
    responseCookies = response.cookies
    print(f'responseCookies={responseCookies}')
    expireDateTime=next(x for x in responseCookies if x.name == 'connect.sid').expires
    return {
              'expires': expireDateTime,
              'connect.sid': responseCookies['connect.sid']
            }


def authenticatedGet(url):
    jar = requests.cookies.RequestsCookieJar()
    jar.set('connect.sid', cookie['connect.sid'])
    return requests.get(url=url, cookies=jar).json()

def getCollections():
    return authenticatedGet(collectionsApi)

def getRaindrops(collectionId):
    return authenticatedGet(f'{raindropsApi}/{collectionId}')

# https://api.raindrop.io/v1/raindrops?search=[{"key":"word","val":"swagger"}]
def search(term):
  jar = requests.cookies.RequestsCookieJar()
  jar.set('connect.sid', cookie['connect.sid'])
  queryString={ "search": f'%5B%7B%22key%22%3A%22word%22%2C%22val%22%3A%22{term}%22%7D%5D' }
  # return authenticatedGet(raindropsApi, params=queryString)
  url="https://api.raindrop.io/v1/raindrops?search=[{\"key\":\"word\",\"val\":\"dimension\"}]"
  return requests.get(url=url, cookies=jar, params=queryString).json()