#!/usr/bin/python
# Writer (c) 2012, MrStealth
# Rev. 1.0.6
# -*- coding: utf-8 -*-

import os, sys, urllib2, socket
import xbmcgui, xbmcaddon, xbmcplugin

import HTMLParser
import  CommonFunctions

common = CommonFunctions
common.plugin = "plugin.video.iptv5.ts9.ru"

handle = int(sys.argv[1])

__addon__ = xbmcaddon.Addon(id='plugin.video.iptv5.ts9.ru')
__language__ = __addon__.getLocalizedString
addon_icon    = __addon__.getAddonInfo('icon')
addon_path    = __addon__.getAddonInfo('path')

# TODO Replace by commonParse function
def unescape(entity, encoding):
    if encoding == 'utf-8':
        return HTMLParser.HTMLParser().unescape(entity).encode(encoding)
    elif encoding == 'cp1251':
        return HTMLParser.HTMLParser().unescape(entity).decode(encoding).encode('utf-8')

def check_url(url):
    if not url.find("rtsp") == -1 or not url.find("inetcom") == -1: # skip rtsp and authenticated
        return []
    try:
        response = urllib2.urlopen(url, None, 2)
        return {'url':response.geturl(), 'mimetype':response.info()['Content-type']}
    except urllib2.HTTPError, e:
        return []
    except urllib2.URLError, e:
        return []
    except socket.timeout, e:
        return []
    except:
        return []
    else:
        return url

def xbmcItem(mode, url, title, icon=False, category=False):
    uri = sys.argv[0] + '?mode='+ mode + '&url=' + url
    if not icon: icon = addon_icon
    if title: uri += '&title=' + title
    if category: uri += '&category=' + category

    item = xbmcgui.ListItem(title, iconImage=icon, thumbnailImage=icon)
    item.setProperty('IsPlayable', 'false')
    xbmcplugin.addDirectoryItem(handle, uri, item, True)


def xbmcPlayableItem(mode, title, url, action, mimetype=False):
    print action
    uri = sys.argv[0] + '?mode='+ mode + '&url=' + url

    item = xbmcgui.ListItem(title, iconImage=addon_icon, thumbnailImage=addon_icon)
    item.setInfo(type='Video', infoLabels = {'title': title})
    item.setProperty('IsPlayable', 'true')

    if action == 'add':
        label = __language__(1001)
    else:
        label = __language__(1002)

    xbmcContextMenuItem(item, action, label, url, title)
    xbmcplugin.addDirectoryItem(handle, uri, item)

def xbmcContextMenuItem(item, action, label, url, title):
    script = "special://home/addons/plugin.video.iptv5.ts9.ru/contextmenu.py"
    params = action + "|%s"%url + "|%s"%title
    runner = "XBMC.RunScript(" + str(script)+ ", " + params + ")"
    item.addContextMenuItems([(label, runner)])
