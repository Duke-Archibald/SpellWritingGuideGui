import asyncio
import inspect
import os
import random
import sys

import numpy as np
import cmasher as cmr
import qasync
import qdarkstyle
from PIL import Image
from PIL.PngImagePlugin import PngInfo
from PyQt5.QtCore import QSettings
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QMainWindow, QComboBox, QSlider, QLineEdit, QFileDialog, QSpinBox, QColorDialog, \
    QPushButton, QCheckBox, QApplication
# from asyncqt import QEventLoop
from colour import Color
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.colors import LinearSegmentedColormap

import bases
import line_shapes
from ui.MainWindowUI import Ui_MainWindow
from writer import generate_unique_combinations, draw_multiple_inputs

os.system("pyuic5 -o ui/MainWindowUI.py ui/MainWindow.ui")
colormaps = ['custom','viridis', 'viridis_r', 'plasma', 'plasma_r', 'inferno', 'inferno_r', 'magma', 'magma_r',
             'cividis', 'cividis_r', 'Greys', 'Greys_r', 'Purples', 'Purples_r', 'Blues', 'Blues_r', 'Greens',
             'Greens_r', 'Oranges', 'Oranges_r', 'Reds', 'Reds_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 'OrRd',
             'OrRd_r', 'PuRd', 'PuRd_r', 'RdPu', 'RdPu_r', 'BuPu', 'BuPu_r', 'GnBu', 'GnBu_r', 'PuBu', 'PuBu_r',
             'YlGnBu', 'YlGnBu_r', 'PuBuGn', 'PuBuGn_r', 'BuGn', 'BuGn_r', 'YlGn', 'YlGn_r', 'binary', 'binary_r',
             'gist_yarg', 'gist_yarg_r', 'gist_gray', 'gist_gray_r', 'gray', 'gray_r', 'bone', 'bone_r', 'pink',
             'pink_r', 'spring', 'spring_r', 'summer', 'summer_r', 'autumn', 'autumn_r', 'winter', 'winter_r', 'cool',
             'cool_r', 'Wistia', 'Wistia_r', 'hot', 'hot_r', 'afmhot', 'afmhot_r', 'gist_heat', 'gist_heat_r', 'copper',
             'copper_r', 'PiYG', 'PiYG_r', 'PRGn', 'PRGn_r', 'BrBG', 'BrBG_r', 'PuOr', 'PuOr_r', 'RdGy', 'RdGy_r',
             'RdBu', 'RdBu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Spectral', 'Spectral_r', 'coolwarm',
             'coolwarm_r', 'bwr', 'bwr_r', 'seismic', 'seismic_r', 'twilight', 'twilight_r', 'twilight_shifted',
             'twilight_shifted_r', 'hsv', 'hsv_r', 'Pastel1', 'Pastel1_r', 'Pastel2', 'Pastel2_r', 'Paired', 'Paired_r',
             'Accent', 'Accent_r', 'Dark2', 'Dark2_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r', 'tab10',
             'tab10_r', 'tab20', 'tab20_r', 'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'flag', 'flag_r', 'prism',
             'prism_r', 'ocean', 'ocean_r', 'gist_earth', 'gist_earth_r', 'terrain', 'terrain_r', 'gist_stern',
             'gist_stern_r', 'gnuplot', 'gnuplot_r', 'gnuplot2', 'gnuplot2_r', 'CMRmap', 'CMRmap_r', 'cubehelix',
             'cubehelix_r', 'brg', 'brg_r', 'gist_rainbow', 'gist_rainbow_r', 'rainbow', 'rainbow_r', 'jet', 'jet_r',
             'turbo', 'turbo_r', 'nipy_spectral', 'nipy_spectral_r', 'gist_ncar', 'gist_ncar_r', 'cmr.amber',
             'cmr.amber_r', 'cmr.amethyst', 'cmr.amethyst_r', 'cmr.apple', 'cmr.apple_r', 'cmr.arctic', 'cmr.arctic_r',
             'cmr.bubblegum', 'cmr.bubblegum_r', 'cmr.chroma', 'cmr.chroma_r', 'cmr.copper', 'cmr.copper_r',
             'cmr.copper_s', 'cmr.copper_s_r', 'cmr.cosmic', 'cmr.cosmic_r', 'cmr.dusk', 'cmr.dusk_r', 'cmr.eclipse',
             'cmr.eclipse_r', 'cmr.ember', 'cmr.ember_r', 'cmr.emerald', 'cmr.emerald_r', 'cmr.emergency',
             'cmr.emergency_r', 'cmr.emergency_s', 'cmr.emergency_s_r', 'cmr.fall', 'cmr.fall_r', 'cmr.flamingo',
             'cmr.flamingo_r', 'cmr.freeze', 'cmr.freeze_r', 'cmr.fusion', 'cmr.fusion_r', 'cmr.gem', 'cmr.gem_r',
             'cmr.ghostlight', 'cmr.ghostlight_r', 'cmr.gothic', 'cmr.gothic_r', 'cmr.guppy', 'cmr.guppy_r',
             'cmr.holly', 'cmr.holly_r', 'cmr.horizon', 'cmr.horizon_r', 'cmr.iceburn', 'cmr.iceburn_r', 'cmr.infinity',
             'cmr.infinity_r', 'cmr.infinity_s', 'cmr.infinity_s_r', 'cmr.jungle', 'cmr.jungle_r', 'cmr.lavender',
             'cmr.lavender_r', 'cmr.lilac', 'cmr.lilac_r', 'cmr.neon', 'cmr.neon_r', 'cmr.neutral', 'cmr.neutral_r',
             'cmr.nuclear', 'cmr.nuclear_r', 'cmr.ocean', 'cmr.ocean_r', 'cmr.pepper', 'cmr.pepper_r', 'cmr.pride',
             'cmr.pride_r', 'cmr.prinsenvlag', 'cmr.prinsenvlag_r', 'cmr.rainforest', 'cmr.rainforest_r',
             'cmr.redshift', 'cmr.redshift_r', 'cmr.sapphire', 'cmr.sapphire_r', 'cmr.savanna', 'cmr.savanna_r',
             'cmr.seasons', 'cmr.seasons_r', 'cmr.seasons_s', 'cmr.seasons_s_r', 'cmr.seaweed', 'cmr.seaweed_r',
             'cmr.sepia', 'cmr.sepia_r', 'cmr.sunburst', 'cmr.sunburst_r', 'cmr.swamp', 'cmr.swamp_r', 'cmr.torch',
             'cmr.torch_r', 'cmr.toxic', 'cmr.toxic_r', 'cmr.tree', 'cmr.tree_r', 'cmr.tropical', 'cmr.tropical_r',
             'cmr.viola', 'cmr.viola_r', 'cmr.voltage', 'cmr.voltage_r', 'cmr.waterlily', 'cmr.waterlily_r',
             'cmr.watermelon', 'cmr.watermelon_r', 'cmr.wildfire', 'cmr.wildfire_r', 'cmr.heat', 'cmr.heat_r']
