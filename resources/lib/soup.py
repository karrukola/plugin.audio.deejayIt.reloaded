import urllib2
from BeautifulSoup import BeautifulSoup

url = "http://www.deejay.it/reloaded/radio/"

reloaded_list = []

def translate_date(ep_title):
    return ep_title


page = urllib2.urlopen(url)
soup = BeautifulSoup(page)

prog_list = soup.find('ul', {'class': 'block-grid four-up mobile-two-up'}).findAll('li')

# prog = prog_list[2]
# prog_name_url = prog.a
# print 'titolo:'
# print prog_name_url['title']
# print 'immagine:'
# print prog.img['src']
# print 'url:'
# print prog_name_url['href']
# print 'data:'
# dataAstrale = prog.hgroup.span.string
# print dataAstrale

# <a href="http://www.deejay.it/audio/20150111/415405/" title="Weejay">
# <img src="http://www.deejay.it/wp-content/uploads/2013/09/WEEJAY-150x150.jpg" alt="Weejay" />
# </a>


for prog in prog_list:
    prog_name_url = prog.a
    reloaded_list.append(
        (prog_name_url['title'],
            prog.img['src'],
            prog_name_url['href'],
            translate_date(prog.hgroup.span.string))
        )

for reloaded in reloaded_list:
    print reloaded

nextpage = soup.find('a', {'class': 'nextpostslink'})
if not nextpage:
    nextpageurl = ''
else:
    nextpageurl = nextpage['href']

print 'nextpageurl:'
print nextpageurl


# for prog in prog_list :
#     print prog


# for prog in prog_list:
#     prog_name_url = prog.xpath("./a")[0].attrib
#     reloaded_list.append(
#         (prog_name_url['title'],
#             prog.xpath("./a/img")[0].attrib['src'],
#             prog_name_url['href'],
#             translate_date(prog.xpath("./hgroup/span")[0].text))
#         )
# nextpage = root.xpath(".//a[@class='nextpostslink']")
