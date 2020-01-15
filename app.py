import time
import json
import picamera
import RPi.GPIO as GPIO
import requests
import urllib.parse
import settings


headers = {
    # Request headers
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': settings.KEY,
}
params = urllib.parse.urlencode({
    'returnFaceId': 'false',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'emotion',
})
camera = picamera.PiCamera()
DISPLAY_URL = "http://f1ee1c4a.ngrok.io/api/v1/face"
FILE_NAME = './tmp.jpg'
BUTTON_PIN = 14


def main():
    camera.resolution = (800, 600)
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(BUTTON_PIN, GPIO.RISING, callback=callback, bouncetime=300)
    try:
        while(True):
            time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()


def callback(channel):
    camera.capture(FILE_NAME)
    with open(FILE_NAME, 'rb') as f:
        img = f.read()
    print(settings.API)
    con = requests.request("POST", settings.API, headers=headers, params=params, data=img)
    data = json.loads(con.text)
    emotions = []
    for i in data:
        anger = i["faceAttributes"]["emotion"]["anger"]
        happiness = i["faceAttributes"]["emotion"]["happiness"]
        neutral = i["faceAttributes"]["emotion"]["neutral"]
        sadness = i["faceAttributes"]["emotion"]["sadness"]
        suprise = i["faceAttributes"]["emotion"]["surprise"]
        emotions.extend([anger, happiness, neutral, sadness, suprise])
        # print("anger:{0}".format(anger))
        # print("happiness:{0}".format(happiness))
        # print("neutral:{0}".format(neutral))
        # print("sadness:{0}".format(sadness))
        # print("surprise:{0}".format(suprise))
        print(max(emotions))


if __name__ == "__main__":
    main()