linestyle = ["solid", "dashed", "dashdot", "dotted"]


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.QcheckBox_list = []
        self.Qhs_list = []
        self.Qle_list = []
        self.Qcb_list = []
        self.Qsb_list = []
        self.QpbColor = []
        self.area = 0
        self.savename = "test.png"
        self.figure2 = plt.figure(2)
        self.figure = plt.figure(1)

        self.canvas = FigureCanvas(self.figure)
        # self.toolbar = NavigationToolbar(self.canvas, self)

        self.app = app
        self.settings = QSettings("SpwllWrittingGuide", "Gui-1")

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("MainWindow")

        # self.ui.cb_area.addItems(list(open("Attributes/area_types.txt", 'r').read().splitlines()))
        self.ui.cb_school.addItems(list(open("Attributes/school.txt", 'r').read().splitlines()))
        # self.ui.cb_range_distance.addItems(list(open("Attributes/range.txt", 'r').read().splitlines()))
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

        # self.ui.vl_1.addWidget(self.toolbar)
        self.ui.vl_1.addWidget(self.canvas)

        self.ui.cb_base_shape.currentTextChanged.connect(self.basechange)
        self.ui.cb_line_shape.currentTextChanged.connect(self.linechange)
        self.ui.cb_colormaps.currentTextChanged.connect(self.cmapchange)

        self.ui.pb_create_rune.clicked.connect(self.savespell)
        # self.ui.pb_export_png.clicked.connect(self.exportspell)
        self.ui.pb_load_rune.clicked.connect(self.loadspell)
        self.ui.pb_rollareavalue.clicked.connect(self.rollsValue)
        self.ui.pb_rollrange.clicked.connect(self.rollRange)
        self.ui.pb_self_value.clicked.connect(self.createItemArea)

        self.ui.pb_add_color_to_map.clicked.connect(self.add_color_choice)
        self.ui.pb_remove_color_to_map.clicked.connect(self.remove_color_choice)

        self.ui.cb_area_type.currentTextChanged.connect(self.createItemArea)

        self.ui.hs_line_1.valueChanged.connect(self.draw)
        self.ui.checkb_line_2.clicked.connect(self.draw)
        self.ui.hs_base_1.valueChanged.connect(self.draw)
        self.ui.hs_base_2.valueChanged.connect(self.draw)
        self.ui.hs_base_3.valueChanged.connect(self.draw)
        self.ui.hs_base_4.valueChanged.connect(self.draw)
        self.ui.hs_guide_line_size.valueChanged.connect(self.draw)
        self.ui.hs_spell_line_size.valueChanged.connect(self.draw)
        self.ui.hs_marker_size.valueChanged.connect(self.draw)

        self.ui.hs_h_loc_pos.valueChanged.connect(self.draw)
        self.ui.vs_v_loc_pos.valueChanged.connect(self.draw)

        self.ui.cb_colormaps.currentTextChanged.connect(self.draw)
        # self.ui.cb_area.currentTextChanged.connect(self.draw)
        self.ui.cb_dtype.currentTextChanged.connect(self.draw)
        self.ui.cb_level.currentTextChanged.connect(self.draw)
        self.ui.cb_school.currentTextChanged.connect(self.draw)
        # self.ui.cb_range_distance.currentTextChanged.connect(self.draw)
        # self.ui.cb_range_form.currentTextChanged.connect(self.draw)
        self.ui.cb_base_shape.currentTextChanged.connect(self.draw)
        self.ui.cb_guide_line_type.currentTextChanged.connect(self.draw)
        self.ui.cb_line_shape.currentTextChanged.connect(self.draw)

        self.ui.checkb_legend.clicked.connect(self.draw)
        self.ui.checkb_legend.clicked.connect(self.legendclicked)
        self.ui.checkb_guide_line.clicked.connect(self.draw)
        self.ui.checkb_guide_line.clicked.connect(self.guidelineclicked)
        self.ui.checkb_breakdown.clicked.connect(self.draw)
        self.ui.checkb_breakdown.clicked.connect(self.breakdownclicked)

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
        self.ui.checkb_line_2.setVisible(False)
        self.basechange()
        self.linechange()
        self.add_color_choice()
        self.add_color_choice()
        self.legendclicked()
        self.breakdownclicked()
        self.guidelineclicked()
        self.draw()

        # draws a spell given certain values by comparing it to input txt

    def add_color_choice(self, placeholder="", color="#111111"):
        button = QPushButton(color, parent=self)
        button.clicked.connect(self.chose_color)
        color = QColor(color)
        if color.isValid():
            luminace = color.red() * 0.2126 + color.green() * 0.7152 + color.blue() * 0.0722

            if luminace > 179:
                text = "#000000"
            else:
                text = "#ffffff"
            button.setStyleSheet(f'QPushButton {{background-color: {color.name()}; color: {text};}}')
        self.ui.vl_custom_color.addWidget(button)

    def remove_color_choice(self, placeholder="", index=-1):

        if index != -1:
            index = index
        else:
            index = self.ui.vl_custom_color.count() - 1
        if self.ui.vl_custom_color.count() <= 3:
            pass
        else:
            widget = self.ui.vl_custom_color.itemAt(index).widget()
            self.ui.vl_custom_color.removeWidget(widget)
            widget.deleteLater()
            widget = None

    def breakdownclicked(self):
        if self.ui.checkb_breakdown.isChecked():
            self.ui.cb_colormaps.show()
            self.ui.l_color_map_name.show()
            self.ui.pb_add_color_to_map.show()
            self.ui.pb_remove_color_to_map.show()
            for y in range(self.ui.vl_custom_color.count()):
                widget = self.ui.vl_custom_color.itemAt(y).widget()
                widget.show()
        else:
            self.ui.cb_colormaps.hide()
            self.ui.l_color_map_name.hide()
            self.ui.pb_add_color_to_map.hide()
            self.ui.pb_remove_color_to_map.hide()
            for y in range(self.ui.vl_custom_color.count()):
                widget = self.ui.vl_custom_color.itemAt(y).widget()
                widget.hide()
    def legendclicked(self):
        if self.ui.checkb_legend.isChecked():
            self.ui.hs_h_loc_pos.show()
            self.ui.vs_v_loc_pos.show()

        else:
            self.ui.hs_h_loc_pos.hide()
            self.ui.vs_v_loc_pos.hide()

    def guidelineclicked(self):
        if self.ui.checkb_guide_line.isChecked():
            self.ui.hs_guide_line_size.show()
            self.ui.cb_guide_line_type.show()
            self.ui.l_guide_line_size.show()
            self.ui.l_guide_line_type.show()
        else:
            self.ui.hs_guide_line_size.hide()
            self.ui.cb_guide_line_type.hide()
            self.ui.l_guide_line_size.hide()
            self.ui.l_guide_line_type.hide()

    def cmapchange(self):
        if self.ui.cb_colormaps.currentText() == "custom":
            custom = True
        else:
            custom = False
        self.ui.pb_add_color_to_map.setVisible(custom)
        self.ui.pb_remove_color_to_map.setVisible(custom)
        for y in range(self.ui.vl_custom_color.count()):
            widget = self.ui.vl_custom_color.itemAt(y).widget()
            widget.setVisible(custom)

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
        return int(round(random.randint(10, 200), -1) / 2)

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
            att, non_repeating = self.non_repetingcheck()
            if val > len(non_repeating):
                print("in", val)
                return checkvalue(val - (len(non_repeating) / 2))
            else:
                return int(val)

        A = int(self.ui.le_value_A.text() if self.ui.le_value_A.text().isnumeric() else 0)
        B = int(self.ui.le_value_B.text() if self.ui.le_value_B.text().isnumeric() else 0)
        C = int(self.ui.le_value_C.text() if self.ui.le_value_C.text().isnumeric() else 0)
        D = int(self.ui.le_value_D.text() if self.ui.le_value_D.text().isnumeric() else 0)
        E = int(self.ui.le_value_E.text() if self.ui.le_value_E.text().isnumeric() else 0)
        F = int(self.ui.le_value_F.text() if self.ui.le_value_F.text().isnumeric() else 0)
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
            self.area = checkvalue(E * A)
        elif index == 7:
            self.area = checkvalue(B * A)
        elif index == 8:
            self.area = checkvalue(D ** 3)
        elif index == 9:
            self.area = checkvalue(E * F * 2)
        elif index == 10:
            self.area = checkvalue(E * F * np.pi)

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
            self.ui.checkb_line_2.setVisible(False)
            self.ui.checkb_line_2.setChecked(False)
        if len(sig.parameters) - 2 >= 1:
            self.ui.labelline_2.setVisible(True)
            self.ui.checkb_line_2.setVisible(True)
            if len(sig.parameters) - 2 < 2:
                self.ui.labelline_1.setVisible(False)
                self.ui.hs_line_1.setVisible(False)
                self.ui.hs_line_1.setValue(0)
        if len(sig.parameters) - 2 >= 2:
            self.ui.labelline_1.setVisible(True)
            self.ui.hs_line_1.setVisible(True)

        for position, (name, param) in enumerate(sig.parameters.items()):
            # print(position, name)
            if position == 0:
                continue
            if position == 1:
                continue
            if position == 2:
                self.ui.labelline_2.setText(name)
            if position == 3:
                self.ui.labelline_1.setText(name)

    def exportspell(self):
        plt.figure(2)
        self.figure2.set_size_inches(20, 20)
        self.draw()

        plt.savefig(self.savename, dpi=100)
        plt.figure(1)
        self.draw()

    def savespell(self):
        self.QpbColor = []
        self.Qsb_list = []
        self.Qle_list = []
        self.Qcb_list = []
        self.Qhs_list = []
        self.QcheckBox_list = []
        metadata = PngInfo()
        for z in range(self.ui.vl_custom_color.count()):
            colorW = self.ui.vl_custom_color.itemAt(z).widget()
            if isinstance(colorW, QPushButton):
                self.QpbColor.append(colorW.text())
        for y in range(self.ui.vl_setting.count()):
            layout = self.ui.vl_setting.itemAt(y)
            for x in range(layout.count()):
                widget = layout.itemAt(x).widget()
                if isinstance(widget, QComboBox):
                    self.Qcb_list.append(widget)
                elif isinstance(widget, QSpinBox):
                    self.Qsb_list.append(widget)
                elif isinstance(widget, QLineEdit):
                    self.Qle_list.append(widget)
                elif isinstance(widget, QSlider):
                    self.Qhs_list.append(widget)
                elif isinstance(widget, QCheckBox):
                    self.QcheckBox_list.append(widget)
        plt.figure(2)
        self.figure2.set_size_inches(20, 20)
        self.draw()
        os.makedirs(self.savename.split("/")[0], exist_ok=True)
        plt.savefig(self.savename, dpi=100)
        plt.figure(1)
        self.draw()
        targetImage = Image.open(self.savename)
        for widget in self.Qcb_list:
            metadata.add_text(str(widget.objectName()), str(widget.currentText()))
        for widget in self.Qhs_list:
            metadata.add_text(str(widget.objectName()), str(widget.value()))
        for widget in self.Qle_list:
            metadata.add_text(str(widget.objectName()), str(widget.text()))
        for widget in self.Qsb_list:
            metadata.add_text(str(widget.objectName()), str(widget.value()))
        for widget in self.QcheckBox_list:
            metadata.add_text(str(widget.objectName()), str(widget.isChecked()))
        metadata.add_text(str("custom_colors"), str(self.QpbColor))

        targetImage.save(f"{self.savename.replace('.png', '.sr.png')}", "PNG", pnginfo=metadata)
        os.remove(self.savename)

    def loadspell(self):
        dialog = QFileDialog(self)
        dialog.setNameFilter("Spells rune (*.sr.png)")
        dialog.setDirectory(r'C:\Users\DukeArchibald\PycharmProjects\SpellWritingGuideGui\spells')
        if dialog.exec_():
            fileName = dialog.selectedFiles()
            targetImage = Image.open(fileName[0])
            meta = dict(targetImage.text)
            for name, value in meta.items():
                if name.split("_")[0] == "custom":
                    print("load custom", value)
                    for hex_color in eval(value):
                        print(hex_color)
                        self.add_color_choice("", hex_color)
                    for z in range(self.ui.vl_custom_color.count()):
                        print(z, self.ui.vl_custom_color.itemAt(z).widget().text())
                    self.remove_color_choice("", 1)
                    self.remove_color_choice("", 1)

                if name.split("_")[0] == "checkb":
                    QcheckB = self.findChild(QCheckBox, name)
                    QcheckB.setChecked(bool(value))
                if name.split("_")[0] == "cb":
                    Qcb = self.findChild(QComboBox, name)
                    # Qcb.blockSignals(True)
                    Qcb.setCurrentText(value)
                    # Qcb.blockSignals(False)
                elif name.split("_")[0] == "hs":
                    Qhs = self.findChild(QSlider, name)
                    Qhs.blockSignals(True)
                    Qhs.setValue(int(value))
                    Qhs.blockSignals(False)
                elif name.split("_")[0] == "le":
                    Qle = self.findChild(QLineEdit, name)
                    Qle.blockSignals(True)
                    Qle.setText(value)
                    Qle.blockSignals(False)
                elif name.split("_")[0] == "sb":
                    Qsb = self.findChild(QSpinBox, name)
                    Qsb.blockSignals(True)
                    Qsb.setValue(int(value))
                    Qsb.blockSignals(False)
            self.createItemArea()
            self.draw()
            targetImage.close()

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

        return attributes, non_repeating

    def make_Ramp(self):
        ramp_colors = []
        for y in range(self.ui.vl_custom_color.count()):
            widget = self.ui.vl_custom_color.itemAt(y).widget()
            if isinstance(widget, QPushButton):
                ramp_colors.append(widget.text())

        color_ramp = LinearSegmentedColormap.from_list('custom', [Color(c1).rgb for c1 in ramp_colors])
        return color_ramp

    def chose_color(self):
        color = QColorDialog.getColor()

        if color.isValid():
            luminace = color.red() * 0.2126 + color.green() * 0.7152 + color.blue() * 0.0722

            if luminace > 179:
                text = "#000000"
            else:
                text = "#ffffff"
            self.sender().setStyleSheet(f'QPushButton {{background-color: {color.name()}; color: {text};}}')
            self.sender().setText(color.name())

    def draw(self):

        self.figure.clear()

        if self.ui.cb_colormaps.currentText() == "custom":
            cmap = self.make_Ramp()
        else:
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
        base_kwargs = [self.ui.hs_base_1.value() / 1000, self.ui.hs_base_2.value() / 100,
                       self.ui.hs_base_3.value() / 100, self.ui.hs_base_4.value() / 100, ]
        shape_kwargs = [self.ui.checkb_line_2.isChecked(), self.ui.hs_line_1.value() / 100]
        labels = [f"level: {level}",
                  f"school: {school}",
                  f"damage type: {dtype}",
                  f"range: {rang}",
                  f"area_type: {area}"]
        attributes, non_repeating = self.non_repetingcheck()
        for x, attribute in enumerate(attributes):
            if attribute > len(non_repeating):
                attributes[x] = attribute - len(non_repeating)
        if len(colors) == 0 and breakdown is True:
            colors = [cmap(i / len(attributes)) for i in range(len(attributes))]
        title = f"spell level {level} from the {school} school,\n range of {rang} {area} with {dtype} damage type"
        title_filenameclean = title.replace("\n", "").replace("/", "-")
        self.savename = f"spells/{title_filenameclean} legend-{legend} breakdown-{breakdown}.png"
        self.savename = self.savename.replace(" ", "_")
        input_array = np.array(
            [non_repeating[i] for i in attributes])  # note +1 s.t. 0th option is always open for empty input
        draw_multiple_inputs(self.figure, self.figure2, self.ui, input_array, labels=labels, legend=legend,
                             base_fn=base, base_kwargs=base_kwargs,
                             shape_fn=lines, shape_kwargs=shape_kwargs,
                             colors=colors)
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)

    dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()
    app.setStyleSheet(dark_stylesheet + "QMessageBox { messagebox-text-interaction-flags: 5; }")
    app.setWindowIcon(QIcon('5f8fc82c7f3c699f8c34e3313027559d_original.png'))

    with loop:
        main = MainWindow()
        main.show()
        loop.run_forever()
