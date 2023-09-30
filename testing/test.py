import sys

import cmasher as cmasher
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QColorDialog


class ButtonColorChangerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the window properties (title and initial size)
        self.setWindowTitle("Button Color Changer")
        self.setGeometry(100, 100, 300, 200)  # (x, y, width, height)

        # Create a central widget for the main window
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create a QPushButton with an initial text
        self.button2 = QPushButton("Click me to change the color and text!")
        self.button = QPushButton("Click me to change the color and text!")
        self.button.clicked.connect(self.change_button_color)
        self.button2.clicked.connect(self.change_button_color)

        # Create a layout for the central widget and add the button
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.button2)

        # Set the layout for the central widget
        central_widget.setLayout(layout)

    def change_button_color(self):

        color = QColorDialog.getColor()

        if color.isValid():
            # print(color.red(),color.green(),color.blue())
            luminace = color.red()* 0.2126 + color.green() * 0.7152 + color.blue() * 0.0722

        if luminace > 179:
            text = "#000000"
        else:
            text = "#ffffff"
        self.sender().setStyleSheet(f'QPushButton {{background-color: {color.name()}; color: {text};}}')
        self.sender().setText(color.name())
        print(self.sender().text())

def main():
    app = QApplication(sys.argv)
    window = ButtonColorChangerApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    masher = cmasher.get_cmap_list()
    colormaps = ['viridis', 'plasma', 'inferno', 'magma', 'cividis', 'Greys', 'Purples', 'Blues', 'Greens',
                 'Oranges',
                 'Reds',
                 'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
                 'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn', 'binary', 'gist_yarg', 'gist_gray', 'gray', 'bone',
                 'pink', 'spring', 'summer', 'autumn', 'winter', 'cool',
                 'Wistia', 'hot', 'afmhot', 'gist_heat', 'copper', 'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu',
                 'RdYlBu',
                 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic', 'twilight', 'twilight_shifted', 'hsv', 'Pastel1',
                 'Pastel2', 'Paired', 'Accent', 'Dark2',
                 'Set1', 'Set2', 'Set3', 'tab10', 'tab20', 'tab20b',
                 'tab20c', 'flag', 'prism', 'ocean', 'gist_earth', 'terrain',
                 'gist_stern', 'gnuplot', 'gnuplot2', 'CMRmap',
                 'cubehelix', 'brg', 'gist_rainbow', 'rainbow', 'jet',
                 'turbo', 'nipy_spectral', 'gist_ncar']
    colormaps_r = []
    for x in colormaps:
        colormaps_r.append(x+"_r")
    colormaps_full = [j for i in zip(colormaps,colormaps_r) for j in i]
    mashed = ["cmr."+maps for maps in masher]
    print(colormaps_full+mashed)

