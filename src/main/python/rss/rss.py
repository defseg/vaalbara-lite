# TODO: 
# - OPML import
# - need to figure out how to do refresh
# - should have bool in config: use user-defined names or the ones provided by the RSS feed?

from urllib.request import urlopen
import urllib.error
import xml.etree.ElementTree as ET
from menus.menu import Menu, MenuItem

def main(config) -> Menu:
	return fetch_all(config['feeds'])

def fetch_all(feeds, menu = None):
	if menu is None:
		menu = Menu('RSS')
	for name in feeds:
		if feeds[name].__class__.__name__ == 'dict':
			# it's a folder
			submenu = Menu(name)
			fetch_all(feeds[name], submenu)
			menu.append(submenu)
		else:
			# if it's not a folder, assume it's a feed
			menu.append(read_feed(feeds[name], name))
	return menu

def read_feed(feed, feed_name):
	'''Open a feed's URL and read the RSS.'''
	try:
		html = urlopen(feed).read()
		el = ET.fromstring(html)
		feed_title = el.find('./channel/title').text
		menu = Menu(feed_name)
		for item in el.findall('./channel/item'):
			add_item(item, menu)
	except urllib.error.HTTPError as err:
		menu = Menu(f'* {feed_name}') 
		add_error_notification(str(err), menu)
	return menu

def add_item(item, menu):
	'''Parse an ElementTree `item` element into a MenuItem and append it to `menu`.'''
	item = MenuItem(
		text = item.find('title').text
	,	action = 'navigate'
	,	data = {'url': item.find('link').text}
	)
	menu.append(item)
	return menu

def add_error_notification(error_text, menu):
	item = MenuItem(
		text = error_text
	,	action = ''
	,	data = {}
	)
	menu.append(item)
	return menu
