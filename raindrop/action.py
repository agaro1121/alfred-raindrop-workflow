# encoding: utf-8

import sys
from workflow import Workflow, ICON_WEB
# import raindrop_service

def search_key_for_post(bookmark):
     """Generate a string search key for a bookmark"""
     elements = []
     elements.append(bookmark['title'])  # title of bookmark
     elements.append(bookmark['link'])  # bookmark tags
    #  elements.append(bookmark['summary'])  # description
     return u' '.join(elements)

def main(wf):

    # Retrieve bookmarks from cache if available and no more than 60
    # seconds old
    bookmarks = wf.cached_data('bookmarks', raindrop_service.getAllBookmarksParallel2, max_age=5)

    # Get query from Alfred
    if len(wf.args):
        query = wf.args[0]
    else:
        query = None

    if query:
        wf.logger.debug("received query="+query)
        filteredBookmarks = wf.filter(query, bookmarks, key=search_key_for_post)
        # Need to do this for now because filteredBookmarks is full of dupes :-(
        temp = {}
        for bk in filteredBookmarks:
            temp.update({
                bk['title']: bk
            })
        for bookmark in temp.values():
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