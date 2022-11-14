import cv2
import numpy as np
import WalabotAPI as wlbt

import misukasu.defaults as defaults


class SensorRadar():
    def __init__(self):
        self.ready = False
        wlbt.Init()
        wlbt.SetSettingsFolder()
        wlbt.ConnectAny()
        wlbt.SetProfile(wlbt.PROF_SENSOR)
        wlbt.SetArenaR(defaults.MIN_R, defaults.MAX_R, defaults.RES_R)
        wlbt.SetArenaTheta(defaults.MIN_T, defaults.MAX_T, defaults.RES_T)
        wlbt.SetArenaPhi(defaults.MIN_P, defaults.MAX_P, defaults.RES_P)
        wlbt.Start()
        self.ready = True
    
    def get_frame(self):
        if self.ready:
            self.ready = False
            wlbt.Trigger()
            frame, sizeX, sizeY, sizeZ, _ = wlbt.GetRawImage()
            frame = np.array(frame).astype(np.uint8)
            self.ready = True
            return (frame, sizeX, sizeY, sizeZ)

    def release(self):
        wlbt.Stop()
        wlbt.Disconnect()
        wlbt.Clean()

class SensorCamera():
    def __init__(self, device_id = defaults.DEVICE_ID):
        self.ready = False
        self.capture = cv2.VideoCapture(device_id)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, defaults.FRAME_WIDTH)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, defaults.FRAME_HEIGHT)
        self.capture.set(cv2.CAP_PROP_FPS, 30)
        self.ready = True

    def get_frame(self):
        if self.ready:
            self.ready = False
            ret, frame = self.capture.read()
            if ret:
                frame = np.array(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)).astype(np.uint8)
                self.ready = True
                return frame
            self.ready = True

    def release(self):
        self.capture.release()
