# -*- coding: utf-8 -*-

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
    "Referer": "http://www.rtp.pt/play/"
}

RTP_CHANNELS = [
    {   "id": "rtp1",
        "name" : "adf0348a2551890ed2e9db7cdea27c52",
        "streams": [
            {"type":"hls", "url": "https://streaming-live.rtp.pt/liverepeater/smil:rtp1.smil/playlist.m3u8"},
            {"type":"dashwv", "url": "https://streaming-live.rtp.pt/liverepeater/rtp1.smil/manifest.mpd", "tk": "https://www.rtp.pt/play/direto/rtp1", "license": "https://widevine-proxy.drm.technology/proxy"}
        ]
    },
    {   "id": "rtp2",
        "name" : "67eb6d97b8066c5d693d07d76ad24625",
        "streams": [
            {"type":"hls", "url": "https://streaming-live.rtp.pt/liverepeater/smil:rtp2.smil/playlist.m3u8"},
        ]
    },
    {   "id": "rtp3",
        "name" : "a30daa249f3fa81438bb01a479cd4b75",
        "streams": [
             {"type":"hls", "url": "https://streaming-live.rtp.pt/livetvhlsDVR/rtpndvr.smil/playlist.m3u8?DVR"},
             {"type":"dashwv", "url": "https://streaming-live.rtp.pt/liverepeater/rtpn.smil/manifest.mpd?DVR", "tk": "https://www.rtp.pt/play/direto/rtp3", "license": "https://widevine-proxy.drm.technology/proxy" }
        ] 
    },
    {   "id": "rtpinternacional",
        "name" : "0d91f368ad1305feb514e374cb6e45e21a9b40760a4fd8bd1dd212b0d6923409",
        "streams": [
             {"type":"hls", "url": "https://streaming-live.rtp.pt/liverepeater/smil:rtpi.smil/playlist.m3u8"},
             {"type":"dashwv", "url": "https://streaming-live.rtp.pt/liverepeater/rtpi.smil/manifest.mpd", "tk": "https://www.rtp.pt/play/direto/rtpinternacional", "license": "https://widevine-proxy.drm.technology/proxy" }
        ] 
    },
    {   "id": "rtpmemoria",
        "name" : "9a143915e2070ccb512acd790593ae91",
        "streams": [
             {"type":"hls", "url": "https://streaming-live.rtp.pt/liverepeater/smil:rtpmem.smil/playlist.m3u8"},
             {"type":"dashwv", "url": "https://streaming-live.rtp.pt/liverepeater/rtpmem.smil/manifest.mpd", "tk": "https://www.rtp.pt/play/direto/rtpmemoria", "license": "https://widevine-proxy.drm.technology/proxy" }
        ] 
    },
    {   "id": "rtpmadeira",
        "name" : "b8b31566443b3fec60bdfb42114456b6",
        "streams": [
             {"type":"hls", "url": "https://streaming-live.rtp.pt/liverepeater/smil:rtpmadeira.smil/playlist.m3u8"},
             {"type":"dashwv", "url": "https://streaming-live.rtp.pt/liverepeater/rtpmadeira.smil/manifest.mpd", "tk": "https://www.rtp.pt/play/direto/rtpmadeira", "license": "https://widevine-proxy.drm.technology/proxy" }
        ] 
    },
    {   "id": "rtpacores",
        "name" : "f44142d282a3a53fa0260c5178b8ad1b",
        "streams": [
             {"type":"hls", "url": "https://streaming-live.rtp.pt/liverepeater/smil:rtpacores.smil/playlist.m3u8"},
             {"type":"dashwv", "url": "https://streaming-live.rtp.pt/liverepeater/rtpacores.smil/manifest.mpd", "tk": "https://www.rtp.pt/play/direto/rtpacores", "license": "https://widevine-proxy.drm.technology/proxy" }
        ] 
    },
    {   "id": "rtpafrica",
        "name" : "5a1a462be0d32a590e6d3a3b48f9c821",
        "streams": [
             {"type":"hls", "url": "https://streaming-live.rtp.pt/liverepeater/smil:rtpafrica.smil/playlist.m3u8"},
             {"type":"dashwv", "url": "https://streaming-live.rtp.pt/liverepeater/rtpafrica.smil/manifest.mpd", "tk": "https://www.rtp.pt/play/direto/rtpafrica", "license": "https://widevine-proxy.drm.technology/proxy" }
        ] 
    },
]