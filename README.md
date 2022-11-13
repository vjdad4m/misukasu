# MISUKASU

Radar-based pose estimation with additional features

Requires: [walabot](https://walabot.com/), numpy, opencv

## sensor apis

misukasu provides easy-to-use apis for the used sensors.

```python
from misukasu.sensor import SensorCamera
from misukasu.sensor import SensorRadar

camera = SensorCamera()
radar = SensorRadar()

while True:
	camera_latest = camera.get_frame()
	radar_latest = radar.get_frame()

camera.release()
radar.release()
```
