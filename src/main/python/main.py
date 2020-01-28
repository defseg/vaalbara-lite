from config import config, set_default, load_text
import importlib, os, sys
from menus.indicator import Indicator
from menus.dispatcher import Dispatcher
import xml.etree.ElementTree as ET
from fbs_runtime.application_context.PySide2 import ApplicationContext
import rss

from menus.menu import BaseMenu, MenuItem

def main():
  ctx = ApplicationContext()
  widgets = get_widgets(config)
  _print_loading_msg('All widgets loaded!')
  indicator = Indicator(ctx)
  build_dispatcher(widgets, indicator)
  indicator.set_menu(build_menu_items(widgets))
  _print_loading_msg('All menus built!')
  indicator.go()

def get_widgets(config):
  return [rss]

def build_widget_configs(widgets, config):
  for widget in widgets:
    if _name(widget) not in config:
      if hasattr(widget, 'default'):
        set_default(_name(widget), widget.default)
        config[_name(widget)] = load_text(widget.default)[_name(widget)] # TODO maybe make this better
      else:
        set_default(_name(widget), '# No defaults given')

def build_dispatcher(widgets, indicator):
  defaults = {
    'refreshall': lambda: indicator.set_menu(build_menu_items(widgets)),
    'refresh'   : lambda w: indicator.update_widget(build_by_name(widgets, w.data['name']))
  }

  Dispatcher(defaults)

def build_menu_items(widgets) -> BaseMenu:
  '''This builds the BaseMenu.
     Each widget has a `main` function, which receives one argument: the value
  in the `config` dict corresponding to the widget's name. For example, a 
  widget `foo` would receive `config['foo']` as an argument to its `main`.'''
  # TODO
  items = []
  for widget in widgets:
    items.append(build_menu_item(widget))
  return BaseMenu(items)

def build_menu_item(widget):
  '''Call one loaded widget to get its menu, and return a Menu.'''
  res = widget.main(config.get(_name(widget)))
  res.append(MenuItem('Refresh', 'refresh', {'name': _name(widget)}))
  return res

def build_by_name(widgets, w_name):
  # TODO: probably want to make this not O(n) at some point
  for w in widgets:
    if _name(w) == w_name:
      return build_menu_item(w)

def _name(widget):
  '''Get only the name of the widget, not the module path.'''
  return widget.__name__.split('.')[-1]

def _print_loading_msg(text):
  '''Print some loading messages if display_loading_msgs is set to true in the 
  config.'''
  if config.get('vaalbara') and config.get('vaalbara').get('display_loading_msgs'):
    print(text)

if __name__ == '__main__':
  main()

class AppletError(Exception):
  pass
