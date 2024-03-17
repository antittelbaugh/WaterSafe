import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QSlider, QHBoxLayout
from PyQt5.QtGui import QImage, QPixmap
import PySpin

global continue_recording
continue_recording = True


def handle_close(evt):
    global continue_recording
    continue_recording = False


def acquire_and_display_images(cam, nodemap, nodemap_tldevice, label, gain_slider, exposure_slider):
    global continue_recording

    sNodemap = cam.GetTLStreamNodeMap()

    node_bufferhandling_mode = PySpin.CEnumerationPtr(sNodemap.GetNode('StreamBufferHandlingMode'))
    if not PySpin.IsAvailable(node_bufferhandling_mode) or not PySpin.IsWritable(node_bufferhandling_mode):
        print('Unable to set stream buffer handling mode.. Aborting...')
        return False

    node_newestonly = node_bufferhandling_mode.GetEntryByName('NewestOnly')
    if not PySpin.IsAvailable(node_newestonly) or not PySpin.IsReadable(node_newestonly):
        print('Unable to set stream buffer handling mode.. Aborting...')
        return False

    node_newestonly_mode = node_newestonly.GetValue()
    node_bufferhandling_mode.SetIntValue(node_newestonly_mode)

    try:
        node_acquisition_mode = PySpin.CEnumerationPtr(nodemap.GetNode('AcquisitionMode'))
        if not PySpin.IsAvailable(node_acquisition_mode) or not PySpin.IsWritable(node_acquisition_mode):
            print('Unable to set acquisition mode to continuous (enum retrieval). Aborting...')
            return False

        node_acquisition_mode_continuous = node_acquisition_mode.GetEntryByName('Continuous')
        if not PySpin.IsAvailable(node_acquisition_mode_continuous) or not PySpin.IsReadable(
                node_acquisition_mode_continuous):
            print('Unable to set acquisition mode to continuous (entry retrieval). Aborting...')
            return False

        acquisition_mode_continuous = node_acquisition_mode_continuous.GetValue()
        node_acquisition_mode.SetIntValue(acquisition_mode_continuous)

        print('Acquisition mode set to continuous...')

        cam.BeginAcquisition()

        print('Acquiring images...')

        while continue_recording:
            try:
                image_result = cam.GetNextImage(1000)

                if image_result.IsIncomplete():
                    print('Image incomplete with image status %d ...' % image_result.GetImageStatus())
                else:
                    image_data = image_result.GetNDArray()

                    height, width = image_data.shape
                    q_img = QImage(image_data.data, width, height, width, QImage.Format_Grayscale8)

                    label.setPixmap(QPixmap.fromImage(q_img))

                image_result.Release()

            except PySpin.SpinnakerException as ex:
                print('Error: %s' % ex)
                return False

        cam.EndAcquisition()

    except PySpin.SpinnakerException as ex:
        print('Error: %s' % ex)
        return False

    return True


def run_single_camera(cam, label, gain_slider, exposure_slider):
    try:
        nodemap_tldevice = cam.GetTLDeviceNodeMap()
        cam.Init()
        nodemap = cam.GetNodeMap()

        result = acquire_and_display_images(cam, nodemap, nodemap_tldevice, label, gain_slider, exposure_slider)

        cam.DeInit()

    except PySpin.SpinnakerException as ex:
        print('Error: %s' % ex)
        result = False

    return result


def main():
    app = QApplication(sys.argv)

    system = PySpin.System.GetInstance()

    cam_list = system.GetCameras()

    num_cameras = cam_list.GetSize()

    print('Number of cameras detected: %d' % num_cameras)

    if num_cameras == 0:
        print('Not enough cameras!')
        input('Done! Press Enter to exit...')
        return False

    for cam in cam_list:
        window = QWidget()
        window.setWindowTitle('Camera Viewer')

        image_label = QLabel()

        gain_slider = QSlider()
        gain_slider.setOrientation(1)  # Vertical orientation
        gain_slider.setMinimum(0)
        gain_slider.setMaximum(100)

        exposure_slider = QSlider()
        exposure_slider.setOrientation(1)  # Vertical orientation
        exposure_slider.setMinimum(0)
        exposure_slider.setMaximum(100)

        layout = QVBoxLayout()
        layout.addWidget(image_label)

        # Add sliders to a horizontal layout
        slider_layout = QHBoxLayout()
        slider_layout.addWidget(gain_slider)
        slider_layout.addWidget(exposure_slider)
        layout.addLayout(slider_layout)

        window.setLayout(layout)
        window.setGeometry(100, 100, 800, 600)
        window.show()

        result = run_single_camera(cam, image_label, gain_slider, exposure_slider)

        if not result:
            print('Failed to run camera example.')

    cam_list.Clear()
    system.ReleaseInstance()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
