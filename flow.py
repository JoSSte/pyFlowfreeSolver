#!/usr/bin/env python3

# https://github.com/engineer-man/youtube/blob/master/105/stick_hero.py

from ppadb.client import Client as AdbClient

from PIL import Image
import numpy
import time

adb = AdbClient(host='127.0.0.1', port=5037)
devices = adb.devices()

if len(devices) == 0:
    print('no device attached')
    quit()

device = devices[0]

#while True:
image = device.screencap()
with open('screen.png', 'wb') as f:
    f.write(image)
image = Image.open('screen.png')
image = numpy.array(image, dtype=numpy.uint8)