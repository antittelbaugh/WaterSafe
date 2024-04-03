import os
import PySpin
import matplotlib.pyplot as plt
import sys
import keyboard
import time

import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QStatusBar, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPainterPath, QBrush, QColor
from PyQt5.QtCore import QRectF
from PyQt5 import QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from skimage.filters import threshold_otsu
from skimage import io
from skimage.color import rgb2gray, label2rgb
from skimage.measure import label, regionprops_table
from skimage.morphology import closing
from PyQt5.QtWidgets import QGroupBox
import pandas as pd

class ImageViewerWidget(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor="#2A2E34")
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.setParent(parent)
        self.setGeometry(39, 122, 290, 319)
        self.ax.axis('off')
        self.border_radius = 20
        self.background_painted = False  # Flag to track if background has been painted
        self.setVisible(True)



    def imshow(self, image):
        self.ax.clear()
        self.ax.imshow(image, cmap='viridis')
        self.ax.axis('off')
        self.fig.tight_layout(pad=0)
        self.draw()
class WaterSafeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle("WATER-SAFE: Microplastic Detection and PFAS Collection")
        self.setGeometry(0, 0, 800, 480)
        self.setStyleSheet("background-color: #00161A;")
        self.initUI()
        self.show()
        cam =setup()
        while(True):
            getimage(cam)
    def initUI(self):
        self.image_viewer = ImageViewerWidget(self)
        self.image_viewer.setVisible(True)
        self.image_viewer.raise_()
        image_back = QWidget()
        image_back.setParent(self)
        image_back.setGeometry(29, 112, 310, 339)
        image_back.setVisible(True)
        image_back.setStyleSheet("background: #2A2E34;border : 2px solid black; border-radius : 24px;color: #F3F9F9;")
        image_back.show()
        self.image_viewer.raise_()
        
def setup():
    system =PySpin.System.GetInstance()
    cam_list= system.GetCameras()
    for i, cam in enumerate(cam_list):
        cam = cam
    nodemap_tldevice = cam.GetTLDeviceNodeMap()
    cam.Init()
    #nodemap = cam.GetNodeMap()
    sNodemap = cam.GetTLStreamNodeMap()
    # Change bufferhandling mode to NewestOnly
    node_bufferhandling_mode = PySpin.CEnumerationPtr(sNodemap.GetNode('StreamBufferHandlingMode'))
    if not PySpin.IsReadable(node_bufferhandling_mode) or not PySpin.IsWritable(node_bufferhandling_mode):
        print('Unable to set stream buffer handling mode.. Aborting...')
        return False

    # Retrieve entry node from enumeration node
    node_newestonly = node_bufferhandling_mode.GetEntryByName('NewestOnly')
    if not PySpin.IsReadable(node_newestonly):
        print('Unable to set stream buffer handling mode.. Aborting...')
        return False

    # Retrieve integer value from entry node
    #node_newestonly_mode = node_newestonly.GetValue()
    cam.BeginAcquisition()
    device_serial_number = ''
    node_device_serial_number = PySpin.CStringPtr(nodemap_tldevice.GetNode('DeviceSerialNumber'))
    if PySpin.IsReadable(node_device_serial_number):
        device_serial_number = node_device_serial_number.GetValue()
        print('Device serial number retrieved as %s...' % device_serial_number)
    return cam


def getimage(self,cam):
    img =cam.GetNextImage(1000)
    self.image_viewer.imshow(img)
    img.Release()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = WaterSafeApp()
    sys.exit(app.exec_())

