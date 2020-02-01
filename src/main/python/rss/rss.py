# TODO: 
# - OPML import
# - need to figure out how to do refresh
# - should have bool in config: use user-defined names or the ones provided by the RSS feed?

import requests
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
	try:
		response = requests.get(feed, headers={
			'user-agent': 'vaalbara-lite' # some feeds will 403 if a user-agent isn't defined
			})
		response.raise_for_status()
		rss_xml = response.text
		el = ET.fromstring(rss_xml)
		feed_title = el.find('./channel/title').text
		menu = Menu(feed_name)
		for item in el.findall('./channel/item'):
			add_item(item, menu)
	except (requests.exceptions.RequestException, requests.HTTPError, ET.ParseError) as err:
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
