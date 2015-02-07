import re
import urllib2
from BeautifulSoup import BeautifulSoup

url = "http://www.deejay.it/audio/20130526-4/269989/"
page = urllib2.urlopen(url)
soup = BeautifulSoup(page)

fileurl = soup.find('div', {'id': 'playerCont'})

print 'fileurl:'
print fileurl

print "fileurl.iframe['src']:"
print fileurl.iframe['src']

hit = re.find("file=(.*.mp3)&",
    fileurl.iframe['src'])

print 'hit:'
print hit


# if not fileurl:
#     return ''
# else:
#     hit = re.findall("file=(.*.mp3)&",
#         fileurl[0].attrib['src'])
#     if not hit:
#         return ''
#     else:
#         return hit[0]
