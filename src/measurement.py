import os
import time
from threading import Thread

import numpy as np


class Measurement:
    def __init__(self, _type, _data):
        self.type = _type
        self.data = _data
        self.timestamp = time.time()
    
    def save(self, file_location):
        if self.data is None:
            return None
        file_path = os.path.join(file_location, f"{self.type}_{self.timestamp}")
        if isinstance(self.data, np.ndarray):
            np.save(file_path, self.data)
        else:
            with open(file_path + '.txt', "w") as f:
                f.write(str(self.data))

    def __str__(self):
        if self.data is None:
            return f"{self.type}: None <{self.timestamp}>"
        elif isinstance(self.data, np.ndarray):
           return f"{self.type}: {self.data.shape} <{self.timestamp}>"
        else:
            return f"{self.type}: {self.data} <{self.timestamp}>"
    
    def __repr__(self):
        return self.__str__()

class Sensor(object):
    def __init__(self):
        self.latest = None
        self.is_running = True

    def get_measurement(self):
        raise NotImplementedError
    
    def release(self):
        raise NotImplementedError
    
    def start(self):
        self.thread = Thread(target=self._run)
        self.thread.daemon = True
        self.thread.start()

    def _run(self):
        while self.is_running:
            self.latest = self.get_measurement()
        
    def stop(self):
        self.is_running = False
        self.thread.join()
        time.sleep(1)
        self.release()