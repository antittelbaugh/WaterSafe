import PySpin
import tkinter as tk
from PIL import Image, ImageTk
import threading

class CameraGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Camera GUI")

        self.camera = None
        self.image_label = tk.Label(master)
        self.image_label.pack()

        self.gain_var = tk.DoubleVar()
        self.exposure_var = tk.DoubleVar()

        self.gain_scale = tk.Scale(master, label="Gain", from_=0, to=20, orient=tk.HORIZONTAL, variable=self.gain_var, command=self.update_gain)
        self.gain_scale.pack()

        self.exposure_scale = tk.Scale(master, label="Exposure (us)", from_=0, to=100000, orient=tk.HORIZONTAL, variable=self.exposure_var, command=self.update_exposure)
        self.exposure_scale.pack()

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

        # Create a separate thread for camera acquisition
        self.acquisition_thread = threading.Thread(target=self.acquire_images)
        self.acquisition_thread.daemon = True
        self.acquisition_thread.start()

    def acquire_images(self):
        while True:
            try:
                # Get the current gain and exposure values
                gain = self.gain_var.get()
                exposure_time = self.exposure_var.get()

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
                    image = Image.fromarray(image_data)
                    photo = ImageTk.PhotoImage(image=image)

                    # Update the image displayed in the GUI
                    self.image_label.config(image=photo)
                    self.image_label.image = photo
                    self.master.update()

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
    root = tk.Tk()
    app = CameraGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
