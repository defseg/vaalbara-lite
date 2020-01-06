from PySide2 import QtGui
from PySide2.QtWidgets import QSystemTrayIcon, QMenu, QApplication, QStyle
from .dispatcher import Dispatcher
from .xml_to_obj import MenuItem
import sys, signal

class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        self.menu = BaseMenu()
        self.setContextMenu(self.menu)
        # Set up Ctrl+C handling. 
        # Could be done differently - see https://coldfix.eu/2016/11/08/pyqt-boilerplate/#keyboardinterrupt-ctrl-c
        # But this way is simpler and a little faster.
        signal.signal(signal.SIGINT, signal.SIG_DFL)

    def add_needed_items(self):
        refresh_option = self.menu.addAction('Refresh all')
        refresh_option.triggered.connect(Dispatcher.get('refreshall'))
        quit_option = self.menu.addAction('Quit')
        quit_option.triggered.connect(QtGui.qApp.quit)

    def clear_menu(self):
        self.menu.clear()

class BaseMenu(QMenu):
    def __init__(self):
        QMenu.__init__(self, "")
        self.widgets = {}

    def add_widget(self, menu):
        assert menu.__class__.__name__ == "Menu"
        self.widgets[menu.text] = QtMenu(menu, parent=self)
        self.addMenu(self.widgets[menu.text])

    def refresh_widget(self, menu):
        assert menu.__class__.__name__ == "Menu"
        self.widgets[menu.text].refresh(menu)

class QtMenu(QMenu):
    def __init__(self, menu, parent=None):
        QMenu.__init__(self, menu.text, parent)
        self.__add_all(menu)

    def refresh(self, menu):
        self.clear()
        self.__add_all(menu)

    def __add_all(self, menu):
        for i in menu.items:
            self.__add(i)

    def __add(self, thing):
        if thing.__class__.__name__ == "Menu":
            self.addMenu(QtMenu(thing, parent=self))
        elif thing.__class__.__name__ == "MenuItem":
            menu_item = self.addAction(thing.text)
            if thing.action:
                menu_item.triggered.connect(Dispatcher.get(thing))
        else:
            raise IndicatorError("{} isn't menu or item".format(thing))

class Indicator():
    def __init__(self):
        self.app       = QApplication(sys.argv)
        icon_graphic   = QApplication.style().standardIcon(QStyle.SP_DriveDVDIcon)
        self.icon      = SystemTrayIcon(icon_graphic)
        self.icon_menu = self.icon.menu # let's just put this here 

    def set_menu(self, menu_base):
        self.icon.clear_menu()
        for w in menu_base.items:
            self.icon_menu.add_widget(w)
        self.icon.add_needed_items()

    def update_widget(self, menu):
        self.icon_menu.refresh_widget(menu)

    def go(self):
        self.icon.show()
        sys.exit(self.app.exec_())

class IndicatorError(Exception):
    pass