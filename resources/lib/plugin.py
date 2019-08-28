# -*- coding: utf-8 -*-

import routing
import logging
import requests
import re
import urllib
import xbmcaddon
from sys import exit, version_info
from resources.lib import kodiutils
from resources.lib import kodilogging
from xbmcgui import ListItem
from xbmcplugin import addDirectoryItem, endOfDirectory, setResolvedUrl

from resources.lib.channels import RTP_CHANNELS, HEADERS 


if kodiutils.PY3:
    from urllib.parse import urlencode
else:
    from urllib import urlencode


ADDON = xbmcaddon.Addon()
ICON = ADDON.getAddonInfo("icon")
logger = logging.getLogger(ADDON.getAddonInfo('id'))
kodilogging.config()
plugin = routing.Plugin()

@plugin.route('/')
def index():
    # Request dvr
    try:
        req = requests.get("http://www.rtp.pt/play/direto", headers=HEADERS).text
    except:
        raise_notification()

    match = re.compile(r'<a title=".+? - (.+?)" href="/play/direto/(.+?)".*?\n.*?\n.*?<img alt=".+?" src ="(.+?)"').findall(req) #class="item">\n.+?<div class="img-holder">\n.+?<img alt=".+?" src ="(.+?)" class="img-responsive">').findall(req)
    
    for rtp_channel in RTP_CHANNELS:
        dvr = "Not available"
        progimg = ""
        for prog, key, img in match:
            if key.lower() == rtp_channel["id"]:
                dvr = prog
                if img.startswith("/"):
                    img = "http:{}".format(img)
                progimg = img
                break
        
        liz = ListItem("[B][COLOR blue]{}[/B][/COLOR] ({})".format(
            kodiutils.compat_py23str(rtp_channel["name"]),
            kodiutils.compat_py23str(dvr))
        )
        liz.setArt({"thumb": progimg, "icon": progimg, "fanart": kodiutils.FANART})
        liz.setProperty('IsPlayable', 'true')
        liz.setInfo("Video", infoLabels={"plot": kodiutils.compat_py23str(dvr)})
        addDirectoryItem(
            plugin.handle,
            plugin.url_for(
                play,
                label=kodiutils.compat_py23str(rtp_channel["name"]),
                channel=kodiutils.compat_py23str(rtp_channel["id"]),
                img=kodiutils.compat_py23str(progimg),
                prog=kodiutils.compat_py23str(dvr)
            ), liz, False)

    endOfDirectory(plugin.handle)


@plugin.route('/play')
def play():
    channel = plugin.args["channel"][0]
    name = plugin.args["label"][0]
    prog = plugin.args["prog"][0]

    icon = ICON
    if "img" in plugin.args:
        icon = plugin.args["img"][0]


    for rtp_channel in RTP_CHANNELS:
        if rtp_channel["id"] == channel:
            streams = rtp_channel["streams"]
            for stream in streams:
                if stream["type"] == "hls":
                    if requests.head(stream["url"], headers=HEADERS).status_code == 200:
                        liz = ListItem("[B][COLOR blue]{}[/B][/COLOR] ({})".format(
                            kodiutils.compat_py23str(name),
                            kodiutils.compat_py23str(prog))
                        )
                        liz.setArt({"thumb": icon, "icon": icon})
                        liz.setProperty('IsPlayable', 'true')
                        liz.setPath("{}|{}".format(stream["url"], urlencode(HEADERS)))
                        setResolvedUrl(plugin.handle, True, liz)
                        break
                    else:
                        continue


def raise_notification():
    kodiutils.ok(kodiutils.get_string(32000),kodiutils.get_string(32002))
    exit(0)


def run():
    plugin.run()
