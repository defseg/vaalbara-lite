from config import config, set_default, load_text
import importlib, os, sys
from menus.indicator import Indicator
from menus.dispatcher import Dispatcher
import xml.etree.ElementTree as ET
from fbs_runtime.application_context.PySide2 import ApplicationContext
import rss

from menus.menu import BaseMenu, Menu, MenuItem

def main():
  ctx = ApplicationContext()
  build_config(config)
  indicator = Indicator(ctx)
  build_dispatcher(indicator)

  indicator.set_menu(build_menu())
  _print_loading_msg('All menus built!')
  indicator.go()

def build_config(config):
  if 'rss' not in config:
    set_default('rss', rss.default)
    config['rss'] = load_text(rss.default)['rss']

def build_dispatcher(indicator):
  defaults = {
    'refresh': lambda w: indicator.set_menu(build_menu())
  }

  Dispatcher(defaults)

def build_menu():
  menu = Menu('RSS')
  menu.add(rss.main(config.get('rss')).items)
  menu.append(MenuItem('Refresh', 'refresh'))
  # TODO remove the need for this
  return menu

def _print_loading_msg(text):
  '''Print some loading messages if display_loading_msgs is set to true in the 
  config.'''
  if config.get('vaalbara') and config.get('vaalbara').get('display_loading_msgs'):
    print(text)

if __name__ == '__main__':
  main()

class AppletError(Exception):
  pass
