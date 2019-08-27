# -*- coding: utf-8 -*-

import routing
import logging
import requests
import inputstreamhelper
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
    from Cryptodome.Cipher import AES
    from Cryptodome.Util import Padding
    
    if kodiutils.PY3:
        key = b'0123456789abcdef'
        IV = 16 * b'\x00'
    else:
        key = '0123456789abcdef'
        IV = 16 * '\x00'

    mode = AES.MODE_CBC
    encryptor = AES.new(key, mode, IV=IV)
    
    for rtp_channel in RTP_CHANNELS:
        if kodiutils.PY3:
            decrypted_channel_name = str(Padding.unpad(encryptor.decrypt(bytes.fromhex(rtp_channel["name"])), 16), "utf-8")
        else:
            decrypted_channel_name = Padding.unpad(encryptor.decrypt(rtp_channel["name"].decode("hex")), 16)
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
            kodiutils.compat_py23str(decrypted_channel_name),
            kodiutils.compat_py23str(dvr))
        )
        liz.setArt({"thumb": progimg, "icon": progimg, "fanart": kodiutils.FANART})
        liz.setProperty('IsPlayable', 'true')
        liz.setInfo("Video", infoLabels={"plot": kodiutils.compat_py23str(dvr)})
        addDirectoryItem(
            plugin.handle,
            plugin.url_for(
                play,
                label=kodiutils.compat_py23str(decrypted_channel_name),
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
                elif stream["type"] == "dashwv":
                    is_helper = inputstreamhelper.Helper('mpd', drm='com.widevine.alpha')
                    if is_helper.check_inputstream():
                        # Grab token
                        src = requests.get(stream["tk"], headers=HEADERS).text
                        tk = re.compile('k: \"(.+?)\"', re.DOTALL).findall(src)
                        if tk:
                            payload = '{"drm_info":[D{SSM}], "kid": "E13506F7439BEAE7DDF0489FCDDF7481", "token":"' + tk[0] + '"}'
                            liz = ListItem("[B][COLOR blue]{}[/B][/COLOR] ({})".format(
                                kodiutils.compat_py23str(name),
                                kodiutils.compat_py23str(prog))
                            )
                            liz.setPath(stream["url"])
                            liz.setProperty('inputstream.adaptive.license_type', 'com.widevine.alpha')
                            liz.setProperty('inputstream.adaptive.manifest_type', 'mpd')
                            liz.setProperty('inputstreamaddon', 'inputstream.adaptive')
                            liz.setProperty('inputstream.adaptive.stream_headers', urlencode(HEADERS))
                            liz.setMimeType('application/dash+xml')
                            liz.setProperty('inputstream.adaptive.license_key', '{}|{}|{}|'.format(stream["license"], "Content-Type=application/json", urllib.quote(payload)))
                            liz.setContentLookup(False)
                            setResolvedUrl(plugin.handle, True, liz)


def raise_notification():
    kodiutils.ok(kodiutils.get_string(32000),kodiutils.get_string(32002))
    exit(0)


def run():
    plugin.run()
