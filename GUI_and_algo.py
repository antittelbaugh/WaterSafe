import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QStatusBar
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from skimage.filters import threshold_mean
from skimage import io
from skimage.color import rgb2gray, label2rgb
from skimage.measure import label, regionprops_table
from skimage.morphology import closing
import pandas as pd

class WaterSafeApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("WATER-SAFE: Microplastic Detection and PFAS Collection")
        self.setGeometry(100, 100, 800, 600)

        self.initUI()

    def initUI(self):

        # Sample Image and Matplotlib Histogram
        self.image = FigureCanvas(Figure())
        self.image_ax = self.image.figure.add_subplot(111)
        self.image.setVisible(False)  # Initially set to invisible

        self.canvas = FigureCanvas(Figure())
        self.ax = self.canvas.figure.add_subplot(111)
        self.canvas.setVisible(False)  # Initially set to invisible

        # Top row buttons
        play_button = QPushButton("Run ▶️")
        info_button = QPushButton("Info ℹ️")
        help_button = QPushButton("Help ❓")

        top_button_layout = QHBoxLayout()
        top_button_layout.addWidget(play_button)
        top_button_layout.addWidget(info_button)
        top_button_layout.addWidget(help_button)

        # Image and Histogram Layout
        image_histogram_layout = QHBoxLayout()
        image_histogram_layout.addWidget(self.image)
        image_histogram_layout.addWidget(self.canvas)

        # Bottom row buttons and status area
        save_button = QPushButton("Save Data 💾")
        status_bar = QStatusBar()

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(save_button)
        bottom_layout.addWidget(status_bar)

        # Combine all layouts
        main_layout = QVBoxLayout()
        main_layout.addLayout(top_button_layout)
        main_layout.addLayout(image_histogram_layout)
        main_layout.addLayout(bottom_layout)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Connect button signals to functions
        play_button.clicked.connect(self.on_run_clicked)
        info_button.clicked.connect(self.on_info_clicked)
        help_button.clicked.connect(self.on_help_clicked)
        save_button.clicked.connect(self.on_save_clicked)

    def create_image_and_graph(self):
        # Load image and perform processing
        img = io.imread('MP_PA_1.jpg')
        img = rgb2gray(img)
        thresh = threshold_mean(img)
        bw = closing(img > thresh)
        label_image = label(bw)
        labeled_img = label2rgb(label_image, image=img, bg_label=0)
        self.image.imshow(labeled_img)
       

        # Set the Matplotlib figure size to match the image size
        fig_width = labeled_img.shape[1] / 100
        fig_height = labeled_img.shape[0] / 100
        self.canvas.figure.set_size_inches(fig_width, fig_height)

        # Extract region properties and create histogram
        props = regionprops_table(label_image, properties=['label', 'feret_diameter_max'])
        df = pd.DataFrame(props)
        df['feret_diameter_max'] = df['feret_diameter_max'] * 0.58
        df = df[df['feret_diameter_max'] >= 17.24]
        self.ax.hist( df['feret_diameter_max'],bins=10, edgecolor='black')

        self.ax.set_xlabel('Size (um)')
        self.ax.set_ylabel('Frequency')
        self.ax.set_title('Size Distribution')
        self.canvas.draw()  # Redraw the canvas

        # Show the labeled image and graph
        #self.sample_image_label.setVisible(True)
        self.canvas.setVisible(True)

    def array_to_qimage(self, array):
        height, width, channel = array.shape
        bytes_per_line = 3 * width
        qimage = QImage(array.data, width, height, bytes_per_line, QImage.Format_RGB888)
        return qimage

    def qimage_to_pixmap(self, qimage):
        return QPixmap.fromImage(qimage)

    def on_run_clicked(self):
        # Call the custom function to create the labeled image and graph
        self.create_image_and_graph()

    def on_info_clicked(self):
        print("Info button clicked")

    def on_help_clicked(self):
        print("Help button clicked")

    def on_save_clicked(self):
        print("Save button clicked")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = WaterSafeApp()
    mainWin.show()
    sys.exit(app.exec_())
