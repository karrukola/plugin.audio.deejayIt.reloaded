import re
import urllib2
from lxml import etree as ET

def get_reloaded_list():
#  This returns an array of tuples containing:
#  Program name
#  Thumbnail URL
#  Last episode
#  Date
#   ('Deejay chiama Italia',
#     'http://www.deejay.it/wp-content/uploads/2013/05/DJCI-150x150.jpg',
#     'http://www.deejay.it/audio/20141212-4/412626/',
#     '20141212')

    url = "http://www.deejay.it/reloaded/radio/"
    response = []

    tree = ET.parse(urllib2.urlopen(url), ET.HTMLParser())
    root = tree.getroot()

    #Trova la lista programmi
    #TODO!!! funzione per tradurre la data (come gestisce 2014/2015?)
    #TODO!!! la lista programmi copre più pagine. Funzione ricorsiva?
    prog_list = root.findall(".//ul[@class='block-grid four-up mobile-two-up']/li")

    for prog in prog_list:
        prog_name_url = prog.find("./a").attrib
        response.append(
            (prog_name_url['title'],
            prog.find("./a/img").attrib['src'],
            prog_name_url['href'],
            prog.find("./hgroup/span").text)
            )
    return response


def get_episodi(url, oldimg):
    page = urllib2.urlopen(url).read()
    new_url = re.findall('^.*a\shref="(http.+audio\?.+)".*title.*rchivio.*$',
                         page,
                         re.MULTILINE)
    #addParam('param', 'image', 'http://www.deejay.it/wp-content/uploads/2013/05/cordialmente.jpg');
    new_img = re.findall('addParam\(\'param\', \'image\', \'(http://www\.deejay\.it/wp-content/uploads/.*)\'.*$',
                         page,
                         re.MULTILINE)
    if new_img:
        img = new_img[0]
    else:
        img = oldimg

    if new_url:
        url = new_url[0]
        page = urllib2.urlopen(url).read()

    #programma: TUPLA contente titolo e URL, dall'URL devi caricare ogni pagina per trovare l'indirizzo del file audio
    #<a title="Puntata del 10 Dicembre 2012" href="http://www.deejay.it/audio/20121210-3/271333/"></a>
    episodi = re.findall('^\s*<a\shref="(.*/audio/([0-9]{8}).*)"\s+title="(.*)".*$',
                         page,
                         re.MULTILINE)
    # ('http://www.deejay.it/audio/20071120-2/278354/', '20071120', 'Puntata del 20 Novembre 2007')

    show_reloaded = re.findall('http://www.deejay.it/audio[/page/\d]*\?reloaded=(.*)',
                                url)[0]

    #Passo finale: aggiungi il link alla pagina successiva
    #<a href='http://www.deejay.it/audio/page/2/?reloaded=dee-giallo' class='nextpostslink'></a>

    nextpage = re.findall(
        '<a href=\'(http://www.deejay.it/audio/page/\d+/\?reloaded=' + show_reloaded + ')\' class=\'nextpostslink\'>',
        page,
        re.MULTILINE)
    if nextpage:
        nextpage = nextpage[0]
    else:
        nextpage = ''

    return episodi, nextpage, img


def get_epfile(url):
    page = urllib2.urlopen(url).read()
    fileurl = re.findall('^.*(http.*\.(?:mp3|wma))\s*</p>.*$',
                         page,
                         re.MULTILINE)
    if fileurl:
        out = fileurl[0]
    else:
        out = ''
    return out


programmi = get_reloaded_list()

#    ---------------------------------------------------
for p in programmi:
    print p

#p = programmi[17][2]
#print p
#eps = get_episodi(p)

#eps = get_episodi('http://www.deejay.it/audio/page/13/?reloaded=dee-giallo','')

#fileurl = get_epfile('http://www.deejay.it/audio/20130527-3/269977/')
#print fileurl
