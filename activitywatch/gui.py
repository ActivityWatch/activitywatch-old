"""
A simple GUI test consisting only of a tray icon

Features:
 - Status indication
 - Open Web UI
 - Quit
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


def sigint_handler(*args):
    """Handles the SIGINT signal (Ctrl+C)"""
    QApplication.quit()

def main():
    signal.signal(signal.SIGINT, sigint_handler)

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

main()
