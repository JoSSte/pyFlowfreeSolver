#!/usr/bin/env python3
from ppadb.client import Client as AdbClient

# https://android.stackexchange.com/questions/221204/how-to-install-xapk-apks-or-multiple-apks-via-adb

# todo:
# fetch xapk from https://apkpure.com/flow-free/com.bigduckgames.flow
# unzip
# install

#apk_path = "com.bigduckgames.flow.apk"
#apk_path = "config.arm64_v8a.apk"
apk_path = "config.en.apk"

# Default is "127.0.0.1" and 5037
client = AdbClient(host="127.0.0.1", port=5037)
devices = client.devices()

for device in devices:
    device.install(apk_path)

# Check apk is installed
for device in devices:
    print(device.is_installed("com.bigduckgames.flow"))
    #print(device.shell("pm list packages -f"))    