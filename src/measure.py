import os
import time
import threading
import queue

from sensors import Camera, WalabotRadar

def data_save_thread(queue, file_location):
    while True:
        measurement = queue.get()
        if measurement is None:
            pass
        elif measurement == 'STOP':
            break
        else:
            measurement.save(file_location)
            print('Saved:', measurement)

def run_measurement(save_location):
    cam = Camera()
    radar = WalabotRadar()
    
    cam.start()
    radar.start()
    
    data_queue = queue.Queue()
    save_thread = threading.Thread(target=data_save_thread, args=(data_queue, save_location))
    save_thread.start()
    
    time.sleep(1)
    
    previous_time_camera = 0
    previous_time_radar = 0

    try:
        while True:
            if cam.latest is not None:
                if cam.latest.timestamp != previous_time_camera:
                    previous_time_camera = cam.latest.timestamp
                    data_queue.put(cam.latest)
            if radar.latest is not None:
                if radar.latest.timestamp != previous_time_radar:
                    previous_time_radar = radar.latest.timestamp
                    data_queue.put(radar.latest)
    except KeyboardInterrupt:
        data_queue.put('STOP')
        save_thread.join()

if __name__ == '__main__':
    data_folder = os.path.join(os.path.dirname(__file__), '../data/')
    os.makedirs(data_folder, exist_ok=True)
    run_measurement(data_folder)