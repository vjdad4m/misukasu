import time
from threading import Thread

import cv2
import numpy as np

import misukasu.defaults as defaults
from misukasu.sensor import SensorCamera, SensorRadar


class Measurement():
    def __init__(self, mtype, data):
        self.mtype = mtype
        self.data = np.array(data)
        self.time = round(time.time(), 4)
    
    def __repr__(self):
        return f'Measurement <{self.mtype}> @ {self.time}\n{self.data}'
    
    def save(self, folder='./out'):
        if self.data is not None:
            location = '/'.join([folder, self.mtype, str(self.time).replace('.', '_')])
            np.save(location + '.npy', self.data)

class Measurer():
    def __init__(self):
        self.camera = SensorCamera()
        self.radar = SensorRadar()
        self.latest_camera = Measurement(None, None)
        self.latest_radar = Measurement(None, None)
    
    def measure_camera(self):
        while True:
            self.latest_camera = Measurement('camera', self.camera.get_frame())
    
    def measure_radar(self):
        while True:
            self.latest_radar = Measurement('radar', self.radar.get_frame())
    
    def run_camera_thread(self):
        thread_camera = Thread(target = self.measure_camera)
        thread_camera.daemon = True
        defaults.debug_print('starting camera thread')
        thread_camera.start()
    
    def run_radar_thread(self):
        thread_radar = Thread(target = self.measure_radar)
        thread_radar.daemon = True
        defaults.debug_print('starting radar thread')
        thread_radar.start()
    
    def run(self):
        self.run_camera_thread()
        self.run_radar_thread()

def measure():
    mes = Measurer()
    defaults.debug_print('starting measure')
    mes.run()

    n_samples = 0

    while mes.latest_camera.data == None or mes.latest_radar.data == None:
        time.sleep(0.01)

    t_start = time.time()
    while True:
        lcamera = mes.latest_camera
        lradar = mes.latest_radar

        if abs(lcamera - lradar) < defaults.MAX_MATCH_DISTANCE:
            lcamera.save()
            lradar.save()
            n_samples += 1

        cv2.imshow('misukasu - camera', lcamera.data)
        cv2.imshow('misukasu - radar', lradar.data)

        if cv2.waitKey(1) in [ord('q'), 27]:
            cv2.destroyAllWindows()
            break

    t_end = time.time()

    print(f'Finished measurement, captured {n_samples} samples, took {t_end - t_start} seconds.')

if __name__ == '__main__':
    measure()