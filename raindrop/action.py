# encoding: utf-8

import sys
import argparse
from workflow import Workflow, ICON_WEB, ICON_WARNING
from workflow.notify import notify
import utilities

def search_key_for_post(bookmark):
     """Generate a string search key for a bookmark"""
     elements = []
     elements.append(bookmark['title'])  # title of bookmark
    #  elements.append(bookmark['link'])  # bookmark tags
    #  elements.append(bookmark['summary'])  # description
     return u' '.join(elements)

def main(wf):
    parser = argparse.ArgumentParser()

    # usage: script.py -e aa@bb.com -p some-password
    parser.add_argument('-e', '--email', default=None)
    parser.add_argument('-p', '--password', default=None)
    # add an optional query and save it to 'query'
    parser.add_argument('--query', dest='query', nargs='?')
    args = parser.parse_args(wf.args)

    if args.email and args.password:
        utilities.upsertCredentialsFile(args.email, args.password)
        raindrop_service.persistCookies()
        if not utilities.hasValidCookie():
            print("Could not login. Please try again")
            return 0
        else:
            print("Successfully logged in!")
            return 0

    # Check if user has credentials and a cookie that hasn't expired yet
    if not utilities.hasCredentials():
        wf.add_item(title="You are not logged in",
                    subtitle="Please use: brlogin email password",
                    valid=True,
                    icon=ICON_WARNING)
        wf.send_feedback()
        return 0
    else:
        # Refresh cookie if something is wrong or it's expired
        if not utilities.hasValidCookie():
            raindrop_service.persistCookies()
        
        # TODO: cache bookmarks
        query=args.query
        wf.logger.debug("received query="+query)

        bookmarks = wf.cached_data('bookmarks', raindrop_service.getAllBookmarksParallel, max_age=60)

        if len(query) > 0:    
            # filteredBookmarks = raindrop_service.search(query)
            filteredBookmarks = wf.filter(query, bookmarks, key=search_key_for_post)
            for bookmark in filteredBookmarks:
                wf.add_item(title=bookmark['title'],
                        subtitle=bookmark['summary'],
                        icon=ICON_WEB,
                        valid=True,
                        arg=bookmark['link'])
            # Send the results to Alfred as XML
            wf.send_feedback()

if __name__ == u"__main__":
    wf = Workflow(libraries=['./lib'])
    import raindrop_service
    sys.exit(wf.run(main))