import re
import urllib2
from BeautifulSoup import BeautifulSoup


def get_podcast():
    url = 'http://www.deejay.it/podcast/radio/'
    soup = BeautifulSoup(urllib2.urlopen(url))
    lista = []
    podcast_section = soup.find('div', {'class': 'article-list'})
    article_list = podcast_section.findAll('article')

    for art in article_list:
        podcast = []
        shows = art.findAll('li')
        for show in shows:
            titolo = show.find('a')['title']
            indirizzo = show.find('a')['href']
            # print titolo
            # print indirizzo
            podcast.append(
                (titolo, indirizzo)
                )

        dataAstrale = art.find('span', {'class': 'hour'}).text
        pic = art.find('img')['src']
        titolo = art.find('a')['title']
        indirizzo = art.find('a')['href']

        lista.append(
            (titolo,
            indirizzo,
            dataAstrale,
            pic,
            podcast)
        )
    return lista


P = get_podcast()
p = P[4]
print p




