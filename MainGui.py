import asyncio
import faulthandler
import getpass
import os
import socket
import sys
import time

import qdarkstyle
from PyQt5.QtCore import QSettings
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow
from asyncqt import QApplication, QEventLoop
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


import bases
import line_shapes
from ui.MainWindowUI import Ui_MainWindow
from writer import draw_spell

os.system("pyuic5 -o ui/MainWindowUI.py ui/MainWindow.ui")
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.app = app
        self.settings = QSettings("SpwllWrittingGuide", "Gui-1")

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("MainWindow")
        self.ui.cb_area.addItems(list(open("Attributes/area_types.txt", 'r').read().splitlines()))
        self.ui.cb_school.addItems(list(open("Attributes/school.txt", 'r').read().splitlines()))
        self.ui.cb_range_distance.addItems(list(open("Attributes/range.txt", 'r').read().splitlines()))
        self.ui.cb_dtype.addItems(list(open("Attributes/damage_types.txt", 'r').read().splitlines()))
        self.ui.cb_level.addItems(list(open("Attributes/levels.txt", 'r').read().splitlines()))
        self.figure = plt.figure(figsize=(4, 4))
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.ui.vl_1.addWidget(self.toolbar)
        self.ui.vl_1.addWidget(self.canvas)
        self.ui.pb_create_rune.clicked.connect(self.draw)
    def draw(self):
        self.figure.clear()
        level = self.ui.cb_level.currentText().lower()
        school = self.ui.cb_school.currentText().lower()
        area = self.ui.cb_area.currentText().lower()
        dtype = self.ui.cb_dtype.currentText().lower()
        rang = self.ui.cb_range_distance.currentText().lower() + self.ui.cb_range_form.currentText().lower()
        legend = self.ui.checkb_legend.isChecked()
        breakdown = self.ui.checkb_breakdown.isChecked()
        title = f"spell level {level} from the {school} school,\n range of {rang} {area} with {dtype} damage type"
        title_filenameclean = title.replace("\n","").replace("/","-")
        savename = f"spells/{title_filenameclean} legend-{legend} breakdown-{breakdown}.png"
        draw_spell(level, rang, area, dtype, school, title=title, legend=legend,
                   base_fn=bases.polygon, shape_fn=line_shapes.straight,
                   breakdown=breakdown, savename=savename)
if __name__ == "__main__":

    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()
    app.setStyleSheet(dark_stylesheet + "QMessageBox { messagebox-text-interaction-flags: 5; }")
    app.setWindowIcon(QIcon('resources/bookicon.png'))

    with loop:
            main = MainWindow()
            main.show()
            loop.run_forever()