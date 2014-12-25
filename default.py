import sys
import urllib
import urlparse

import xbmcgui
import xbmcplugin
import resources.lib.deejayItParser as deejay
import xbmcaddon


__settings__ = xbmcaddon.Addon(id='plugin.audio.deejayIt.reloaded')
__language__ = __settings__.getLocalizedString


base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

xbmcplugin.setContent(addon_handle, 'episodes')
xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_UNSORTED)
xbmcplugin.addSortMethod(addon_handle, xbmcplugin.SORT_METHOD_DATE)


def build_url(query):
    return base_url + '?' + urllib.urlencode(query)


mode = args.get('mode', None)

if mode is None:
    for prog in deejay.get_reloaded_list():
        url = build_url({'mode': 'epList',
                         'progName': prog[0],
                         'lastReloadedUrl': prog[2],
                         'showThumb': prog[1],
                         'fanArt': ['']})
        #showThumbm, parsata da PROGRAMMI, deve essere usata da play -> inoltrata attraverso i modi
        li = xbmcgui.ListItem(prog[0], iconImage=prog[1])
        li.setInfo('music', {'date': prog[3]})
        xbmcplugin.addDirectoryItem(handle=addon_handle,
                                    url=url,
                                    listitem=li,
                                    isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'epList':
    progName = args['progName'][0]
    lastReloadedUrl = args['lastReloadedUrl'][0]
    showThumb = args['showThumb'][0]
    fanArt = args['fanArt'][0]

    episodi, nextpage, img = deejay.get_episodi(url=lastReloadedUrl,
        oldimg=fanArt)
    for ep in episodi:
        #('http://www.deejay.it/audio/20071120-2/278354/', '20071120', 'Puntata del 20 Novembre 2007')
        url = build_url({'mode': 'play',
                         'epUrl': ep[0],
                         'showThumb': showThumb,
                         'title': ep[2],
                         'progName': progName})
        #Per alcuni episodi (e.g. Deejay Chiama Italia 2014-05-06) la cartella non ha il nome atteso, anno dato come 2015
        data = ep[1][6:8] + '.' + ep[1][4:6] + '.' + ep[2][-4:]
        li = xbmcgui.ListItem(ep[2],
                              iconImage='DefaultAudio.png')
        li.setProperty('IsPlayable', 'true')
        li.setProperty('fanart_image', img)
        li.setInfo('music', {'date': data})
        xbmcplugin.addDirectoryItem(handle=addon_handle,
                                    url=url,
                                    listitem=li)

    if nextpage:
        #Questo aggiunge la prossima pagina
        url = build_url({'mode': 'epList',
                         'progName': progName,
                         'lastReloadedUrl': nextpage,
                         'showThumb': showThumb,
                         'fanArt': img})
        li = xbmcgui.ListItem('>>> '+__language__(30001)+' >>>')
        xbmcplugin.addDirectoryItem(handle=addon_handle,
                                    url=url,
                                    listitem=li,
                                    isFolder=True)

    # e chiudiamo la lista
    xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'play':
    url = deejay.get_epfile(args['epUrl'][0])
    item = xbmcgui.ListItem(path=url)
    item.setThumbnailImage(args['showThumb'][0])
    item.setInfo('music', {'title': args['title'][0],
                           'album': args['progName'][0],
                           'artist': 'Radio Deejay'})
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
    xbmcplugin.endOfDirectory(addon_handle)
