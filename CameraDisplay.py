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
        self.exposure_slider.valueChanged.connect(self.update_exposure)
        self.layout.addWidget(self.exposure_slider)

        self.camera = None

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

        # Turn off auto gain
        self.camera.GainAuto.SetValue(PySpin.GainAuto_Off)

        # Turn off auto exposure
        self.camera.ExposureAuto.SetValue(PySpin.ExposureAuto_Off)

        # Create a separate thread for camera acquisition
        self.acquisition_thread = threading.Thread(target=self.acquire_images)
        self.acquisition_thread.daemon = True
        self.acquisition_thread.start()

    def acquire_images(self):
        while True:
            try:
                # Get the current gain and exposure values
                gain = self.gain_slider.value()
                exposure_time = self.exposure_slider.value()

                # Set the camera gain and exposure
                if self.camera is not None:
                    self.camera.Gain.SetValue(gain)
                    self.camera.ExposureTime.SetValue(exposure_time)

                # Capture an image
                image_result = self.camera.GetNextImage()
                if image_result.IsIncomplete():
                    print("Image incomplete")
                else:
                    # Convert the image to a format suitable for display
                    image_data = image_result.GetNDArray()
                    image = QPixmap.fromImage(QImage(image_data, image_data.shape[1], image_data.shape[0], QImage.Format_RGB888))
                    self.image_label.setPixmap(image)
                    self.image_label.adjustSize()

                # Release the image
                image_result.Release()

            except PySpin.SpinnakerException as ex:
                print('Error: %s' % ex)
                break

    def update_gain(self, value):
        pass  # Gain is updated directly within acquire_images()

    def update_exposure(self, value):
        pass  # Exposure time is updated directly within acquire_images()

def main():
    app = QApplication(sys.argv)
    gui = CameraGUI()
    gui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
