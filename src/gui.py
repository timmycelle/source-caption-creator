from shared import *
from core import file

from srctools import game
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QMenuBar,
    QMenu,
    QStyleFactory
)
from PySide6.QtCore import (
    QSettings
)

import sys
import json
#from pathlib import Path

args = parser.parse_args()

class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        self.settings = QSettings("timmycelle", name)

        self.current_style = str(self.settings.value("style", "Fusion", type=str))

        self.setWindowTitle(name)
        self.resize(800, 600)

        self.menubar = QMenuBar()
        self.menuFile = QMenu("File")
        self.menuEdit = QMenu("Edit")
        self.menuSettings = QMenu("Settings")
        self.menuHelp = QMenu("Help")
        self.menubar.addMenu(self.menuFile)
        self.menubar.addMenu(self.menuEdit)
        self.menubar.addMenu(self.menuSettings)
        self.menubar.addMenu(self.menuHelp)

        self.menuSettingsDesign = self.menuSettings.addMenu("Design")
        for design in QStyleFactory.keys():
            action = self.menuSettingsDesign.addAction(design)
            action.triggered.connect(lambda checked=False, d=design: self.changeStyle(d))

        self.setMenuBar(self.menubar)

        QApplication.setStyle(QStyleFactory.create(self.current_style))

    def showEvent(self, event):
        #self.setup()
        event.accept()

    def setup(self):
        print("setuP!")
        SCC.p_game = QFileDialog.getExistingDirectory(caption="Source Engine game directory")
        #QFileDialog.getOpenFileName(caption="JSON Caption File", filter="*.json", dir=SCC.game)[0]
        print(SCC.p_game)
        #SCC.game = game.Game(SCC.p_game)
        """if SCC.game.game_name:
            self.setWindowTitle(f"{name} | {SCC.game.game_name} ({Path(SCC.p_game).name})")
        else:
            self.setWindowTitle(f"{name} | {Path(SCC.p_game).name}")"""
    
    def changeStyle(self, style):
        QApplication.setStyle(QStyleFactory.create(style))
        self.current_style = style
        self.settings.setValue("style", style)

        for action in self.menuSettingsDesign.actions():
            if action.text() == style:
                action.setCheckable(True)
                action.setChecked(True)
            else:
                action.setCheckable(False)

        #log(f"Set style '{style}'", f"{name}:style", frm["INFO"])

def main():
    app = QApplication(sys.argv)
    app.setApplicationName(name)
    app.processEvents()
    win = Main()
    win.show()
    sys.exit(app.exec())
if __name__ == "__main__":
    main()