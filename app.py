from picamera import PiCamera
import http.client
import json
import urllib
import time
import settings

headers = {
    # Request headers
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': settings.KEY,
}

write_file_name = './tmp.jpg'
camera = PiCamera()
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

    con = http.client.HTTPSConnection(settings.API)
    con.request('POST', '/face/v1.0/detect?%s' % params, img, headers)
    response = con.getresponse()
    data = json.loads(response.read())
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

    con.close()
    time.sleep(5)
