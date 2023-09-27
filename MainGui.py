import asyncio
import inspect
import os
import random
import sys

import numpy as np
import qdarkstyle
from PyQt5.QtCore import QSettings
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QComboBox
from asyncqt import QApplication, QEventLoop
from librosa.display import cmap
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

import bases
import line_shapes
from ui.MainWindowUI import Ui_MainWindow
from writer import draw_spell, generate_unique_combinations, load_attribute, draw_multiple_inputs

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
linestyle = ["solid", "dashed", "dashdot", "dotted"]


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.area = 0
        self.savename = "test.png"
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
        self.ui.cb_guide_line_type.addItems(linestyle)
        self.ui.cb_base_shape.currentTextChanged.connect(self.basechange)
        self.ui.cb_line_shape.currentTextChanged.connect(self.linechange)
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.ui.vl_1.addWidget(self.toolbar)
        self.ui.vl_1.addWidget(self.canvas)
        self.ui.pb_create_rune.clicked.connect(self.savespell)
        self.ui.pb_rollareavalue.clicked.connect(self.rollsValue)
        self.ui.pb_rollrange.clicked.connect(self.rollRange)
        self.ui.pb_self_value.clicked.connect(self.createItemArea)
        self.ui.cb_area_type.currentTextChanged.connect(self.createItemArea)
        self.ui.hs_line_1.valueChanged.connect(self.draw)
        self.ui.hs_line_2.clicked.connect(self.draw)
        self.ui.hs_base_1.valueChanged.connect(self.draw)
        self.ui.hs_base_2.valueChanged.connect(self.draw)
        self.ui.hs_base_3.valueChanged.connect(self.draw)
        self.ui.hs_base_4.valueChanged.connect(self.draw)
        self.ui.cb_colormaps.currentTextChanged.connect(self.draw)
        self.ui.cb_area.currentTextChanged.connect(self.draw)
        self.ui.cb_dtype.currentTextChanged.connect(self.draw)
        self.ui.cb_level.currentTextChanged.connect(self.draw)
        self.ui.cb_school.currentTextChanged.connect(self.draw)
        self.ui.cb_range_distance.currentTextChanged.connect(self.draw)
        self.ui.cb_range_form.currentTextChanged.connect(self.draw)
        self.ui.checkb_legend.clicked.connect(self.draw)
        self.ui.checkb_breakdown.clicked.connect(self.draw)
        self.ui.pb_rollareavalue.clicked.connect(self.draw)
        self.ui.pb_rollrange.clicked.connect(self.draw)
        self.ui.pb_self_value.clicked.connect(self.draw)
        self.ui.cb_area_type.currentTextChanged.connect(self.draw)

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

        # draws a spell given certain values by comparing it to input txt

    def rollsValue(self):
        self.ui.le_value_A.setText(str(self.rollA()))
        self.ui.le_value_B.setText(str(self.rollB()))
        self.ui.le_value_C.setText(str(self.rollB()))
        self.ui.le_value_D.setText(str(self.rollD()))
        self.ui.le_value_E.setText(str(self.rollE()))
        self.ui.le_value_F.setText(str(self.rollF()))
        self.createItemArea()

    def rollA(self):

        return random.randint(1, 10)

    def rollB(self):
        return int(round(random.randint(10, 200), -1)/2)

    # def rollC(self):
    #
    #     return int(round(random.randint(1, 100) / 2, -1))

    def rollD(self):

        return random.randint(1, 4)

    def rollE(self):

        return random.randint(1, 8)

    def rollF(self):

        return random.randint(0, 9)

    def rollRange(self):
        result = random.randint(0, 5)

        if result == 0:
            result = "Touch"
            self.ui.l_feets.setText("")
        elif result == 5:
            result = "up to 300"
            self.ui.l_feets.setText("Feets")
        else:
            result = result * 30
            self.ui.l_feets.setText("Feets")
        self.ui.le_range.setText(str(result))

    def createItemArea(self):

        def checkvalue(val):
            att,non_repeating = self.non_repetingcheck()
            if val > len(non_repeating):
                print("in",val)
                return checkvalue(val - (len(non_repeating)/2))
            else:
                return int(val)
        A = int(self.ui.le_value_A.text())
        B = int(self.ui.le_value_B.text())
        C = int(self.ui.le_value_C.text())
        D = int(self.ui.le_value_D.text())
        E = int(self.ui.le_value_E.text())
        F = int(self.ui.le_value_F.text())
        self.ui.cb_area_type.setItemText(3, f"Wall {B} feet long, {C} feet tall, {A} feet thick")
        self.ui.cb_area_type.setItemText(4, f"Sphere of radius {D} feet")
        self.ui.cb_area_type.setItemText(5, f"Cylinder of radius {D} feets, {C} feets tall")
        self.ui.cb_area_type.setItemText(6, f"{E} feets Cone")
        self.ui.cb_area_type.setItemText(7, f"{B} feets line, {A} feets thick")
        self.ui.cb_area_type.setItemText(8, f"{D} feets Cube")
        self.ui.cb_area_type.setItemText(9, f"{E} feets Square {F} feets of the ground")
        self.ui.cb_area_type.setItemText(10, f"{E} feets Circle {F} feets of the ground")
        if type(self.sender()) == QComboBox:
            pass
        else:
            self.ui.cb_area_type.setCurrentIndex(int(A))
        index = self.ui.cb_area_type.currentIndex()
        if index == 1:
            self.area = 1
        elif index == 2:
            self.area = 2
        elif index == 3:
            self.area = checkvalue(int(((B * C) / 10) * A))
        elif index == 4:
            self.area = checkvalue(D ** 2)
        elif index == 5:
            self.area = checkvalue(D * C)

        elif index == 6:
            self.area = checkvalue(E*A)
        elif index == 7:
            self.area = checkvalue(B*A)
        elif index == 8:
            self.area = checkvalue(D**3)
        elif index == 9:
            self.area = checkvalue(E*F*2)
        elif index == 10:
            self.area = checkvalue(E*F*np.pi)

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


    def non_repetingcheck(self):
        i_range = 0
        if self.ui.le_range.text().lower() == "touch":
            i_range = 0
        elif self.ui.le_range.text().lower() == "up to 300":
            i_range = 300
        elif self.ui.le_range.text().isnumeric():
            i_range = int(self.ui.le_range.text())
        i_levels = self.ui.cb_level.currentIndex()
        i_area = self.area
        i_dtype = self.ui.cb_dtype.currentIndex()
        i_school = self.ui.cb_school.currentIndex()
        attributes = [i_levels, i_school, i_dtype, i_range, i_area]
        N = 2 * len(attributes) + 1

        if not os.path.isdir("Uniques/"):
            os.makedirs("Uniques/")
        if os.path.isfile(f'Uniques/{N}.npy'):
            non_repeating = np.load(f'Uniques/{N}.npy')
        else:
            non_repeating = generate_unique_combinations(N)
            non_repeating = np.array(non_repeating)
            np.save(f"Uniques/{N}.npy", non_repeating)
        return attributes,non_repeating
    def draw(self):

        self.figure.clear()
        cmap = plt.get_cmap(self.ui.cb_colormaps.currentText())
        colors = []
        level = self.ui.cb_level.currentText().lower()
        school = self.ui.cb_school.currentText().lower()
        area = self.ui.cb_area_type.currentText().lower()
        dtype = self.ui.cb_dtype.currentText().lower()
        rang = self.ui.le_range.text()
        legend = self.ui.checkb_legend.isChecked()
        breakdown = self.ui.checkb_breakdown.isChecked()
        base = getattr(bases, self.ui.cb_base_shape.currentText())
        lines = getattr(line_shapes, self.ui.cb_line_shape.currentText())
        base_kwargs = [self.ui.hs_base_1.value() / 100, self.ui.hs_base_2.value() / 100,
                       self.ui.hs_base_3.value() / 100, self.ui.hs_base_4.value() / 100, ]
        shape_kwargs = [self.ui.hs_line_2.isChecked(), self.ui.hs_line_1.value() / 100]
        labels = [f"level: {level}",
                  f"school: {school}",
                  f"damage type: {dtype}",
                  f"range: {rang}",
                  f"area_type: {area}"]
        attributes, non_repeating = self.non_repetingcheck()
        if len(colors) == 0 and breakdown is True:
            colors = [cmap(i / len(attributes)) for i in range(len(attributes))]
        title = f"spell level {level} from the {school} school,\n range of {rang} {area} with {dtype} damage type"
        title_filenameclean = title.replace("\n", "").replace("/", "-")
        self.savename = f"spells/{title_filenameclean} legend-{legend} breakdown-{breakdown}.png"
        # draw_spell(self.figure, self.ui, level, rang, self.area, dtype, school, title=title, legend=legend,
        #            base_fn=base, base_kwargs=base_kwargs, shape_fn=lines, shape_kwargs=shape_kwargs,
        #            breakdown=breakdown, colors=colors)
        input_array = np.array(
            [non_repeating[i] for i in attributes])  # note +1 s.t. 0th option is always open for empty input
        draw_multiple_inputs(self.figure, self.ui, input_array, labels=labels, legend=legend,
                             base_fn=base, base_kwargs=base_kwargs,
                             shape_fn=lines, shape_kwargs=shape_kwargs,
                             colors=colors)
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
