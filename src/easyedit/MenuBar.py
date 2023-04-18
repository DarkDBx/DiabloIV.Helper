from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QApplication, QMenuBar


class MenuBar(QMenuBar):
    newFile = pyqtSignal()
    openFile = pyqtSignal()
    saveFile = pyqtSignal()
    saveFileAs = pyqtSignal()

    undoEdit = pyqtSignal()
    redoEdit = pyqtSignal()
    cutText = pyqtSignal()
    copyText = pyqtSignal()
    pasteText = pyqtSignal()

    changeFont = pyqtSignal()

    changeLanguage = pyqtSignal(str)

    openAboutDialog = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.fileMenu = None
        self.editMenu = None
        self.settingsMenu = None
        self.helpMenu = None

        self.changeFileMenu()
        self.createEditMenu()
        self.createSettingsMenu()
        self.createHelpMenu()

    def changeFileMenu(self):
        newFileAction = QAction(QIcon("new.png"), 'New File', self)
        newFileAction.setShortcut("Ctrl+N")
        newFileAction.setStatusTip("New file")
        newFileAction.triggered.connect(lambda: self.newFile.emit())

        openFileAction = QAction(QIcon("open.png"), 'Open File', self)
        openFileAction.setShortcut("Ctrl+O")
        openFileAction.setStatusTip("Open file")
        openFileAction.triggered.connect(lambda: self.openFile.emit())

        saveFileAction = QAction(QIcon("save.png"), 'Save File', self)
        saveFileAction.setShortcut("Ctrl+S")
        saveFileAction.setStatusTip("Save file")
        saveFileAction.triggered.connect(lambda: self.saveFile.emit())

        saveFileAsAction = QAction(QIcon("save.png"), 'Save File As', self)
        saveFileAsAction.setShortcut("Ctrl+Shift+S")
        saveFileAsAction.setStatusTip("Save file as")
        saveFileAsAction.triggered.connect(lambda: self.saveFileAs.emit())

        quitAction = QAction(QIcon("quit.png"), 'Quit', self)
        quitAction.setShortcut("Ctrl+Q")
        quitAction.setStatusTip("Quit EasyEdit")
        quitAction.triggered.connect(lambda: QApplication.quit())

        self.fileMenu = self.addMenu("File")
        self.fileMenu.addAction(newFileAction)
        self.fileMenu.addAction(openFileAction)
        self.fileMenu.addAction(saveFileAction)
        self.fileMenu.addAction(saveFileAsAction)
        self.fileMenu.addAction(quitAction)

    def createEditMenu(self):
        undoEditAction = QAction(QIcon("icons/undo.png"), "Undo", self)
        undoEditAction.setStatusTip("Undo last edit")
        undoEditAction.setShortcut("Ctrl+Z")
        undoEditAction.triggered.connect(lambda: self.undoEdit.emit())

        redoEditAction = QAction(QIcon("icons/redo.png"), "Redo", self)
        redoEditAction.setStatusTip("Redo last edit")
        redoEditAction.setShortcut("Ctrl+Shift+Z")
        redoEditAction.triggered.connect(lambda: self.redoEdit.emit())

        cutTextAction = QAction(QIcon("icons/cut.png"), "Cut Selection", self)
        cutTextAction.setStatusTip("Cut text to clipboard")
        cutTextAction.setShortcut("Ctrl+X")
        cutTextAction.triggered.connect(lambda: self.cutText.emit())

        copyTextAction = QAction(QIcon("icons/copy.png"), "Copy Selection", self)
        copyTextAction.setStatusTip("Copy text to clipboard")
        copyTextAction.setShortcut("Ctrl+C")
        copyTextAction.triggered.connect(lambda: self.copyText.emit())

        pasteTextAction = QAction(QIcon("icons/paste.png"), "Paste", self)
        pasteTextAction.setStatusTip("Paste text from clipboard")
        pasteTextAction.setShortcut("Ctrl+V")
        pasteTextAction.triggered.connect(lambda: self.pasteText.emit())

        self.editMenu = self.addMenu("Edit")
        self.editMenu.addAction(undoEditAction)
        self.editMenu.addAction(redoEditAction)
        self.editMenu.addAction(cutTextAction)
        self.editMenu.addAction(copyTextAction)
        self.editMenu.addAction(pasteTextAction)

    def createSettingsMenu(self):
        changeFontAction = QAction(QIcon("icons/font.png"), "Change Font", self)
        changeFontAction.setStatusTip("Change font")
        changeFontAction.triggered.connect(lambda: self.changeFont.emit())

        self.settingsMenu = self.addMenu("Settings")

        self.settingsMenu.addAction(changeFontAction)

        languageMenu = self.settingsMenu.addMenu("Language")

        bashLanguageAction = QAction("Bash", self)
        bashLanguageAction.setStatusTip("Set language to Bash")
        bashLanguageAction.triggered.connect(lambda: self.changeLanguage.emit("Bash"))
        languageMenu.addAction(bashLanguageAction)

        batchLanguageAction = QAction("Batch", self)
        batchLanguageAction.setStatusTip("Set language to Batch")
        batchLanguageAction.triggered.connect(lambda: self.changeLanguage.emit("Batch"))
        languageMenu.addAction(batchLanguageAction)

        cmakeLanguageAction = QAction("CMake", self)
        cmakeLanguageAction.setStatusTip("Set language to CMake")
        cmakeLanguageAction.triggered.connect(lambda: self.changeLanguage.emit("CMake"))
        languageMenu.addAction(cmakeLanguageAction)

        coffeeScriptLanguageAction = QAction("CoffeeScript", self)
        coffeeScriptLanguageAction.setStatusTip("Set language to CoffeeScript")
        coffeeScriptLanguageAction.triggered.connect(lambda: self.changeLanguage.emit("CoffeeScript"))
        languageMenu.addAction(coffeeScriptLanguageAction)

        cppLanguageAction = QAction("C++", self)
        cppLanguageAction.setStatusTip("Set language to C++")
        cppLanguageAction.triggered.connect(lambda: self.changeLanguage.emit("C++"))
        languageMenu.addAction(cppLanguageAction)

        csharpLanguageAction = QAction("C#", self)
        csharpLanguageAction.setStatusTip("Set language to C#")
        csharpLanguageAction.triggered.connect(lambda: self.changeLanguage.emit("C#"))
        languageMenu.addAction(csharpLanguageAction)

        cssLanguageAction = QAction("CSS", self)
        cssLanguageAction.setStatusTip("Set language to CSS")
        cssLanguageAction.triggered.connect(lambda: self.changeLanguage.emit("CSS"))
        languageMenu.addAction(cssLanguageAction)

        dLanguageAction = QAction("D", self)
        dLanguageAction.setStatusTip("Set language to D")
        dLanguageAction.triggered.connect(lambda: self.changeLanguage.emit("D"))
        languageMenu.addAction(dLanguageAction)

        fortranLanguageAction = QAction("Fortran", self)
        fortranLanguageAction.setStatusTip("Set language to Fortran")
        fortranLanguageAction.triggered.connect(lambda: self.changeLanguage.emit("Fortran"))
        languageMenu.addAction(fortranLanguageAction)

        htmlLanguageAction = QAction("HTML", self)
        htmlLanguageAction.setStatusTip("Set language to HTML")
        htmlLanguageAction.triggered.connect(lambda: self.changeLanguage.emit("HTML"))
        languageMenu.addAction(htmlLanguageAction)

        jsonLanguageAction = QAction("JSON", self)
        jsonLanguageAction.setStatusTip("Set language to JSON")
        jsonLanguageAction.triggered.connect(lambda: self.changeLanguage.emit("JSON"))
        languageMenu.addAction(jsonLanguageAction)

        luaLanguageAction = QAction("Lua", self)
        luaLanguageAction.setStatusTip("Set language to Lua")
        luaLanguageAction.triggered.connect(lambda: self.changeLanguage.emit("Lua"))
        languageMenu.addAction(luaLanguageAction)

        makefileLanguageAction = QAction("Makefile", self)
        makefileLanguageAction.setStatusTip("Set language to Makefile")
        makefileLanguageAction.triggered.connect(lambda: self.changeLanguage.emit("Makefile"))
        languageMenu.addAction(makefileLanguageAction)

        markdownLanguageAction = QAction("Markdown", self)
        markdownLanguageAction.setStatusTip("Set language to Markdown")
        markdownLanguageAction.triggered.connect(lambda: self.changeLanguage.emit("Markdown"))
        languageMenu.addAction(markdownLanguageAction)

        matlabLanguageAction = QAction("Matlab", self)
        matlabLanguageAction.setStatusTip("Set language to Matlab")
        matlabLanguageAction.triggered.connect(lambda: self.changeLanguage.emit("Matlab"))
        languageMenu.addAction(matlabLanguageAction)

        pascalLanguageAction = QAction("Pascal", self)
        pascalLanguageAction.setStatusTip("Set language to Pascal")
        pascalLanguageAction.triggered.connect(lambda: self.changeLanguage.emit("Pascal"))
        languageMenu.addAction(pascalLanguageAction)

        perlLanguageAction = QAction("Perl", self)
        perlLanguageAction.setStatusTip("Set language to Perl")
        perlLanguageAction.triggered.connect(lambda: self.changeLanguage.emit("Perl"))
        languageMenu.addAction(perlLanguageAction)

        pythonLanguageAction = QAction("Python", self)
        pythonLanguageAction.setStatusTip("Set language to Python")
        pythonLanguageAction.triggered.connect(lambda: self.changeLanguage.emit("Python"))
        languageMenu.addAction(pythonLanguageAction)

        rubyLanguageAction = QAction("Ruby", self)
        rubyLanguageAction.setStatusTip("Set language to Ruby")
        rubyLanguageAction.triggered.connect(lambda: self.changeLanguage.emit("Ruby"))
        languageMenu.addAction(rubyLanguageAction)

        sqlLanguageAction = QAction("SQL", self)
        sqlLanguageAction.setStatusTip("Set language to SQL")
        sqlLanguageAction.triggered.connect(lambda: self.changeLanguage.emit("SQL"))
        languageMenu.addAction(sqlLanguageAction)

        texLanguageAction = QAction("TeX", self)
        texLanguageAction.setStatusTip("Set language to TeX")
        texLanguageAction.triggered.connect(lambda: self.changeLanguage.emit("TeX"))
        languageMenu.addAction(texLanguageAction)

        yamlLanguageAction = QAction("YAML", self)
        yamlLanguageAction.setStatusTip("Set language to YAML")
        yamlLanguageAction.triggered.connect(lambda: self.changeLanguage.emit("YAML"))
        languageMenu.addAction(yamlLanguageAction)

        xmlLanguageAction = QAction("XML", self)
        xmlLanguageAction.setStatusTip("Set language to XML")
        xmlLanguageAction.triggered.connect(lambda: self.changeLanguage.emit("XML"))
        languageMenu.addAction(xmlLanguageAction)

    def createHelpMenu(self):
        aboutDialogAction = QAction('About', self)
        aboutDialogAction.setStatusTip('About the application.')
        aboutDialogAction.setShortcut('CTRL+H')
        aboutDialogAction.triggered.connect(lambda: self.openAboutDialog.emit())

        self.helpMenu = self.addMenu("Help")
        self.helpMenu.addAction(aboutDialogAction)
