from PySide2 import QtGui
from PySide2.QtWidgets import QSystemTrayIcon, QMenu, QApplication, QStyle
from PySide2.QtGui import QIcon
from .dispatcher import Dispatcher
from .menu import MenuItem
import sys, signal

class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        self.menu = MenuBase()
        self.setContextMenu(self.menu)
        # Set up Ctrl+C handling. 
        # Could be done differently - see https://coldfix.eu/2016/11/08/pyqt-boilerplate/#keyboardinterrupt-ctrl-c
        # But this way is simpler and a little faster.
        signal.signal(signal.SIGINT, signal.SIG_DFL)

    def add_needed_items(self):
        quit_option = self.menu.addAction('Quit')
        quit_option.triggered.connect(QtGui.qApp.quit)

    def clear_menu(self): 
        self.menu.clear()

class QtMenu(QMenu):
    def __init__(self, menu, parent=None):
        QMenu.__init__(self, menu.text, parent)
        self.__add_all(menu)

    def refresh(self, menu):
        self.clear()
        self.__add_all(menu)

    def __add_all(self, menu):
        for i in menu.items:
            self.add(i)

    def add(self, thing):
        if thing.__class__.__name__ == "Menu" or thing.__class__.__name__ == "BaseMenu":
            self.addMenu(QtMenu(thing, parent=self))
        elif thing.__class__.__name__ == "MenuItem":
            menu_item = self.addAction(thing.text)
            if thing.action:
                menu_item.triggered.connect(Dispatcher.get(thing))
        else:
            raise IndicatorError("{} isn't menu or item".format(thing))

class MenuBase(QtMenu):
    def __init__(self):
        QMenu.__init__(self, "")

class Indicator():
    def __init__(self, ctx):
        self.app       = ctx.app
        icon_graphic   = QIcon(ctx.icon)
        self.icon      = SystemTrayIcon(icon_graphic)
        self.icon_menu = self.icon.menu # let's just put this here 

    def set_menu(self, menu_base):
        self.icon.clear_menu()
        for w in menu_base.items:
            self.icon_menu.add(w)
        self.icon.add_needed_items()

    def update_widget(self, menu):
        self.icon_menu.refresh(menu)

    def go(self):
        self.icon.show()
        sys.exit(self.app.exec_())

class IndicatorError(Exception):
    pass