import sys
import urllib
import urlparse
import xbmc
import xbmcgui
import xbmcplugin
from resources.lib.deejay_it_parser import DeejayItParser


def build_url(query):
    base_url = sys.argv[0]
    return base_url + '?' + urllib.urlencode(query)


def show_mode_choice():
    for op_mode in ['reloaded', 'podcast']:
        xbmcplugin.addDirectoryItem(
            handle=ADDON_HANDLE,
            url=build_url({'mode': op_mode}),
            listitem=xbmcgui.ListItem(op_mode.upper()),
            isFolder=True
        )
    xbmcplugin.endOfDirectory(ADDON_HANDLE)


def build_reloaded_list(shows):
    show_list = []
    for show in shows:
        li = xbmcgui.ListItem(label=shows[show]['title'],
                              iconImage=shows[show]['icon'])
        # set the fanart to the albumc cover
        li.setProperty('fanart_image',
                       shows[show]['art'])
        url = build_url({'mode': 'reloadedEpList',
                         'pid': shows[show]['pid'],
                         'rid': shows[show]['rid'],
                         'art': shows[show]['art'],
                         'icon': shows[show]['icon'],
                         'speakers': shows[show]['speakers'],
                         'show_name': shows[show]['title'].encode("ascii",
                                                                  "ignore")})
        # this is still a folder, so isFolder must be True
        show_list.append((url, li, True))
    xbmcplugin.addDirectoryItems(ADDON_HANDLE,
                                 show_list,
                                 len(show_list))
    xbmcplugin.endOfDirectory(ADDON_HANDLE)


def adj_title(testo):
    try:
        int(testo)
        return 'Puntata del %s-%s-%s' % (testo[6:8], testo[4:6], testo[0:4])
    except ValueError:
        return testo


def build_episodes_list(episodes, icon, art, show_name, speakers):
    ep_list = []
    for ep in episodes:
        ep_title = adj_title(episodes[ep]['title'])
        li = xbmcgui.ListItem(label=ep_title,
                              iconImage=icon)
        li.setProperty('fanart_image', art)
        li.setProperty('IsPlayable', 'true')
        li.setInfo('music', {'date': episodes[ep]['date'],
                             'count': ep})
        url = build_url({'mode': 'stream',
                         'url': episodes[ep]['file'],
                         'thumb': icon,
                         'ep_title': ep_title,
                         'show_name': show_name,
                         'speakers': speakers})
        ep_list.append((url, li, False))
    xbmcplugin.addDirectoryItems(ADDON_HANDLE, ep_list, len(ep_list))
    xbmcplugin.setContent(ADDON_HANDLE, 'songs')
    xbmcplugin.endOfDirectory(ADDON_HANDLE)


def play_song(url, thumb, ep_title, show_name, speakers):
    play_item = xbmcgui.ListItem(path=url)
    play_item.setThumbnailImage(thumb)
    play_item.setInfo('music', {'title': ep_title,
                                'album': show_name,
                                'artist': speakers})
    xbmcplugin.setResolvedUrl(ADDON_HANDLE, True, listitem=play_item)


def main():
    args = urlparse.parse_qs(sys.argv[2][1:])
    mode = args.get('mode', None)

    if mode is None:
        show_mode_choice()
    elif mode[0] == 'reloaded':
        deejay = DeejayItParser()
        build_reloaded_list(deejay.get_reloaded_list())
    elif mode[0] == 'reloadedEpList':
        deejay = DeejayItParser()
        ep_data = deejay.get_episodes(pid=args.get('pid', None)[0],
                                      rid=args.get('rid', None)[0],
                                      ep_type='reloaded')
        build_episodes_list(ep_data,
                            icon=args.get('icon', None)[0],
                            art=args.get('art', None)[0],
                            show_name=args.get('show_name', None)[0],
                            speakers=args.get('speakers')[0])

    elif mode[0] == 'stream':
        play_song(url=args['url'][0],
                  thumb=args.get('thumb')[0],
                  ep_title=args.get('ep_title')[0],
                  show_name=args.get('show_name')[0],
                  speakers=args.get('speakers')[0])


if __name__ == '__main__':
    ADDON_HANDLE = int(sys.argv[1])
    main()
