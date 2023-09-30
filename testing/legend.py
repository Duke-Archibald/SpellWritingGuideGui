import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (

    QApplication,

    QHBoxLayout,

    QPushButton,

    QWidget, QGridLayout, QSlider,

)
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class Window(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("QHBoxLayout Example")
        self.figure = plt.figure()

        self.canvas = FigureCanvas(self.figure)

        # Create a QHBoxLayout instance

        layout = QGridLayout()

        # Add widgets to the layout
        self.sliderh = QSlider(Qt.Orientation.Horizontal, self)
        self.sliderv = QSlider(Qt.Orientation.Vertical, self)
        layout.addWidget(self.sliderh,0,1)

        layout.addWidget(self.sliderv,1,0)
        layout.addWidget(self.canvas,1,1)
        self.sliderv.valueChanged.connect(self.legend)
        self.sliderh.valueChanged.connect(self.legend)
        plt.plot([1, 2, 3], label='Line 2')
        self.figure.legend(loc='outside upper left')


        # Set the layout on the application's window

        self.setLayout(layout)

        print(self.children())

    def legend(self):
        self.figure.clear()
        y = self.sliderv.value() / 10
        x = self.sliderh.value() / 10
        print(x,y)
        plt.plot([1, 2, 3], label='Line 2')
        self.figure.legend(loc='outside upper left',bbox_to_anchor=(x, y))
        self.canvas.draw()


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = Window()

    window.show()

    sys.exit(app.exec_())