import re
import urllib2
from BeautifulSoup import BeautifulSoup

url = "http://www.deejay.it/audio/page/13/?reloaded=dee-giallo"
#url = "http://www.deejay.it/reloaded/radio/"
page = urllib2.urlopen(url)
soup = BeautifulSoup(page)

episodi = soup.find('ul', {'class': 'lista'}).findAll('li')

episodio = episodi[3]
print "episodio.a['href']:"
print episodio.a['href']
print "episodio.a['title']:"
print episodio.a['title']

# for episodio in episodi:
#     lista_episodi.append(
#         (
#             episodio.a['href'],
#             translate_date(episodio.a['title']),
#             episodio.a['title'])
#     #             )
#             )


    #episodi = root.xpath(".//ul[@class='lista']/li/a")
    # if episodi:
    #     for episodio in episodi:
    #         lista_episodi.append(
    #             (
    #                 episodio.attrib['href'],
    #                 translate_date(episodio.attrib['title']),
    #                 episodio.attrib['title'])
    #             )

    # #Passo finale: aggiungi il link alla pagina successiva
    # nextpage = root.xpath(".//a[@class='nextpostslink']")
    # if not nextpage:
    #     nextpageurl = ''
    # else:
    #     nextpageurl = nextpage[0].attrib['href']
    # return lista_episodi, nextpageurl, img
