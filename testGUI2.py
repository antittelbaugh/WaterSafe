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
from CameraViewLayout import CameraViewLayout
from Light import turn_off_led,turn_on_led


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
        self.showFullScreen()

    def initUI(self):

        # Sample Image and Matplotlib Histogram
        self.camera_view_layout = CameraViewLayout(self)
        self.image_viewer = ImageViewerWidget(self)
        self.image_viewer.setVisible(True)
        self.image_viewer.raise_()
        hist_back = QWidget()
        hist_back.setParent(self)
        hist_back.setGeometry(368, 112, 403, 232) 
        hist_back.setVisible(True)
        hist_back.setStyleSheet("background: #2A2E34;border : 2px solid black; border-radius : 24px;color: #F3F9F9;")
        hist_back.show()
        self.histogram_viewer = FigureCanvas(Figure(facecolor="#2A2E34"))
        self.histogram_viewer.setGeometry(378, 122, 383, 212) 
        self.histogram_viewer.setVisible(True)
        self.histogram_viewer.setParent(self)
        image_back = QWidget()
        image_back.setParent(self)
        image_back.setGeometry(29, 112, 310, 339)
        image_back.setVisible(True)
        image_back.setStyleSheet("background: #2A2E34;border : 2px solid black; border-radius : 24px;color: #F3F9F9;")
        image_back.show()
        self.image_viewer.raise_()
        #layout = QHBoxLayout()
        #layout.addWidget(self.image_viewer)
        #self.group_layout = QGroupBox()
        #self.group_layout.setLayout(layout)
        #self.group_layout.setGeometry(29, 112, 310, 339)
        # Set background color and no border for title
        #self.group_layout.setStyleSheet("background: #2A2E34;border : none; border-radius : 24px;")
        # Check visibility of ImageViewerWidget
        
        # Top row buttons
        play_button = QPushButton("Run", self)
        info_button = QPushButton("ℹ️", self)
        info_button.setStyleSheet("background: #545B64;border : 2px solid black; border-radius : 24px; color: #F3F9F9;")
        info_button.setGeometry(648, 36, 48, 48) 
        help_button = QPushButton("❓", self)
        help_button.setStyleSheet("background: #545B64;border : 2px solid black; border-radius : 24px; color: #F3F9F9")
        help_button.setGeometry(724, 36, 48, 48)
        play_button.setStyleSheet("background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #01994D, stop: 1 #00DC73);border : 2px solid black; border-radius : 24px; color: #F3F9F9")
        play_button.setGeometry(29, 36, 140, 48) 
        self.text_label = QLabel('<center>Concentration:   <br>Median Size:    ')
        self.text_label.setGeometry(368,373, 403, 78)
        self.text_label.setParent(self)
        self.text_label.setStyleSheet("background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #E537B3, stop: 1 #DE76DE);border : 2px solid black; border-radius : 24px; color: #F3F9F9")
        self.text_label.show()
        
        #top_button_layout = QHBoxLayout()
        #top_button_layout.addWidget(play_button)
        #top_button_layout.addWidget(info_button)
        #top_button_layout.addWidget(help_button)

        # Bottom row buttons and status area
        save_button = QPushButton("Save", self)
        save_button.setStyleSheet("background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #30333A, stop: 1 #545B64); border : 2px solid black; border-radius : 24px; color: #F3F9F9")
        save_button.setGeometry(199, 36, 140, 48) 
        #status_bar = QStatusBar()

        #bottom_layout = QHBoxLayout()
        #bottom_layout.addWidget(save_button)
        #bottom_layout.addWidget(status_bar)

        # Combine image and histogram in a horizontal layout
        #image_histogram_layout = QHBoxLayout()
        #image_histogram_layout.addWidget(self.image_viewer, 1)  # Set weight to 2 to allocate more space
        #image_histogram_layout.addWidget(self.histogram_viewer, 1)  # Set weight to 1

        # Combine all layouts
        #main_layout = QVBoxLayout()
        #main_layout.addLayout(top_button_layout)
        #main_layout.addLayout(image_histogram_layout)
        #main_layout.addLayout(bottom_layout)

        #central_widget = QWidget()
        #central_widget.setLayout(main_layout)
        #self.setCentralWidget(central_widget)

        # Connect button signals to functions
        play_button.clicked.connect(self.on_run_clicked)
        info_button.clicked.connect(self.on_info_clicked)
        help_button.clicked.connect(self.on_help_clicked)
        save_button.clicked.connect(self.on_save_clicked)

    def create_image_and_graph(self):
        
        # Load image and perform processing
        img = io.imread('combined_image.jpg')
        #img = rgb2gray(img)
        thresh = threshold_otsu(img)
        bw = closing(img > thresh)
        label_image = label(bw)
        labeled_img = label2rgb(label_image, image=img, bg_label=0)

        # Display the labeled image
        self.image_viewer.imshow(labeled_img)

        # Extract region properties and create histogram
        props = regionprops_table(label_image, properties=['label', 'feret_diameter_max'])
        df = pd.DataFrame(props)
        df['feret_diameter_max'] = df['feret_diameter_max'] * 1.2
        concentration = len(df['feret_diameter_max'])
        median = np.median(df['feret_diameter_max'])
        df = df[df['feret_diameter_max'] >= 16.6666]
        self.histogram_viewer.figure.clear()
        ax = self.histogram_viewer.figure.add_subplot(111)
        ax.hist(df['feret_diameter_max'], bins=12, color="#1BDBD6", width = 4)
        ax.set_xlabel('Size (um)')
        ax.set_ylabel('Frequency')
        ax.set_title('Size Distribution          ')
        ax.set_facecolor("#2A2E34")
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.xaxis.label.set_color('#5C6572')
        ax.tick_params(axis='x', colors='#5C6572')
        ax.yaxis.label.set_color('#5C6572')
        ax.tick_params(axis='y', colors='#5C6572')
        ax.title.set_color('#F3F9F9')
        

        
        self.histogram_viewer.figure.tight_layout(pad=0)  # Adjusts subplot params to minimize whitespace

        self.histogram_viewer.draw()
        print("ImageViewerWidget visible:", self.image_viewer.isVisible())

        # Print geometry of ImageViewerWidget
        print("ImageViewerWidget geometry:", self.image_viewer.geometry())

        # Print geometry of QGroupBox (self.group_layout)
        #print("QGroupBox geometry:", self.group_layout.geometry())
        self.text_label.setText(f"<center>Concentration: {concentration} ppl <br>Median Size: {median:.2f}  um")
        turn_off_led()
        

    def on_run_clicked(self):
        # Call the custom function to create the labeled image and graph
        turn_on_led()
        self.camera_view_layout.showFullScreen()
        self.hide()
        #self.create_image_and_graph()

    def on_info_clicked(self):
        print("Info button clicked")

    def on_help_clicked(self):
        print("Help button clicked")

    def on_save_clicked(self):
        print("Save button clicked")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = WaterSafeApp()
    sys.exit(app.exec_())
