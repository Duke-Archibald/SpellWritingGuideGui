import asyncio
import inspect
import os
import sys

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
colormaps = ['viridis', 'plasma', 'inferno', 'magma', 'cividis', 'Greys', 'Purples', 'Blues', 'Greens', 'Oranges',
             'Reds',
             'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
             'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn', 'binary', 'gist_yarg', 'gist_gray', 'gray', 'bone',
             'pink', 'spring', 'summer', 'autumn', 'winter', 'cool',
             'Wistia', 'hot', 'afmhot', 'gist_heat', 'copper', 'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu', 'RdYlBu',
             'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic', 'twilight', 'twilight_shifted', 'hsv', 'Pastel1',
             'Pastel2', 'Paired', 'Accent', 'Dark2',
             'Set1', 'Set2', 'Set3', 'tab10', 'tab20', 'tab20b',
             'tab20c', 'flag', 'prism', 'ocean', 'gist_earth', 'terrain',
             'gist_stern', 'gnuplot', 'gnuplot2', 'CMRmap',
             'cubehelix', 'brg', 'gist_rainbow', 'rainbow', 'jet',
             'turbo', 'nipy_spectral', 'gist_ncar']


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.savename = None
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
        self.ui.cb_colormaps.addItems(colormaps)
        self.ui.cb_base_shape.addItems([attribute for attribute in dir(bases) if
                                        callable(getattr(bases, attribute)) and attribute.startswith('__') is False]
                                       )
        self.ui.cb_line_shape.addItems([attribute for attribute in dir(line_shapes) if
                                        callable(getattr(line_shapes, attribute)) and attribute.startswith(
                                            '__') is False]
                                       )
        self.ui.cb_base_shape.currentTextChanged.connect(self.basechange)
        self.ui.cb_line_shape.currentTextChanged.connect(self.linechange)
        self.figure = plt.figure(figsize=(4, 4))
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.ui.vl_1.addWidget(self.toolbar)
        self.ui.vl_1.addWidget(self.canvas)
        self.ui.pb_create_rune.clicked.connect(self.savespell)
        self.ui.hs_line_1.valueChanged.connect(self.draw)
        self.ui.hs_line_2.clicked.connect(self.draw)
        self.ui.hs_base_1.valueChanged.connect(self.draw)
        self.ui.hs_base_2.valueChanged.connect(self.draw)
        self.ui.hs_base_3.valueChanged.connect(self.draw)
        self.ui.hs_base_4.valueChanged.connect(self.draw)
        self.ui.labelbase_1.setVisible(False)
        self.ui.hs_base_1.setVisible(False)

        self.ui.labelbase_2.setVisible(False)
        self.ui.hs_base_2.setVisible(False)

        self.ui.labelbase_3.setVisible(False)
        self.ui.hs_base_3.setVisible(False)

        self.ui.labelbase_4.setVisible(False)
        self.ui.hs_base_4.setVisible(False)

        self.ui.labelline_1.setVisible(False)
        self.ui.hs_line_1.setVisible(False)

        self.ui.labelline_2.setVisible(False)
        self.ui.hs_line_2.setVisible(False)
        self.basechange()
        self.linechange()

    def basechange(self):
        self.ui.hs_base_1.blockSignals(True)
        self.ui.hs_base_2.blockSignals(True)
        self.ui.hs_base_3.blockSignals(True)
        self.ui.hs_base_4.blockSignals(True)
        self.ui.hs_base_1.setValue(0)
        self.ui.hs_base_2.setValue(0)
        self.ui.hs_base_3.setValue(0)
        self.ui.hs_base_4.setValue(0)
        self.ui.hs_base_1.blockSignals(False)
        self.ui.hs_base_2.blockSignals(False)
        self.ui.hs_base_3.blockSignals(False)
        self.ui.hs_base_4.blockSignals(False)

        func = getattr(bases, self.ui.cb_base_shape.currentText())
        sig = inspect.signature(func)
        if len(sig.parameters) - 1 <= 0:
            self.ui.labelbase_1.setVisible(False)
            self.ui.hs_base_1.setVisible(False)
            self.ui.hs_base_1.setValue(0)

            self.ui.labelbase_2.setVisible(False)
            self.ui.hs_base_2.setVisible(False)
            self.ui.hs_base_2.setValue(0)

            self.ui.labelbase_3.setVisible(False)
            self.ui.hs_base_3.setVisible(False)
            self.ui.hs_base_3.setValue(0)

            self.ui.labelbase_4.setVisible(False)
            self.ui.hs_base_4.setVisible(False)
            self.ui.hs_base_4.setValue(0)
        if len(sig.parameters) - 1 >= 1:
            self.ui.labelbase_1.setVisible(True)
            self.ui.hs_base_1.setVisible(True)
            if len(sig.parameters) - 1 < 2:
                self.ui.labelbase_2.setVisible(False)
                self.ui.hs_base_2.setVisible(False)
                self.ui.hs_base_2.setValue(0)

                self.ui.labelbase_3.setVisible(False)
                self.ui.hs_base_3.setVisible(False)
                self.ui.hs_base_3.setValue(0)

                self.ui.labelbase_4.setVisible(False)
                self.ui.hs_base_4.setVisible(False)
                self.ui.hs_base_4.setValue(0)
        if len(sig.parameters) - 1 >= 2:
            self.ui.labelbase_2.setVisible(True)
            self.ui.hs_base_2.setVisible(True)
            if len(sig.parameters) - 1 < 3:
                self.ui.labelbase_3.setVisible(False)
                self.ui.hs_base_3.setVisible(False)
                self.ui.hs_base_3.setValue(0)

                self.ui.labelbase_4.setVisible(False)
                self.ui.hs_base_4.setVisible(False)
                self.ui.hs_base_4.setValue(0)
        if len(sig.parameters) - 1 >= 3:
            self.ui.labelbase_3.setVisible(True)
            self.ui.hs_base_3.setVisible(True)
            if len(sig.parameters) - 1 < 4:
                self.ui.labelbase_4.setVisible(False)
                self.ui.hs_base_4.setVisible(False)
                self.ui.hs_base_4.setValue(0)

        if len(sig.parameters) - 1 >= 4:
            self.ui.labelbase_4.setVisible(True)
            self.ui.hs_base_4.setVisible(True)

        for position, (name, param) in enumerate(sig.parameters.items()):
            if position == 0:
                continue
            if position == 1:
                self.ui.labelbase_1.setText(name)
            if position == 2:
                self.ui.labelbase_2.setText(name)
            if position == 3:
                self.ui.labelbase_3.setText(name)
            if position == 4:
                self.ui.labelbase_4.setText(name)

    def linechange(self):
        self.ui.hs_line_1.blockSignals(True)
        self.ui.hs_line_1.setValue(0)
        self.ui.hs_line_1.blockSignals(False)
        # self.ui.hs_line_2.setValue(0)
        func = getattr(line_shapes, self.ui.cb_line_shape.currentText())
        sig = inspect.signature(func)
        if len(sig.parameters) - 2 <= 0:
            self.ui.labelline_1.setVisible(False)
            self.ui.hs_line_1.setVisible(False)
            self.ui.hs_line_1.setValue(0)

            self.ui.labelline_2.setVisible(False)
            self.ui.hs_line_2.setVisible(False)
            self.ui.hs_line_2.setChecked(False)
        if len(sig.parameters) - 2 >= 1:
            self.ui.labelline_2.setVisible(True)
            self.ui.hs_line_2.setVisible(True)
            if len(sig.parameters) - 2 < 2:
                self.ui.labelline_1.setVisible(False)
                self.ui.hs_line_1.setVisible(False)
                self.ui.hs_line_1.setValue(0)
        if len(sig.parameters) - 2 >= 2:
            self.ui.labelline_1.setVisible(True)
            self.ui.hs_line_1.setVisible(True)

        for position, (name, param) in enumerate(sig.parameters.items()):
            print(position, name)
            if position == 0:
                continue
            if position == 1:
                continue
            if position == 2:
                self.ui.labelline_2.setText(name)
            if position == 3:
                self.ui.labelline_1.setText(name)

    def savespell(self):
        plt.savefig(self.savename, dpi=250)

    def draw(self):

        self.figure.clear()
        level = self.ui.cb_level.currentText().lower()
        school = self.ui.cb_school.currentText().lower()
        area = self.ui.cb_area.currentText().lower()
        dtype = self.ui.cb_dtype.currentText().lower()
        rang = self.ui.cb_range_distance.currentText().lower() + self.ui.cb_range_form.currentText().lower()
        legend = self.ui.checkb_legend.isChecked()
        breakdown = self.ui.checkb_breakdown.isChecked()
        base = getattr(bases, self.ui.cb_base_shape.currentText())
        lines = getattr(line_shapes, self.ui.cb_line_shape.currentText())
        base_kwargs = [self.ui.hs_base_1.value() / 100, self.ui.hs_base_2.value() / 100,
                       self.ui.hs_base_3.value() / 100, self.ui.hs_base_4.value() / 100, ]
        shape_kwargs = [ self.ui.hs_line_2.isChecked(),self.ui.hs_line_1.value() / 100]
        print(shape_kwargs)
        title = f"spell level {level} from the {school} school,\n range of {rang} {area} with {dtype} damage type"
        title_filenameclean = title.replace("\n", "").replace("/", "-")
        self.savename = f"spells/{title_filenameclean} legend-{legend} breakdown-{breakdown}.png"
        draw_spell(self.ui, level, rang, area, dtype, school, title=title, legend=legend,
                   base_fn=base, base_kwargs=base_kwargs, shape_fn=lines, shape_kwargs=shape_kwargs,
                   breakdown=breakdown)
        self.canvas.draw()


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
