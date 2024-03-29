import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QGraphicsView, QGraphicsScene, QStatusBar
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen, QColor
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class WaterSafeApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("WATER-SAFE: Microplastic Detection and PFAS Collection")
        self.setGeometry(100, 100, 800, 600)

        self.initUI()

    def initUI(self):
        # Top row buttons
        play_button = QPushButton("Run ▶️")
        info_button = QPushButton("Info ℹ️")
        help_button = QPushButton("Help ❓")

        top_button_layout = QHBoxLayout()
        top_button_layout.addWidget(play_button)
        top_button_layout.addWidget(info_button)
        top_button_layout.addWidget(help_button)

        # Image display and Histogram
        image_display = QLabel("Image Display Area")
        presence_label = QLabel("Presence:")
        concentration_label = QLabel("Concentration:")
        histogram_label = QLabel("Size Distribution Histogram")

        image_layout = QVBoxLayout()
        image_layout.addWidget(image_display)
        image_layout.addWidget(presence_label)
        image_layout.addWidget(concentration_label)

        histogram_layout = QVBoxLayout()
        histogram_layout.addWidget(histogram_label)

        image_histogram_layout = QHBoxLayout()
        image_histogram_layout.addLayout(image_layout, 1)
        image_histogram_layout.addLayout(histogram_layout, 1)

        # Bottom row buttons and status area
        save_button = QPushButton("Save Data 💾")
        status_bar = QStatusBar()

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(save_button)
        bottom_layout.addWidget(status_bar)

        # Sample Image
        self.sample_image_path = "MP_PA_1.jpg"  # Replace with the path to your sample image
        self.sample_image_label = QLabel()
        self.sample_image_label.setVisible(False)  # Initially set to invisible

        # Matplotlib Histogram
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
        image_histogram_layout.addWidget(self.sample_image_label)
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
        # Your custom function to create the image and graph
        pixmap = QPixmap(self.sample_image_path)
        self.sample_image_label.setPixmap(pixmap)

        # Set the Matplotlib figure size to match the image size
        fig_width = pixmap.width() / 100
        fig_height = pixmap.height() / 100
        self.canvas.figure.set_size_inches(fig_width, fig_height)

        self.ax.clear()  # Clear previous data in the graph
        x = np.random.randn(1000)
        self.ax.hist(x, bins=30, color='blue', alpha=0.7)
        self.canvas.draw()  # Redraw the canvas
    def on_run_clicked(self):
        # Call the custom function to create the image and graph
        self.create_image_and_graph()

        # Show the image and graph
        self.sample_image_label.setVisible(True)
        self.canvas.setVisible(True)

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