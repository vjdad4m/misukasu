import argparse
import time

from misukasu.sensor import SensorCamera, SensorRadar


def test_camera(test_duration):
    cam = SensorCamera()
    n_frames = 0

    start_time = time.time()
    while time.time() - start_time < test_duration:
        frame = cam.get_frame()
        n_frames += 1

    cam.release()
    return n_frames


def test_radar(test_duration):
    radar = SensorRadar()
    n_frames = 0

    start_time = time.time()
    while time.time() - start_time < test_duration:
        frame = radar.get_frame()
        n_frames += 1

    radar.release()
    return n_frames


def print_stats(n_frames, duration):
    print('received', n_frames, 'frames')
    print('test took', duration, 'seconds')
    print('resulting in', n_frames / duration, 'fps')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--duration', type=int, default=10)
    args = parser.parse_args()
    test_duration = args.duration

    print('selected test duration:', test_duration, 'seconds')

    print('- running camera benchmark...')
    frames = test_camera(test_duration)
    print_stats(frames, test_duration)

    print('- running radar benchmark...')
    frames = test_radar(test_duration)
    print_stats(frames, test_duration)
