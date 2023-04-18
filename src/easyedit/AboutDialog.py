from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout


class AboutDialog(QDialog):
    """Create the necessary elements to show helpful text in a dialog."""

    def __init__(self, parent=None):
        """Display a dialog that shows application information."""
        super(AboutDialog, self).__init__(parent)

        self.setWindowTitle('About')
        self.setWindowIcon(QIcon("help.png"))
        self.resize(300, 200)

        title = QLabel('EasyEdit\n\nBy:\n')
        title.setAlignment(Qt.AlignCenter)

        author = QLabel('Matthew S. Klosak')
        author.setAlignment(Qt.AlignCenter)

        github = QLabel('<a href="https://github.com/msklosak/EasyEdit/">GitHub</a>')
        github.setOpenExternalLinks(True)
        github.setAlignment(Qt.AlignCenter)

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignVCenter)

        self.layout.addWidget(title)
        self.layout.addWidget(author)
        self.layout.addWidget(github)

        self.setLayout(self.layout)
