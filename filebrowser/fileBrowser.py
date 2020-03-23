from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore
import os, sys, subprocess

from ui import main


class MyFileBrowser(main.Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self, maya=False):
        super(MyFileBrowser, self).__init__()
        self.setupUi(self)
        self.maya = maya
        self.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.context_menu)
        self.populate()

    def populate(self):
        # TODO: Set to user's selected Archive folder
        # also make filepaths safe for both Windows and Mac via OS
        # CHANGE FILE PATH BEFORE RUNNING
        path = "/Users/matthewolson"
        self.model = QtWidgets.QFileSystemModel()
        self.model.setRootPath((QtCore.QDir.rootPath()))
        self.treeView.setModel(self.model)
        self.treeView.setRootIndex(self.model.index(path))
        self.treeView.setSortingEnabled(True)

    def context_menu(self):
        menu = QtWidgets.QMenu()
        open = menu.addAction("Open")
        open.triggered.connect(self.open_file)
        cursor = QtGui.QCursor()
        menu.exec_(cursor.pos())

    def open_file(self):
        # TODO: Link with webpage displayer/editor
        index = self.treeView.currentIndex()
        file_path = self.model.filePath(index)
        # cannot use startfile on Mac, Windows only
        if sys.platform == "win32":
            os.startfile(file_path)
        else:
            opener ="open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, file_path])

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    fb = MyFileBrowser()
    fb.show()
    app.exec_()