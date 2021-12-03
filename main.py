import matplotlib as matplotlib
import pandas as pd
import numpy as np
import qdarkstyle
from PyQt5 import QtWidgets, uic
matplotlib.use('Qt5Agg')
from matplotlib.pyplot import isinteractive
from PyQt5 import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import sys


class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure()
        self.axes = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.fig.tight_layout()
        self.axes.grid()

class Main_window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Main_window, self).__init__()
        uic.loadUi('Team7_on_fire.ui', self)
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
        # Menu Bar
        self.menubar = self.findChild(QtWidgets.QMenuBar, "menubar")
        self.menuFile  = self.menubar.findChild(QtWidgets.QMenu,"menuFile")
        print(type(self.menuFile))
        self.menuFile.addAction("open",self.open_file)
        #   =self.menuFile.findChild(QtWidgets.QAction,"actionoppppen")
        # print(type(self.openAction))

        # graph layout
        self.graph_layout = self.findChild(QtWidgets.QVBoxLayout, "graph_Layout")


        # Radio_butto_Layout
        # radio buttons
        self.one_chunk_button = self.findChild(QtWidgets.QRadioButton, "one_chunk")
        self.multiple_chunks_button = self.findChild(QtWidgets.QRadioButton, "mlutiple_chunks")

        # grid layout
        # sliders
        self.data_percentage_slider = self.findChild(QtWidgets.QSlider, "data_percentage_slider")
        self.number_of_chunks_slider = self.findChild(QtWidgets.QSlider, "number_of_chunks_slider")
        self.polynomial_degree_slider = self.findChild(QtWidgets.QSlider, "polynomial_degree_slider")
        self.sliders_arr = [self.data_percentage_slider, self.number_of_chunks_slider,self.polynomial_degree_slider]


        # lables
        self.data_percentage_label = self.findChild(QtWidgets.QLabel, "data_percentage_label")
        self.number_of_chunks_lable = self.findChild(QtWidgets.QLabel, "number_of_chunks_lable")
        self.degree_lable = self.findChild(QtWidgets.QLabel, "degree_lable")
        self.lables_arr =[ self.data_percentage_label, self.number_of_chunks_lable,
                                self.degree_lable]
        self.lable_3 = self.findChild(QtWidgets.QLabel, "label_3")

        #Buttons
        self.ploting_button = self.findChild(QtWidgets.QPushButton,"start_button")


        # canves widget
        self.canves  = MplCanvas()
        self.graph_layout.addWidget(self.canves )

        # init:
        self.init_visability_with_radio_buttons()

        # signals
        #   radio button(multiple)
        self.multiple_chunks_button.toggled.connect(self.setting_chunks_mode)
        #   signal func arr
        self.signals_func_arr = [lambda value , i =0:self.slider_updated(value,i),lambda value , i =1:self.slider_updated(value , i),
                                 lambda value , i =2:self.slider_updated(value , i) ]

        for i in range(len(self.sliders_arr)):
            self.sliders_arr[i].valueChanged.connect(self.signals_func_arr[i])

        # Plot button signal
        self.ploting_button.clicked.connect(self.plot_data)
        # self.openAction.triggered.connect(self.open_file())

    def init_visability_with_radio_buttons(self):
        self.one_chunk_button.setChecked(True)
        self.setting_chunks_mode()


    def setting_chunks_mode(self):
        if self.multiple_chunks_button.isChecked():
            self.number_of_chunks_slider.show()
            self.lable_3.show()
            self.number_of_chunks_lable.show()
        else:
            self.number_of_chunks_slider.hide()
            self.lable_3.hide()
            self.number_of_chunks_lable.hide()


    def slider_updated(self, value,i):
        self.lables_arr[i].setText(str(value))


    def open_file(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName()
        if filename:
            self.loaded_data = pd.read_csv(filename)
            self.x_scattered_points = self.loaded_data[self.loaded_data.columns[0]].to_numpy()
            self.y_scattered_points = self.loaded_data[self.loaded_data.columns[1]].to_numpy()

        print(self.x_scattered_points)

    def plot_data(self):
        self.canves.axes.plot(self.x_scattered_points,self.y_scattered_points,"-o")
        self.canves.draw()



def main():
    app = QtWidgets.QApplication(sys.argv)
    main = Main_window()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
