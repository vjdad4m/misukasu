# camera config
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
DEVICE_ID = 0

# radar config
MIN_T = -45
MAX_T = 45
RES_T = 2
MIN_P = -45
MAX_P = 45
RES_P = 2
MIN_R = 10
MAX_R = 400
RES_R = 10

# measurement config
MAX_MATCH_DISTANCE = 0.06 # 60ms

# global settings
DEBUG = True

def debug_print(s):
    if DEBUG: print('[DEBUG]', s) 