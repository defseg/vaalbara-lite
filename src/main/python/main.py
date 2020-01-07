from config import config, set_default, load_text
import importlib, os, sys
from menus.indicator import Indicator
from menus.dispatcher import Dispatcher
from menus.xml_to_obj import parse
import xml.etree.ElementTree as ET
from fbs_runtime.application_context.PySide2 import ApplicationContext
import widgets.rss

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
  return [widgets.rss]

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
    'refresh'   : lambda w: indicator.update_widget(parse(build_by_name(widgets, w.data['name'])))
  }

  Dispatcher(defaults)

def build_menu_items(widgets):
  '''Call every loaded widget and concat them together into an XML description
  of the full menu to build. Widgets may return either an ElementTree element 
  or a string containing valid XML.
     Each widget has a `main` function, which receives one argument: the value
  in the `config` dict corresponding to the widget's name. For example, a 
  widget `foo` would receive `config['foo']` as an argument to its `main`.
  TODO: DTD'''
  menu_xml = ET.Element('menu-base')
  for w in widgets:
    menu_xml.append(build_menu_item(w))
  return parse(menu_xml)

def build_menu_item(widget):
  '''Call one loaded widget to get its menu, and return an ElementTree element
  containing the widget's menu.'''
  _print_loading_msg('Building menu for module {}'.format(_name(widget)))
  res = widget.main(config.get(_name(widget)))
  if res.__class__.__name__ == 'Element':
    pass
  elif w.__class__.__name__ == 'str':
    res = ET.fromstring(res)
  else:
    raise AppletError('Menu was given something besides an element or a str: {}'.format(w.__class__.__name__))
  # Append refresh option.
  refresh = ET.SubElement(res, 'item', {'action': 'refresh', 'name': _name(widget)})
  refresh.text = 'Refresh'
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
