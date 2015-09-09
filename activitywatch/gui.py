"""
A GUI test consisting only of a tray icon

Features:
 - Open Web UI
 - Status indication via disabled text and tray icon (Dropbox style)
 - Quit

Requirements:
 - ActivityWatch should be completely functional without this module and its dependencies (GTK3).
"""

import sys
import threading
import signal
import webbrowser

from gi.repository import Gtk


def show_about_dialog(self):
    about_dialog = Gtk.AboutDialog()

    #about_dialog.set_destroy_with_parent(True)
    about_dialog.set_name("ActivityWatch")
    about_dialog.set_version("0.1") # TODO: Get and set proper version
    about_dialog.set_authors(["Erik Bjäreholt"])

    about_dialog.run()
    about_dialog.destroy()

toggleState = False

def toggle_something(check):
    global toggleState
    toggleState = not toggleState
    check.set_active(toggleState)

def open_popup_menu(icon, button, time):
    print("Opening popup menu")
    menu = Gtk.Menu()

    about = Gtk.MenuItem(label="About")

    statusLine1 = Gtk.MenuItem(label="Status: Running")
    statusLine2 = Gtk.MenuItem(label="  some status")
    statusLine3 = Gtk.MenuItem(label="  more status...")

    quit = Gtk.MenuItem(label="Quit")

    check = Gtk.CheckMenuItem(label="Checktest")
    check.set_active(toggleState)

    statusLine1.set_sensitive(toggleState)
    statusLine2.set_sensitive(toggleState)
    statusLine3.set_sensitive(toggleState)

    about.connect("activate", show_about_dialog)
    check.connect("toggled", toggle_something)
    quit.connect("activate", Gtk.main_quit)

    menu.append(about)
    menu.append(check)
    menu.append(Gtk.SeparatorMenuItem())
    menu.append(statusLine1)
    menu.append(statusLine2)
    menu.append(statusLine3)
    menu.append(Gtk.SeparatorMenuItem())
    menu.append(quit)

    menu.show_all()

    def pos(menu, icon):
        return (Gtk.StatusIcon.position_menu(menu, icon))

    menu.popup(None, None, pos, None, button, time)

def open_dashboard(event):
    print("Opening dashboard")
    webbrowser.open("http://localhost:5000/")

statusicon = Gtk.StatusIcon()
statusicon.set_from_stock(Gtk.STOCK_MEDIA_RECORD)
statusicon.set_title("StatusIcon")
statusicon.connect("popup-menu", open_popup_menu) # Right click
statusicon.connect("activate", open_dashboard) # Left click

def run():
    Gtk.main()

"""
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QSystemTrayIcon, QApplication, QMenu, QWidget, QIcon


class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        menu = QMenu(parent)
        self.setToolTip("This is a tooltip\nThis is a second line")

        openWebUIIcon = QIcon.fromTheme("open", QIcon("none"))
        openWebUIAction = menu.addAction(openWebUIIcon, "Open Dashboard", self.open_webui)

        menu.addSeparator()

        infoText = menu.addAction("Here we can display info")
        infoText.setEnabled(False)

        menu.addSeparator()

        exitIcon = QIcon.fromTheme("application-exit", QIcon("media/application_exit.png"))
        exitAction = menu.addAction(exitIcon, "Quit ActivityWatch", self.exit)

        self.setContextMenu(menu)

    def open_webui(self):
        # TODO: Fetch proper URL from flask
        print("Opening Web UI")
        webbrowser.open("localhost")

    def exit(self):
        # TODO: Do cleanup actions
        # TODO: Save state for resume
        options = QtGui.QMessageBox.Yes | QtGui.QMessageBox.No
        default = QtGui.QMessageBox.No
        answer = QtGui.QMessageBox.question(None, '', "Are you sure you want to quit?", options, default)
        if answer == QtGui.QMessageBox.Yes:
            QApplication.quit()
            from .rest import stop_server
            stop_server()



def run():
    app = QApplication(sys.argv)
    timer = QtCore.QTimer()
    timer.start(500)  # You may change this if you wish.
    timer.timeout.connect(lambda: None)  # Let the interpreter run each 500 ms.

    w = QWidget()
    trayIcon = SystemTrayIcon(QIcon("media/logo.png"), w)

    print("Showing tray icon")
    trayIcon.show()

    # Run the application
    exit_message = app.exec_()

    # Exit
    sys.exit(exit_message)
"""

def main():
    threading.Thread(target=run, daemon=False).start()


if __name__ == "__main__":
    main()
