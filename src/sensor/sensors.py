from measurement import *
import numpy as np

class Camera(Sensor):
    def __init__(self, device_id = 0):
        super().__init__()
        import cv2
        self.cap = cv2.VideoCapture(device_id)
    
    def get_measurement(self):
        ret, frame = self.cap.read()
        return Measurement("camera", frame)

    def release(self):
        self.cap.release()

class WalabotRadar(Sensor):
    def __init__(self):
        super().__init__()
        import WalabotAPI as wlbt
        self.wlbt = wlbt
        self.wlbt.Init()
        self.wlbt.SetSettingsFolder()
        self.wlbt.ConnectAny()
        self.wlbt.SetProfile(self.wlbt.PROF_SENSOR)
        self.wlbt.SetDynamicImageFilter(self.wlbt.FILTER_TYPE_NONE)
        self.wlbt.Start()
    
    def get_measurement(self):
        self.wlbt.Trigger()
        image = self.wlbt.GetRawImage()[0]
        image = np.array(image, dtype=np.float32)
        return Measurement("radar", image)
    
    def release(self):
        self.wlbt.Stop()
        self.wlbt.Disconnect()
        self.wlbt.Clean()

if __name__ == '__main__':
    cam = Camera()
    radar = WalabotRadar()
    cam.start()
    radar.start()

    previous_time_camera = 0
    previous_time_radar = 0

    while True:
        if cam.latest is not None:
            if cam.latest.timestamp != previous_time_camera:
                previous_time_camera = cam.latest.timestamp
                print(cam.latest)
        if radar.latest is not None:
            if radar.latest.timestamp != previous_time_radar:
                previous_time_radar = radar.latest.timestamp
                print(radar.latest)