import re
import urllib2
from BeautifulSoup import BeautifulSoup
import datetime

NOW = datetime.datetime.now()
ANNO = NOW.year
MESE = NOW.month
GIORNO = NOW.day

def month_to_num(date):
    """
    Translate the month name (string) to its corresponding number.
    Strings are written only in Italian since this module is used to parse
    Radio Deejay's website (www.deejay.it).
    Input
        The month name, epxressed in Italian, e.g. Dicembre
    Output
        The corresponding month number, e.g. 12
    """
    return{
    'Gennaio' : 1,
    'gennaio' : 1,
    'Febbraio' : 2,
    'febbraio' : 2,
    'Marzo' : 3,
    'marzo' : 3,
    'Aprile' : 4,
    'aprile' : 4,
    'Maggio' : 5,
    'maggio' : 5,
    'Giugno' : 6,
    'giugno' : 6,
    'Luglio' : 7,
    'luglio' : 7,
    'Agosto' : 8,
    'agosto' : 8,
    'Settembre' : 9,
    'settembre' : 9,
    'Ottobre' : 10,
    'ottobre' : 10,
    'Novembre' : 11,
    'novembre' : 11,
    'Dicembre' : 12,
    'dicembre' : 12
    }[date]


def translate_date(ep_title):
    """
    Translate the date in the episode's title and return it in the format used
    by Kodi.
    Input
        ep_title is the episode's title, such as Puntata del 3 Gennaio 2014.
        But it could also be Puntata del 3 Gennaio
    Output
        translated_date formatted as dd.mm.YYYY
    Fallback, in case the title is not understood, is 19.12.1982. This should
    be the first day on which a DJ, Gerry Scotty in this case, was speaking.
    """
    #ep_title is, normally, Puntata del 3 Gennaio 2014
    hit = re.findall(r"(Puntata*)*([0-9]{1,2}) (\S*)\s*([0-9]{4})*",
        ep_title,
        re.MULTILINE)
    if hit:
        mese = month_to_num(hit[0][2])
        giorno = hit[0][1]
        if hit[0][3]:
            anno = hit[0][3]
        else:
            anno = ANNO
        data_ep = str(anno)+str(mese).rjust(2, '0')+giorno.rjust(2, '0')
        #Sometimes the year is not given, this part checks whether the returned
        #date is in the future and eventually adjusts it.
        #This works under the hypotesis that the website never returns a date
        #in the future
        today = str(ANNO)+str(MESE).rjust(2, '0')+str(GIORNO).rjust(2, '0')
        if data_ep > today:
            data_ep = str(int(data_ep[0:4])-1) + data_ep[4:]
        translated_date = data_ep[6:8]+'.'+data_ep[4:6]+'.'+data_ep[0:4]
    else:
        #19 dicembre 1982: primo intervento del Gerry Scotti speaker
        translated_date = '19.12.1982'
    return translated_date



url = 'http://www.deejay.it/audio/?podcast=deejay-chiama-italia'
soup = BeautifulSoup(urllib2.urlopen(url))

dataAstrale = '19.12.1982'
episodi = soup.find('ul', {'class': 'lista podcast-archive'}).findAll('li')
for ep in episodi:
    print ep
    print ep.a['title']
    tmp = ep.find('span', {'class': 'small-title red'})
    if tmp is not None:
        dataAstrale = tmp.text
    print dataAstrale
    print translate_date(dataAstrale)

# dataAstrale = episodi.findAll('span', {'class': 'small-title red'})
# print dataAstrale

# date = []
# for d in dataAstrale:
#     tmp = d.text
#     print tmp
#     date.append(tmp)

