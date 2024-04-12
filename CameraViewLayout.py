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
from Move import Move


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


class CameraViewLayout(QMainWindow):
    def __init__(self, main_app):
        self.main_app = main_app
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle("WATER-SAFE: Microplastic Detection and PFAS Collection")
        self.setGeometry(0, 0, 800, 480)
        self.setStyleSheet("background-color: #00161A;")
        self.initUI()
        self.showFullScreen()

    def initUI(self):
        # Sample Image and Matplotlib Histogram
        self.mover = Move(self.main_app)
        self.image_viewer = ImageViewerWidget(self)
        self.image_viewer.setVisible(True)
        self.image_viewer.raise_()

        # Create gain and exposure time sliders
        self.create_sliders()

        # Top row buttons
        play_button = QPushButton("OK", self)
        info_button = QPushButton("ℹ️", self)
        info_button.setStyleSheet("background: #545B64; border: 2px solid black; border-radius: 24px; color: #F3F9F9;")
        info_button.setGeometry(648, 36, 48, 48)
        help_button = QPushButton("❓", self)
        help_button.setStyleSheet("background: #545B64; border: 2px solid black; border-radius: 24px; color: #F3F9F9;")
        help_button.setGeometry(724, 36, 48, 48)
        play_button.setStyleSheet("background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #01994D, stop: 1 #00DC73); border: 2px solid black; border-radius: 24px; color: #F3F9F9")
        play_button.setGeometry(29, 36, 140, 48)

        # Information text label
        self.text_label = QLabel(f"<center> Adjust Gain and exposure to desired and tap Apply <br> Click OK to continue")
        self.text_label.setGeometry(368, 373, 403, 78)
        self.text_label.setParent(self)
        self.text_label.setStyleSheet("background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #E537B3, stop: 1 #DE76DE); border: 2px solid black; border-radius: 24px; color: #F3F9F9")
        self.text_label.show()

        # Save button
        save_button = QPushButton("Apply", self)
        save_button.setStyleSheet("background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #30333A, stop: 1 #545B64); border: 2px solid black; border-radius: 24px; color: #F3F9F9")
        save_button.setGeometry(199, 36, 140, 48)

        # Connect button signals to functions
        play_button.clicked.connect(self.on_run_clicked)
        info_button.clicked.connect(self.on_info_clicked)
        help_button.clicked.connect(self.on_help_clicked)
        save_button.clicked.connect(self.on_save_clicked)

    def create_sliders(self):
        # Create a group box for sliders (with no label)
        slider_group = QGroupBox(self)
        slider_group.setStyleSheet("background: #2A2E34; border: 2px solid black; border-radius: 24px; color: #F3F9F9")
        slider_group.setGeometry(368, 112, 403, 232)

        # Create layout for sliders
        slider_layout = QVBoxLayout()

        # Gain slider
        gain_slider = QSlider(Qt.Horizontal)
        gain_slider.setRange(0, 100)
        gain_slider.setValue(50)
        gain_slider.valueChanged.connect(self.on_gain_changed)
        gain_label = QLabel(f"Gain: {gain_slider.value()}")
        gain_label.setAlignment(Qt.AlignCenter)
        gain_label.setStyleSheet("background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #E537B3, stop: 1 #DE76DE); border: 2px solid black; border-radius: 24px; color: #F3F9F9")

        # Exposure time slider
        exposure_slider = QSlider(Qt.Horizontal)
        exposure_slider.setRange(0, 100)
        exposure_slider.setValue(50)
        exposure_slider.valueChanged.connect(self.on_exposure_changed)
        exposure_label = QLabel(f"Exposure Time: {exposure_slider.value()}")
        exposure_label.setAlignment(Qt.AlignCenter)
        exposure_label.setStyleSheet("background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #E537B3, stop: 1 #DE76DE); border: 2px solid black; border-radius: 24px; color: #F3F9F9")

        # Add sliders and labels to layout
        slider_layout.addWidget(gain_label)
        slider_layout.addWidget(gain_slider)
        slider_layout.addWidget(exposure_label)
        slider_layout.addWidget(exposure_slider)

        # Set layout for the group box
        slider_group.setLayout(slider_layout)

        # Store sliders and labels as instance variables
        self.gain_slider = gain_slider
        self.gain_label = gain_label
        self.exposure_slider = exposure_slider
        self.exposure_label = exposure_label
        img = io.imread('PET_b_n_1.jpeg')
        #img = rgb2gray(img)
        #thresh = threshold_otsu(img)
        #bw = closing(img > thresh)
        #label_image = label(bw)
        #labeled_img = label2rgb(label_image, image=img, bg_label=0)

        # Display the labeled image
        self.image_viewer.imshow(img)

    #def create_image_and_graph(self):
        # Load image and perform processing
        
        
        # Extract region properties
        
        # Update information label
        

    def on_run_clicked(self):
        # Call the custom function to create the labeled image and graph
        #self.create_image_and_graph()
        img = io.imread('PET_b_n_1.jpeg')
        #img = rgb2gray(img)
        #thresh = threshold_otsu(img)
        #bw = closing(img > thresh)
        #label_image = label(bw)
        #labeled_img = label2rgb(label_image, image=img, bg_label=0)

        # Display the labeled image
        self.image_viewer.imshow(img)
        self.hide()
        self.mover.showFullScreen()


    def on_info_clicked(self):
        print("Info button clicked")

    def on_help_clicked(self):
        print("Help button clicked")

    def on_save_clicked(self):
        img = io.imread('PET_g_n_1.jpeg')
        self.image_viewer.imshow(img)

    def on_gain_changed(self, value):
        self.gain_label.setText(f"Gain: {value}")

    def on_exposure_changed(self, value):
        self.exposure_label.setText(f"Exposure Time: {value}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = CameraViewLayout()
    sys.exit(app.exec_())