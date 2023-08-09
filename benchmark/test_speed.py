import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../src/'))

import time

from sensors import Camera, WalabotRadar

def test_sensor(sensor, n_measurements = 100):
    count = 0
    sensor.start()
    start_time = time.time()
    previous_time = 0
    while count < n_measurements:
        if sensor.latest is not None:
            if sensor.latest.timestamp != previous_time:
                previous_time = sensor.latest.timestamp
                count += 1
    
    end_time = time.time()
    sensor.stop()
    print("Time elapsed: {} seconds".format(end_time - start_time))

if __name__ == '__main__':
    for k in [10, 100, 500, 1000]:
        print('k = {}'.format(k))
        cam = Camera()
        radar = WalabotRadar()
        time.sleep(2)
        print('Testing camera')
        test_sensor(cam, k)
        print('Testing radar')
        test_sensor(radar, k)