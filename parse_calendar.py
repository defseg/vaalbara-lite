from gi.repository import Gtk
from bs4 import BeautifulSoup, SoupStrainer
from urllib2 import urlopen
from collections import namedtuple
from webbrowser import open as open_in_browser
import datetime

last_parsed_at = datetime.datetime.min
events = False

def build_calendar_items():
  if datetime.datetime.now().date() > last_parsed_at.date():
    set_events(fetch())
  return [menuize(event) for event in events]

def set_events(soup):
  global last_parsed_at, events
  last_parsed_at = datetime.datetime.now()
  events = parse(soup)

def menuize(event):
  menu_item = Gtk.MenuItem(event.title)
  menu_item.connect("activate", navigate)
  menu_item.event_obj = event
  return menu_item

def navigate(e):
  if e.event_obj and e.event_obj.calendar_url:
    open_in_browser(e.event_obj.calendar_url)

def fetch():
  html = urlopen("http://www.thebostoncalendar.com/").read()
  strainer = SoupStrainer("li", class_="event")
  return BeautifulSoup(html, parse_only=strainer)

def parse(soup):
  return [parse_one(li) for li in soup.find_all("li")]

def parse_one(li):
  title_el        = li.select_one("div.info > h3 > a")
  time_str_el     = li.select_one("p.time")
  location_el     = li.select_one("p.location")
  calendar_url_el = li.select_one("a[itemprop=url]")
  title        = title_el.contents                      if title_el        is not None else "No title given"
  time_str     = time_str_el.contents[0].strip() + u"m" if time_str_el     is not None else "No time given"
  location     = location_el.contents[0].strip()        if location_el     is not None else "No location given"
  calendar_url = calendar_url_el.get("href")            if calendar_url_el is not None else "No calendar URL given"
  return CalendarEntry(title=title, time=time_str, location=location, calendar_url=calendar_url)

CalendarEntry = namedtuple("CalendarEntry", ["title", "time", "location", "calendar_url"])