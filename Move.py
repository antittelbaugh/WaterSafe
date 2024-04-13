import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QStatusBar, QLabel, QSlider, QGroupBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPainterPath, QBrush, QColor
from PyQt5.QtCore import QRectF
from PyQt5 import QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from skimage.filters import threshold_otsu
from skimage import io
from skimage.color import rgb2gray, label2rgb
from skimage.measure import label, regionprops_table
from skimage.morphology import closing
import pandas as pd
from Aquisition import run_single_camera


class ImageViewerWidget(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor="#2A2E34")
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.setParent(parent)
        self.setGeometry(39, 122, 290, 319)
        self.ax.axis('off')
        self.border_radius = 20
        self.background_painted = False
        self.setVisible(True)
        

    def imshow(self, image):
        self.ax.imshow(image, cmap='viridis')
        self.ax.axis('off')
        self.fig.tight_layout(pad=0)
        self.draw()


class Move(QMainWindow):
    def __init__(self, main_app):
        self.main_app = main_app
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle("WATER-SAFE: Microplastic Detection and PFAS Collection")
        self.setGeometry(0, 0, 800, 480)
        self.setStyleSheet("background-color: #00161A;")
        self.i =0
        self.exposure = 8000
        self.gain = 18
        self.initUI()
        self.showFullScreen()
    def setExposureandGain(self,exposure,gain):
        self.exposure = exposure
        self.gain = gain

    def initUI(self):
        # Sample Image and Matplotlib Histogram
        self.image_viewer = ImageViewerWidget(self)
        self.image_viewer.setVisible(True)
        self.image_viewer.raise_()

        # Top row buttons
        play_button = QPushButton("Done", self)
        info_button = QPushButton("ℹ️", self)
        info_button.setStyleSheet("background: #545B64; border: 2px solid black; border-radius: 24px; color: #F3F9F9;")
        info_button.setGeometry(648, 36, 48, 48)
        help_button = QPushButton("❓", self)
        help_button.setStyleSheet("background: #545B64; border: 2px solid black; border-radius: 24px; color: #F3F9F9;")
        help_button.setGeometry(724, 36, 48, 48)
        play_button.setStyleSheet("background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #01994D, stop: 1 #00DC73); border: 2px solid black; border-radius: 24px; color: #F3F9F9")
        play_button.setGeometry(29, 36, 140, 48)

        # Information text label
        self.text_label = QLabel(f"<center>Adjust both knobs to 0 <br> Click Done to continue")
        self.text_label.setGeometry(368, 373, 403, 78)
        self.text_label.setParent(self)
        self.text_label.setStyleSheet("background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #E537B3, stop: 1 #DE76DE); border: 2px solid black; border-radius: 24px; color: #F3F9F9")
        self.text_label.show()

        # Save button
    

        # Connect button signals to functions
        play_button.clicked.connect(self.on_run_clicked)
        info_button.clicked.connect(self.on_info_clicked)
        help_button.clicked.connect(self.on_help_clicked)
       

   
      
    def on_run_clicked(self):
        # Call the custom function to create the labeled image and graph
        #self.create_image_and_graph()
        self.i += 1
        if self.i == 1:
            run_single_camera('1.jpg',self.exposure,self.gain)
            self.text_label.setText(f"<center>Adjust the bottom knob to 4.38mm <br> Click Done to continue")
        if self.i ==2:
            run_single_camera('2.jpg',self.exposure,self.gain)
            self.text_label.setText(f"<center>Adjust the bottom knob to 8.76mm <br> Click Done to continue")
        if self.i ==3:
            run_single_camera('3.jpg',self.exposure,self.gain)
            self.text_label.setText(f"<center>Adjust the right knob to 6.57mm <br> Click Done to continue")
        if self.i == 4:
            run_single_camera('4.jpg',self.exposure,self.gain)
            self.text_label.setText(f"<center>Adjust the bottom knob to 4.38mm <br> Click Done to continue")
        if self.i == 5:
            run_single_camera('5.jpg',self.exposure,self.gain)
            self.text_label.setText(f"<center>Adjust the bottom knob to 0mm <br> Click Done to continue")
        if self.i == 6:
            self.i =0
            self.text_label.setText(f"<center>Adjust both knobs to 0 <br> Click Done to continue")
            self.main_app.showFullScreen()
            run_single_camera('6.jpg',self.exposure,self.gain)
            self.main_app.create_image_and_graph()
            self.hide()
        


    def on_info_clicked(self):
        print("Info button clicked")

    def on_help_clicked(self):
        print("Help button clicked")

    
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = Move()
    sys.exit(app.exec_())
