import picamera
import json
import settings
import asyncio
import io
import glob
import os
import sys
import time
import uuid
import requests
import urllib.parse


headers = {
    # Request headers
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': settings.KEY,
}

write_file_name = './tmp.jpg'
camera = picamera.PiCamera()
camera.resolution = (800, 600)

params = urllib.parse.urlencode({
    'returnFaceId': 'false',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'emotion',
})

while True:
    camera.capture(write_file_name)
    with open(write_file_name, 'rb') as f:
        img = f.read()
    print(settings.API)
    con = requests.request("POST", settings.API, headers=headers, params=params, data=img)
    data = json.loads(con.text)
    for i in data:
        anger = i["faceAttributes"]["emotion"]["anger"]
        happiness = i["faceAttributes"]["emotion"]["happiness"]
        neutral = i["faceAttributes"]["emotion"]["neutral"]
        sadness = i["faceAttributes"]["emotion"]["sadness"]
        suprise = i["faceAttributes"]["emotion"]["surprise"]
        print("anger:{0}".format(anger))
        print("happiness:{0}".format(happiness))
        print("neutral:{0}".format(neutral))
        print("sadness:{0}".format(sadness))
        print("surprise:{0}".format(suprise))

    time.sleep(5)
