# set of general utilities to interact with the Web

# @author: rm3086 (at) columbia (dot) edu

import urllib2
from log import strd_logger

# logger
global log
log = strd_logger ('web')


# get the html source associated to a URL
def download_web_data (url):
    try:
        req = urllib2.Request (url, headers={'User-Agent':"Magic Browser"}) 
        con = urllib2.urlopen(req)
        html = con.read()
        con.close()
        return html
    except Exception as e:
        log.error ('%s: %s' % (e, url))
        return None


# clean the html source
def clean_html (html):
    if html is None:
        return None
    return ' '.join(html.replace('\n','').replace('\t','').split()).strip()