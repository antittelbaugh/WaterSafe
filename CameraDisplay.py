import PySpin
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QSlider, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QTimer
from PIL import Image, ImageQt
import sys
import threading

class CameraGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Camera GUI")

        self.camera = None
        self.image_label = QLabel()
        self.setCentralWidget(self.image_label)

        self.gain_slider = QSlider(Qt.Horizontal)
        self.gain_slider.setMinimum(0)
        self.gain_slider.setMaximum(20)
        self.gain_slider.valueChanged.connect(self.update_gain)

        self.exposure_slider = QSlider(Qt.Horizontal)
        self.exposure_slider.setMinimum(0)
        self.exposure_slider.setMaximum(100000)
        self.exposure_slider.valueChanged.connect(self.update_exposure)

        layout = QVBoxLayout()
        layout.addWidget(self.gain_slider)
        layout.addWidget(self.exposure_slider)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.initialize_camera()

    def initialize_camera(self):
        system = PySpin.System.GetInstance()
        self.camera_list = system.GetCameras()
        if self.camera_list.GetSize() == 0:
            print("No cameras found.")
            return

        self.camera = self.camera_list.GetByIndex(0)
        self.camera.Init()
        self.camera.BeginAcquisition()

        self.acquisition_thread = threading.Thread(target=self.acquire_images)
        self.acquisition_thread.daemon = True
        self.acquisition_thread.start()

    def acquire_images(self):
        while True:
            try:
                gain = self.gain_slider.value()
                exposure_time = self.exposure_slider.value()

                if self.camera is not None:
                    self.camera.Gain.SetValue(gain)
                    self.camera.ExposureTime.SetValue(exposure_time)

                image_result = self.camera.GetNextImage()
                if image_result.IsIncomplete():
                    print("Image incomplete")
                else:
                    image_data = image_result.GetNDArray()
                    image = Image.fromarray(image_data)
                    qt_image = ImageQt.ImageQt(image)
                    pixmap = QPixmap.fromImage(qt_image)
                    self.image_label.setPixmap(pixmap)

                image_result.Release()

            except PySpin.SpinnakerException:
                print("Camera disconnected or error occurred")
                break

    def update_gain(self, value):
        pass

    def update_exposure(self, value):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = CameraGUI()
    gui.show()
    sys.exit(app.exec_())
