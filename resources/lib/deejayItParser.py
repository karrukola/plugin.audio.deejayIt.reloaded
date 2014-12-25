import re
import urllib2
from lxml import etree as ET
import dateUtils
import datetime

NOW = datetime.datetime.now()
ANNO = NOW.year
MESE = NOW.month
GIORNO = NOW.day

def translatedate(eptitle):
    #eptitle is, normally, Puntata del 3 Gennaio 2014
    hit = re.findall("(Puntata*)*([0-9]{1,2}) (\S*)\s*([0-9]{4})*",
        eptitle,
        re.MULTILINE)
    if hit:
        mese = dateUtils.monthToNum(hit[0][2])
        giorno = hit[0][1]
        if hit[0][3]:
            anno = hit[0][3]
        else:
            anno = ANNO
        translateddate = str(anno)+str(mese).rjust(2, '0')+giorno.rjust(2, '0')

        #Sometimes the year is not given, this part checks whether the #returned date is in the future and eventually adjusts it.
        #This works under the hypotesis that the website never returns a date #in the future
        today = str(ANNO)+str(MESE).rjust(2, '0')+str(GIORNO).rjust(2, '0')
        if translateddate > today:
            translateddate = str(int(translateddate[0:4])-1) + translateddate[4:]
    else:
        translateddate = ''

    return translateddate

def get_reloaded_list_in_page(url, response):
#  This returns an array of tuples containing:
#  (Program name,
#  Thumbnail URL,
#  Last episode,
#  Date)
#   ('Deejay chiama Italia',
#     'http://www.deejay.it/wp-content/uploads/2013/05/DJCI-150x150.jpg',
#     'http://www.deejay.it/audio/20141212-4/412626/',
#     '20141212')
# from a single page of the website

    root = ET.parse(urllib2.urlopen(url), ET.HTMLParser()).getroot()
    prog_list = root.xpath(".//ul[@class='block-grid four-up mobile-two-up']/li")
    for prog in prog_list:
        prog_name_url = prog.xpath("./a")[0].attrib
        response.append(
            (prog_name_url['title'],
                prog.xpath("./a/img")[0].attrib['src'],
                prog_name_url['href'],
                translatedate(prog.xpath("./hgroup/span")[0].text))
            )
    nextpage = root.xpath(".//a[@class='nextpostslink']")
    if not nextpage:
        nextpageurl = ''
    else:
        nextpageurl = nextpage[0].attrib['href']

    return response, nextpageurl


def get_reloaded_list():
#  This crawls over all the pages to return the complete list of reloaded shows
#  This returns an array of tuples containing:
#  (Program name,
#  Thumbnail URL,
#  Last episode,
#  Date)
#   ('Deejay chiama Italia',
#     'http://www.deejay.it/wp-content/uploads/2013/05/DJCI-150x150.jpg',
#     'http://www.deejay.it/audio/20141212-4/412626/',
#     '20141212')

    url = "http://www.deejay.it/reloaded/radio/"
    lista, nextpageurl = get_reloaded_list_in_page(url, [])
    while nextpageurl:
        lista, nextpageurl = get_reloaded_list_in_page(nextpageurl, lista)

    return lista

def get_episodi(url, oldimg):
    root = ET.parse(urllib2.urlopen(url), ET.HTMLParser()).getroot()

    if oldimg:
        img = oldimg
    else:
        snippet = root.xpath(".//article[@class='twelve columns video player audio']/script")
        if snippet is not None:
            new_img = re.findall(".*addParam.*'param', 'image', '(http://www.deejay.it/.*)'.*",
                snippet[0].text,
                re.MULTILINE)
            if new_img:
                img = new_img[0]
        else:
            img = ''

    new_url = root.xpath(".//span[@class='small-title']/a")
    if new_url is not None:
        root = ET.parse(urllib2.urlopen(new_url[0].attrib['href']),
            ET.HTMLParser()).getroot()
    lista_episodi = []
    episodi = root.xpath(".//ul[@class='lista']/li/a")

    if episodi is not None:
        for episodio in episodi:
            lista_episodi.append(
                (
                    episodio.attrib['href'],
                    translatedate(episodio.attrib['title']),
                    episodio.attrib['title'])
                )

    #Passo finale: aggiungi il link alla pagina successiva
    nextpage = root.xpath(".//a[@class='nextpostslink']")
    if nextpage is None:
        nextpageurl = ''
    else:
        nextpageurl = nextpage[0].attrib['href']

    return lista_episodi, nextpageurl, img

def get_epfile(url):
    root = ET.parse(urllib2.urlopen(url), ET.HTMLParser()).getroot()
    fileurl = root.xpath(".//div[@id='playerCont']/p")

    if fileurl is not None:
        return fileurl[0].text
    else:
        return ''


#    ---------------------------------------------------
#PROGRAMMI = get_reloaded_list()
#for p in PROGRAMMI:
#    print p

#p = PROGRAMMI[17][2]
#print p

#eps = get_episodi('http://www.deejay.it/audio/page/13/?reloaded=dee-giallo', '')
#eps = get_episodi('http://www.deejay.it/audio/20141215-10/412901/','')
#eps = get_episodi('http://www.deejay.it/audio/20141223-2/414155/', 'pippo')
#for e in eps:
#    print e

#fileurl = get_epfile('http://www.deejay.it/audio/20130527-3/269977/')
#print fileurl

#dataAstrale = translatedate('15 Dicembre')
#print dataAstrale
