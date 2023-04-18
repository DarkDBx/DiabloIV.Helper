from PyQt5.QtWidgets import QApplication, QTabWidget

from easyedit.TextArea import TextArea


class TabBar(QTabWidget):
    def __init__(self):
        super().__init__()

        self.setMovable(True)
        self.setTabsClosable(True)

        self.tabCloseRequested.connect(self.closeTab)

    def openTab(self):
        textWidget = TextArea()

        if self.count() == 0:
            self.addTab(textWidget, "Untitled")
        else:
            self.addTab(textWidget, "Untitled ({})".format(self.count() + 1))

        self.setCurrentIndex(self.count() - 1)

    def closeTab(self, index):
        self.removeTab(index)

        if self.count() == 0:
            QApplication.quit()
