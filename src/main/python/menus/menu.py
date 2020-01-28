# A `BaseMenu` has:
#   - an items array of menus and items
#   - nothing else
# A `menu` has:
#   - an items array of menus and items
#   - text - the title of the menu
# A `MenuItem` has:
#   - a data dictionary, which may contain:
#     - an `action` key to determine what to do when the user clicks the item
#     - Existing actions are:
#       - navigate: open the value of `data['url']` in a web browser
#       - quit: quit
#     Presumably this will be expanded later.
#   - text - the title of the item

class Menu:
  def __init__(self, text: str, items = None):
    self.text = text
    if items is None:
      self.items = []
    else:
      self.items = items
  def __repr__(self) -> str:
    return 'Menu: {}; items: {}'.format(self.text, self._items_to_string())
  def _items_to_string(self) -> str:
    return '\n'.join(['- {}'.format(repr(item)) for item in self.items])
  def append(self, item):
    self.items.append(item)
  def add(self, new_items):
    self.items += new_items

class BaseMenu(Menu):
  def __init__(self, items = None):
    super().__init__('', items = items)
  def __repr__(self) -> str:
    return 'BaseMenu; items: {}'.format(len(self.items))

class MenuItem:
  def __init__(self, text, action, data = {}):
    self.text = text
    self.action = action
    self.data = data
  def __repr__(self) -> str:
    return 'MenuItem: {} - Data: {}'.format(self.text, self.data)