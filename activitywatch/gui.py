"""
A simple GUI test consisting only of a tray icon

ToDo:
 - Choose between PyQt or wxPython.

Features:
 - Open Web UI
 - Status indication via disabled text and tray icon (Dropbox style)
 - Quit

Requirements:
 - ActivityWatch should be completely functional without this module and its dependencies (PyQt or wxPython).
   - It might be wise to start considering dividing up the code into core- and gui-modules soon.
"""

import sys
import threading
import signal
import webbrowser

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


def main():
    threading.Thread(target=run, daemon=True).start()


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


if __name__ == "__main__":
    main()
