import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QSlider, QGroupBox, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from skimage.filters import threshold_otsu
from skimage import io
from skimage.color import rgb2gray, label2rgb
from skimage.measure import label, regionprops_table
from skimage.morphology import closing
import pandas as pd

class ImageViewerWidget(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor="#2A2E34")
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.setParent(parent)
        self.ax.axis('off')
        self.setGeometry(39, 122, 290, 319)

    def imshow(self, image):
        self.ax.imshow(image, cmap='viridis')
        self.ax.axis('off')
        self.fig.tight_layout(pad=0)
        self.draw()

class WaterSafeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WATER-SAFE: Microplastic Detection and PFAS Collection")
        self.setGeometry(0, 0, 800, 480)
        self.setStyleSheet("background-color: #00161A;")
        self.initUI()
        self.show()

    def initUI(self):
        # Initialize UI components
        self.image_viewer = ImageViewerWidget(self)
        self.histogram_viewer = FigureCanvas(Figure(facecolor="#2A2E34"))
        self.histogram_viewer.setGeometry(378, 122, 383, 212)
        self.text_label = QLabel(self)
        self.text_label.setGeometry(368, 373, 403, 78)
        self.text_label.setStyleSheet("background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #E537B3, stop: 1 #DE76DE); border: 2px solid black; border-radius: 24px; color: #F3F9F9")
        self.text_label.show()

        # Buttons
        self.play_button = QPushButton("Run", self)
        self.play_button.setGeometry(29, 36, 140, 48)
        self.play_button.setStyleSheet("background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #01994D, stop: 1 #00DC73); border: 2px solid black; border-radius: 24px; color: #F3F9F9")
        self.play_button.clicked.connect(self.on_run_clicked)

    def create_image_and_graph(self):
        # Load image and perform processing
        img = io.imread('composite_image.jpg')
        img = rgb2gray(img)
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
        
        # Update text label
        self.text_label.setText(f"<center>Concentration: {concentration} ppl <br>Median Size: {median:.2f} um</center>")

        # Update histogram
        ax = self.histogram_viewer.figure.add_subplot(111)
        ax.hist(df['feret_diameter_max'], bins=12, color="#1BDBD6", width=4)
        ax.set_xlabel('Size (um)')
        ax.set_ylabel('Frequency')
        ax.set_title('Size Distribution')
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
        
        self.histogram_viewer.figure.tight_layout(pad=0)
        self.histogram_viewer.draw()

    def on_run_clicked(self):
        # Open the CameraViewLayout window
        self.camera_view_layout = CameraViewLayout(self)
        self.camera_view_layout.show()

class CameraViewLayout(QMainWindow):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.setWindowTitle("WATER-SAFE: Microplastic Detection and PFAS Collection")
        self.setGeometry(0, 0, 800, 480)
        self.setStyleSheet("background-color: #00161A;")
        self.initUI()
        self.show()

    def initUI(self):
        # Initialize UI components
        self.image_viewer = ImageViewerWidget(self)
        self.image_viewer.setVisible(True)
        self.image_viewer.raise_()

        # Buttons
        self.ok_button = QPushButton("OK", self)
        self.ok_button.setGeometry(29, 36, 140, 48)
        self.ok_button.setStyleSheet("background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #01994D, stop: 1 #00DC73); border: 2px solid black; border-radius: 24px; color: #F3F9F9")
        self.ok_button.clicked.connect(self.on_ok_clicked)

        self.text_label = QLabel(self)
        self.text_label.setGeometry(368, 373, 403, 78)
        self.text_label.setText("<center>Adjust Gain and exposure to desired and tap Apply <br>Click OK to continue</center>")
        self.text_label.setStyleSheet("background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #E537B3, stop: 1 #DE76DE); border: 2px solid black; border-radius: 24px; color: #F3F9F9")
        self.text_label.show()

    def on_ok_clicked(self):
        # Close the CameraViewLayout window
        self.close()
        # Call the create_image_and_graph method in WaterSafeApp
        self.main_app.create_image_and_graph()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = WaterSafeApp()
    sys.exit(app.exec_())
