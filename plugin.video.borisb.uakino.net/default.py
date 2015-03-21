#!/usr/bin/python
# -*- coding: utf-8 -*-

# Open issues:
# - Series with multiple seasons: http://uakino.net/video/176035-skazochnaya-rus-5-sezon-42-seriya.html

import urllib
import urllib2
import urlparse
import re
from datetime import date
import time
import string
import XbmcHelpers
from BeautifulSoup import BeautifulSoup

from xbmcswift2 import Plugin

BASEURL = "http://uakino.net/"

common = XbmcHelpers
plugin = Plugin()

def get_page(url):
	req = urllib2.Request(url, headers={ 'User-Agent': 'Mozilla/5.0' })
	html = urllib2.urlopen(req).read()
	return html

@plugin.route('/')
def index():
	html = get_page(BASEURL + "video")
	
	soup = BeautifulSoup(html)
	categories = soup('div', {'data-type' : 'categories'})
	print categories
	matches = re.findall('<a href="(.+?)">(.+?)</a>', str(categories))
	items = []
	for match in matches:
		if match[0] == 'javascript:':
			continue
		items.append({	
			'label': match[1],
			'path': plugin.url_for("getSubcategories", url = BASEURL + match[0], offset = 0),
		})
	#xbmc.executebuiltin('Container.SetViewMode(50)')
	return plugin.finish(items)

@plugin.route('/category/<url>/<offset>')
def getSubcategories(url, offset):
	print "getSubcategories(url, offset):"
	print "    url    = " + url
	print "    offset = " + offset
	if offset == 0:
		html = get_page(url)
	else:
		html = get_page("%s?order=date&offset=%s"%(url, offset))
	
	matches = re.findall('<a href="(.+?)" class="fleft thumb"><img src="(.+?)".+?title="(.*)"', html)
	items = [{	
		'label': title,
		'thumbnail': thumbnail,
		'path': plugin.url_for("getSeries", url = BASEURL + uri, offset = 0),
	} for uri, thumbnail, title in matches]
	
	items.append({
		'label': 'Next',
		'path': plugin.url_for("getSubcategories", url = url, offset = int(offset) + 16),
	})
	
	return plugin.finish(items)
	
@plugin.route('/series/<url>/<offset>')
def getSeries(url, offset):
	print "getSeries(url, offset):"
	print "    url    = " + url
	print "    offset = " + offset
	if str(offset) == 0:
		html = get_page(url)
	else:
		html = get_page(url)
		#showErrorMessage("Getting series by offset unsupported")

	soup = BeautifulSoup(html)
	anchors = soup('div', {'class' : 'media_list_item no-popup'})
	items = []
	for anchor in anchors:
		matches = re.findall('<a href="(.+?)".+?class="thumb">.+?<img data-original="(.+?)".+?class="heading">(.+?)</a>', str(anchor), re.DOTALL)
		items.append({	
			'label': matches[0][2],
			'thumbnail': matches[0][1],
			'path': plugin.url_for("playVideo", url = BASEURL + matches[0][0], offset = 0),
		})
	
	matches = re.findall('<iframe src="(.+?)".+?scrolling="no" frameborder="no".+?</iframe>', html)
	if matches != []:
		items.append({
			'label': "Video",
			'path': plugin.url_for("playVideo", url = url),
		})
	
	items.append({
		'label': "Next",
		'path': plugin.url_for("getSubcategories", url = url, offset = int(offset) + 16),
	})
	return plugin.finish(items)
	
@plugin.route('/play/<url>')
def playVideo(url):
	print "playVideo(url):"
	print "    url    = " + url
	html = get_page(url)
	matches = re.findall('<iframe src="(.+?)".+?scrolling="no" frameborder="no".+?</iframe>', html)
	html =get_page(matches[0])
	matches = re.findall('<iframe src="(.+?)".+?</iframe>', html)
	html =get_page(matches[0])
	matches = re.findall('"uid":"player","file":"(.+?)"', html)
	videoUrl = urllib.unquote(matches[0]).decode('utf8')
	xbmc.Player().play(videoUrl)
	
	
def showErrorMessage(msg):
	print msg
	xbmc.executebuiltin("XBMC.Notification(%s,%s, %s)"%("ERROR",msg, str(10*1000)))
		
#	matcher = re.compile('<div class="pic"><a href="(.+?)"><img src="(.+?)" alt="(.+?)" height=".+?" width=".+?" /></a></div> ')
#	matches = matcher.findall(html)
#	items = [{
#		'label': name,
#		'thumbnail': thumburl,
#		'path': plugin.url_for('', url=album_url),
#	} for album_url, thumburl, name in matches]
	
# ==========================================================================================
# MAIN
# ==========================================================================================
if __name__ == '__main__':
    plugin.run()