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
xbmcplugin.addSortMethod(addon_handle,
    sortMethod=xbmcplugin.SORT_METHOD_UNSORTED)
xbmcplugin.addSortMethod(addon_handle,
    sortMethod=xbmcplugin.SORT_METHOD_DATE)
xbmcplugin.addSortMethod(addon_handle,
    sortMethod=xbmcplugin.SORT_METHOD_LABEL)
xbmcplugin.addSortMethod(addon_handle,
    sortMethod=xbmcplugin.SORT_METHOD_PROGRAM_COUNT)


def build_url(query):
    return base_url + '?' + urllib.urlencode(query)


mode = args.get('mode', None)

if mode is None:
    try:
        lista = deejay.get_reloaded_list()
    except IOError or BadStatusLine as e:    #urllib2 errors are a subclass of IOError
        xbmcgui.Dialog().ok(
            __language__(30002),
            __language__(30003),
            str(e.reason))
    else:
        for idx, prog in enumerate(lista):
            url = build_url({'mode': 'epList',
                             'progName': prog[0],
                             'lastReloadedUrl': prog[2],
                             'showThumb': prog[1]})
            #showThumbm, parsata da PROGRAMMI, deve essere usata da play -> inoltrata attraverso i modi
            li = xbmcgui.ListItem(prog[0], iconImage=prog[1])
            li.setInfo('music', {'date': prog[3], 'count': idx})
            xbmcplugin.addDirectoryItem(handle=addon_handle,
                                        url=url,
                                        listitem=li,
                                        isFolder=True)
        xbmcplugin.endOfDirectory(addon_handle)

elif mode[0] == 'epList':
    progName = args['progName'][0]
    lastReloadedUrl = args['lastReloadedUrl'][0]
    showThumb = args['showThumb'][0]
    fanArt = args.get('fanArt')
    
    try:
        episodi, nextpage, img = deejay.get_episodi(url=lastReloadedUrl,
            oldimg=fanArt)
    except IOError or BadStatusLine as e:    #urllib2 errors are a subclass of IOError
        xbmcgui.Dialog().ok(
            __language__(30002),
            __language__(30004),
            str(e.reason))
    else:
        for idx, ep in enumerate(episodi):
            #('http://www.deejay.it/audio/20071120-2/278354/', '20071120', 'Puntata del 20 Novembre 2007')
            url = build_url({'mode': 'play',
                             'epUrl': ep[0],
                             'showThumb': showThumb,
                             'title': ep[2],
                             'progName': progName})
            li = xbmcgui.ListItem(ep[2],
                                  iconImage='DefaultAudio.png')
            li.setProperty('IsPlayable', 'true')
            #Setting fanArt
            #not using setArt to keep Frodo's compatibility
            #li.setArt({'fanart' : img})
            li.setProperty('fanart_image', img)        
            li.setInfo('music', {'date': ep[1], 'count': idx})
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
    try:
        url = deejay.get_epfile(args['epUrl'][0])
    except IOError or BadStatusLine as e:    #urllib2 errors are a subclass of IOError
        xbmcgui.Dialog().ok(
            __language__(30002),
            __language__(30005),
            str(e.reason))
    else:
        item = xbmcgui.ListItem(path=url)
        item.setThumbnailImage(args['showThumb'][0])
        item.setInfo('music', {'title': args['title'][0],
                               'album': args['progName'][0],
                               'artist': 'Radio Deejay'})
        xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
        xbmcplugin.endOfDirectory(addon_handle)
