import re
import urllib2
from lxml import etree as ET
import date_utils
import datetime

NOW = datetime.datetime.now()
ANNO = NOW.year
MESE = NOW.month
GIORNO = NOW.day

def translate_date(ep_title):
    """
    Translate the date in the episode's title and return it in the format used
    by Kodi.
    Input
        ep_title is the episode's title, such as Puntata del 3 Gennaio 2014.
        But it could also be Puntata del 3 Gennaio
    Output
        translated_date formatted as dd.mm.YYYY
    Fallback, in case the title is not understood, is 19.12.1982. This should be
    the first day on which a DJ, Gerry Scotty in this case, was speaking.
    """
    #ep_title is, normally, Puntata del 3 Gennaio 2014
    hit = re.findall("(Puntata*)*([0-9]{1,2}) (\S*)\s*([0-9]{4})*",
        ep_title,
        re.MULTILINE)
    if hit:
        mese = date_utils.month_to_num(hit[0][2])
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

def get_reloaded_list_in_page(url, reloaded_list):
    """
    Return all the available reloaded shows from a single webpage.
    The list is appended to an array of tuples carrying:
    (Program name,
        Thumbnail URL,
        Last episode,
        Date)
    Input
        url of the webpage, e.g.:
        http://www.deejay.it/schede-reloaded/page/2/?section=radio
        reloaded_list, an array of tuples carrying the list of shows returned by
        another parsing operation
    Output
        The above-mentioned array of tuples.
    Single element example:
    ('Deejay chiama Italia',
        http://www.deejay.it/wp-content/uploads/2013/05/DJCI-150x150.jpg',
        'http://www.deejay.it/audio/20141212-4/412626/',
        '19.12.1982')
    """

    root = ET.parse(urllib2.urlopen(url), ET.HTMLParser()).getroot()
    prog_list = root.xpath(".//ul[@class='block-grid four-up mobile-two-up']/li")
    for prog in prog_list:
        prog_name_url = prog.xpath("./a")[0].attrib
        reloaded_list.append(
            (prog_name_url['title'],
                prog.xpath("./a/img")[0].attrib['src'],
                prog_name_url['href'],
                translate_date(prog.xpath("./hgroup/span")[0].text))
            )
    nextpage = root.xpath(".//a[@class='nextpostslink']")
    if not nextpage:
        nextpageurl = ''
    else:
        nextpageurl = nextpage[0].attrib['href']

    return reloaded_list, nextpageurl


def get_reloaded_list():
    """
    Crawl over all the pages to return the complete list of reloaded shows.
    This returns an array of tuples containing the following info for all the
    reloaded shows:
    (Program name,
        Thumbnail URL,
        Last episode,
        Date)
    Input:
        None
    Output
        The above-mentioned array
    E.g.:
    ('Deejay chiama Italia',
        'http://www.deejay.it/wp-content/uploads/2013/05/DJCI-150x150.jpg',
        'http://www.deejay.it/audio/20141212-4/412626/',
        '12.12.2014')
    """
    #hardcoded url
    url = "http://www.deejay.it/reloaded/radio/"
    lista, nextpageurl = get_reloaded_list_in_page(url, [])
    while nextpageurl:
        lista, nextpageurl = get_reloaded_list_in_page(nextpageurl, lista)
    return lista

def get_episodi(url, oldimg):
    root = ET.parse(urllib2.urlopen(url), ET.HTMLParser()).getroot()
    if oldimg is not None:
        img = oldimg[0]
    else:
        snippet = root.xpath(".//article[@class='twelve columns video player audio']/script")
        if snippet:
            new_img = re.findall(".*addParam.*'param', 'image', '(http://www.deejay.it/.*)'.*",
                snippet[0].text,
                re.MULTILINE)
            if new_img:
                img = new_img[0]
        else:
            img = ''

    new_url = root.xpath(".//span[@class='small-title']/a")
    if new_url:
        root = ET.parse(urllib2.urlopen(new_url[0].attrib['href']),
            ET.HTMLParser()).getroot()
    lista_episodi = []
    episodi = root.xpath(".//ul[@class='lista']/li/a")

    if episodi:
        for episodio in episodi:
            lista_episodi.append(
                (
                    episodio.attrib['href'],
                    translate_date(episodio.attrib['title']),
                    episodio.attrib['title'])
                )

    #Passo finale: aggiungi il link alla pagina successiva
    nextpage = root.xpath(".//a[@class='nextpostslink']")
    if not nextpage:
        nextpageurl = ''
    else:
        nextpageurl = nextpage[0].attrib['href']
    return lista_episodi, nextpageurl, img

def get_epfile(url):
    root = ET.parse(urllib2.urlopen(url), ET.HTMLParser()).getroot()
    fileurl = root.xpath(".//div[@id='playerCont']/p")
    if not fileurl:
        return ''
    else:
        return fileurl[0].text


#    ---------------------------------------------------
#PROGRAMMI = get_reloaded_list()
#for p in PROGRAMMI:
#    print p

#p = PROGRAMMI[17][2]
#print p

#eps = get_episodi('http://www.deejay.it/audio/page/13/?reloaded=dee-giallo','')
#eps = get_episodi('http://www.deejay.it/audio/20141215-10/412901/','')
#eps = get_episodi('http://www.deejay.it/audio/20141223-2/414155/', 'pippo')
#for e in eps:
#    print e

#fileurl = get_epfile('http://www.deejay.it/audio/20130527-3/269977/')
#print fileurl

#dataAstrale = translate_date('15 Dicembre')
#print dataAstrale
