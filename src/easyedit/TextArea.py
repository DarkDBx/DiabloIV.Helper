from PyQt5.Qsci import QsciScintilla, QsciLexerBash, QsciLexerBatch, QsciLexerCMake, QsciLexerCoffeeScript, \
    QsciLexerCPP, QsciLexerCSharp, QsciLexerCSS, QsciLexerD, QsciLexerFortran, QsciLexerHTML, QsciLexerJava, \
    QsciLexerJavaScript, QsciLexerJSON, QsciLexerLua, QsciLexerMakefile, QsciLexerMarkdown, QsciLexerMatlab, \
    QsciLexerPascal, QsciLexerPerl, QsciLexerPython, QsciLexerRuby, QsciLexerSQL, QsciLexerTeX, QsciLexerYAML, \
    QsciLexerXML


class TextArea(QsciScintilla):
    def __init__(self):
        super().__init__()

        self.languageToLexer = {
            None: None,
            'Bash': QsciLexerBash,
            'Batch': QsciLexerBatch,
            'CMake': QsciLexerCMake,
            'CoffeeScript': QsciLexerCoffeeScript,
            'C++': QsciLexerCPP,
            'C#': QsciLexerCSharp,
            'CSS': QsciLexerCSS,
            'D': QsciLexerD,
            'Fortran': QsciLexerFortran,
            'HTML': QsciLexerHTML,
            'Java': QsciLexerJava,
            'JavaScript': QsciLexerJavaScript,
            'JSON': QsciLexerJSON,
            'Lua': QsciLexerLua,
            'Makefile': QsciLexerMakefile,
            'Markdown': QsciLexerMarkdown,
            'Matlab': QsciLexerMatlab,
            'Pascal': QsciLexerPascal,
            'Perl': QsciLexerPerl,
            'Python': QsciLexerPython,
            'Ruby': QsciLexerRuby,
            'SQL': QsciLexerSQL,
            'TeX': QsciLexerTeX,
            'YAML': QsciLexerYAML,
            'XML': QsciLexerXML
        }

        self.languageToFile = {
            None: "Text Files (*.txt);;All Files (*)",
            'Bash': "Bash Files (*.sh);;All Files (*)",
            'Batch': "Batch Files (*.bat);;All Files (*)",
            'CMake': "CMake Files (*.txt);;All Files (*)",
            'CoffeeScript': "CoffeeScript Files (*.coffee);;All Files (*)",
            'C++': "C/C++ Source Files (*.c *.cpp *.cxx);;C/C++ Header Files (*.h *.hpp *.hxx);;All Files (*)",
            'C#': "C# Files (*.cs);;All Files (*)",
            'CSS': "CSS Files (*.css);;All Files (*)",
            'D': "D Files (*.d);;All Files (*)",
            'Fortran': "Fortran Files (*.f);;All Files (*)",
            'HTML': "HTML Files (*.html);;All Files (*)",
            'Java': "Java Files (*.java);;All Files (*)",
            'JavaScript': "JavaScript Files (*.js);;All Files (*)",
            'JSON': "JSON Files (*.json);;All Files (*)",
            'Lua': "Lua Files (*.lua);;All Files (*)",
            'Makefile': "All Files (*)",
            'Markdown': "Markdown Files (*.md);;All Files (*)",
            'Matlab': "Matlab Files (*.mlx);;All Files (*)",
            'Pascal': "Pascal Files (*.pas);;All Files (*)",
            'Perl': "Perl Files (*.pl);;All Files (*)",
            'Python': "Python Files (*.py);;All Files (*)",
            'Ruby': "Ruby Files (*.rb);;All Files (*)",
            'SQL': "SQL Files (*.sql);;All Files (*)",
            'TeX': "TeX Files (*.txt);;All Files (*)",
            'YAML': "YAML Files (*.yaml *.yml);;All Files (*)",
            'XML': "XML Files (*.xml);;All Files (*)"
        }

        self.filePath = "Untitled"
        self.currentLanguage = None
        self.setMargins(1)
        self.setMarginType(0, QsciScintilla.NumberMargin)
        self.setUtf8(True)
        self.setIndentationsUseTabs(False)
        self.setTabWidth(4)
        self.setIndentationGuides(False)
        self.setAutoIndent(True)
        self.setScrollWidth(1)
        self.setScrollWidthTracking(True)

    def getFileType(self):
        return self.languageToFile.get(self.currentLanguage)

    def changeLexer(self, lexer):
        if lexer is not None:
            newLexer = self.languageToLexer.get(lexer)(self)
        else:
            newLexer = lexer

        self.setLexer(newLexer)
        self.currentLanguage = lexer

    def changeMarginWidth(self):
        numLines = self.lines()

        self.setMarginWidth(0, "00" * len(str(numLines)))

    def updateFont(self, newFont):
        if self.currentLanguage is not None:
            self.lexer().setFont(newFont)
        else:
            self.setFont(newFont)
