import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QSlider, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import PySpin
import numpy as np
import threading

class CameraGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Camera GUI")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.image_label = QLabel()
        self.layout.addWidget(self.image_label)

        self.gain_slider = QSlider(Qt.Horizontal)
        self.gain_slider.setMinimum(0)
        self.gain_slider.setMaximum(20)
        self.gain_slider.valueChanged.connect(self.update_gain)
        self.layout.addWidget(self.gain_slider)

        self.exposure_slider = QSlider(Qt.Horizontal)
        self.exposure_slider.setMinimum(0)
        self.exposure_slider.setMaximum(100000)
        self.exposure_slider.valueChanged.connect(self.update
