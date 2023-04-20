from os.path import split
import logging
from PyQt5.QtCore import QSettings, QPoint, QSize, pyqtSlot
from PyQt5.QtWidgets import QFileDialog, QFontDialog, QMainWindow

from easyedit.AboutDialog import AboutDialog
from easyedit.MenuBar import MenuBar
from easyedit.TabBar import TabBar


class Editor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.fileToLanguage = {
            '': None,
            'txt': None,
            'sh': 'Bash',
            'bat': 'Batch',
            'coffee': 'CoffeeScript',
            'c': 'C++',
            'cpp': 'C++',
            'cxx': 'C++',
            'h': 'C++',
            'hpp': 'C++',
            'hxx': 'C++',
            'cs': 'C#',
            'css': 'CSS',
            'd': 'D',
            'f': 'Fortran',
            'html': 'HTML',
            'java': 'Java',
            'js': 'JavaScript',
            'json': 'JSON',
            'lua': 'Lua',
            'md': 'Markdown',
            'mlx': 'Matlab',
            'pas': 'Pascal',
            'pl': 'Perl',
            'py': 'Python',
            'rb': 'Ruby',
            'sql': 'SQL',
            'yaml': 'YAML',
            'xml': 'XML'
        }

        self.readWindowSettings()

        self.aboutDialog = AboutDialog()

        self.menuBar = MenuBar()
        self.setMenuBar(self.menuBar)

        self.tabBar = TabBar()
        self.readTabBarSettings()
        self.setCentralWidget(self.tabBar)

        self.changeFont(self.font())

        self.statusBar = self.statusBar()
        # self.updateStatusBarText()

        self.configureSignals()

        self.show()

    def readWindowSettings(self):
        settings = QSettings("msklosak", "EasyEdit")

        settings.beginGroup("Editor")
        self.resize(settings.value("size", QSize(600, 800)))
        self.move(settings.value("pos", QPoint(0, 0)))
        self.setFont(settings.value("font", self.font()))
        settings.endGroup()

    def writeWindowSettings(self):
        settings = QSettings("msklosak", "EasyEdit")

        settings.beginGroup("Editor")
        settings.setValue("size", self.size())
        settings.setValue("pos", self.pos())
        settings.setValue("font", self.font())
        settings.endGroup()

    def readTabBarSettings(self):
        settings = QSettings("msklosak", "EasyEdit")
        settings.beginGroup("Tab Bar")

        savedTabs = settings.value("openedTabs")
        tabLexers = settings.value("tabLexers")
        if savedTabs is None or savedTabs[0] == "Untitled":
            self.tabBar.openTab()
        else:
            for i in range(len(savedTabs)):
                if savedTabs[i] != "Untitled":
                    self.tabBar.openTab()
                    self.openFile(savedTabs[i])
                    self.tabBar.widget(i).changeLexer(tabLexers[i])

        self.tabBar.setCurrentIndex(int(settings.value("currentTab", 0)))

        self.updateWindowTitle()

        settings.endGroup()

    def writeTabBarSettings(self):
        openTabs = []
        tabLexers = []

        for i in range(self.tabBar.count()):
            openTabs.append(self.tabBar.widget(i).filePath)
            tabLexers.append(self.tabBar.widget(i).currentLanguage)

        settings = QSettings("msklosak", "EasyEdit")
        settings.beginGroup("Tab Bar")
        settings.setValue("openedTabs", openTabs)
        settings.setValue("tabLexers", tabLexers)
        settings.setValue("currentTab", self.tabBar.currentIndex())
        settings.endGroup()

    def closeEvent(self, event):
        self.writeTabBarSettings()
        self.writeWindowSettings()

        while self.tabBar.count() > 0:
            self.tabBar.closeTab(0)

    def configureSignals(self):
        # FILE TAB
        self.menuBar.newFile.connect(self.tabBar.openTab)
        self.menuBar.openFile.connect(self.openFileDialog)
        self.menuBar.saveFile.connect(self.saveFile)
        self.menuBar.saveFileAs.connect(self.saveFileAs)

        # EDIT TAB
        self.menuBar.undoEdit.connect(self.tabBar.currentWidget().undo)
        self.menuBar.redoEdit.connect(self.tabBar.currentWidget().redo)
        self.menuBar.cutText.connect(self.tabBar.currentWidget().cut)
        self.menuBar.copyText.connect(self.tabBar.currentWidget().copy)
        self.menuBar.pasteText.connect(self.tabBar.currentWidget().paste)

        # SETTINGS TAB
        self.menuBar.changeFont.connect(self.changeFontDialog)

        # HELP TAB
        self.menuBar.openAboutDialog.connect(lambda: self.aboutDialog.exec_())

        # TAB BAR
        self.tabBar.currentChanged.connect(self.tabChanged)

        # TEXT AREA
        self.menuBar.changeLanguage.connect(self.changeLanguage)
        # self.tabBar.currentWidget().cursorPositionChanged.connect(self.updateStatusBarText)

    def changeLanguage(self, language):
        self.tabBar.currentWidget().changeLexer(language)
        self.changeFont(self.font())

    def changeFont(self, newFont):
        self.setFont(newFont)

        for i in range(self.tabBar.count()):
            self.tabBar.widget(i).updateFont(newFont)

    def changeFontDialog(self):
        font = QFontDialog().getFont()[0]

        self.changeFont(font)

    def openFile(self, fileName):
        with open(fileName, 'r') as file:
            self.tabBar.currentWidget().setText(file.read())

        shortenedFileName = split(fileName)[1]
        extension = shortenedFileName.split('.')

        # Get the programming language of the file based on the
        # extension and set the syntax highlight to that language.
        # If no extension, load default lexer.
        if len(extension) == 2:
            language = self.fileToLanguage.get(extension[1])

            self.changeLanguage(language)
        else:
            self.changeLanguage(None)

        self.tabBar.currentWidget().filePath = fileName
        self.tabBar.setTabText(self.tabBar.currentIndex(), shortenedFileName)
        self.tabBar.currentWidget().changeMarginWidth()
        self.updateWindowTitle()

    def openFileDialog(self):
        fileName = QFileDialog.getOpenFileName(self, "Open File")[0]

        if fileName != "":
            self.openFile(fileName)

    def saveFile(self):
        if self.tabBar.currentWidget().filePath != "Untitled":
            fileName = self.tabBar.currentWidget().filePath

            if fileName != "":
                text = self.tabBar.currentWidget().text()

                with open(fileName, 'w') as file:
                    file.write(text)
                logging.info('File saved as: '+fileName)

            self.changeFont(self.font())
        else:
            self.saveFileAs()

    def saveFileAs(self):
        fileName = QFileDialog.getSaveFileName(self, "Save File", None, self.tabBar.currentWidget().getFileType())[0]

        if fileName != "":
            shortenedFileName = split(fileName)[1]

            self.tabBar.setTabText(self.tabBar.currentIndex(), shortenedFileName)
            self.updateWindowTitle()

            text = self.tabBar.currentWidget().text()

            with open(fileName, 'w') as file:
                file.write(text)

        self.changeFont(self.font())

    def tabChanged(self):
        if self.tabBar.count() > 1:
            # self.tabBar.currentWidget().cursorPositionChanged.connect(self.updateStatusBarText)

            self.updateWindowTitle()

    def updateWindowTitle(self):
        self.setWindowTitle(self.tabBar.tabText(self.tabBar.currentIndex()) + " - EasyEdit")

    @pyqtSlot(int, int)
    def updateStatusBarText(self, line, column):
        self.statusBar.showMessage("Line {}, Column {}".format(line, column))
