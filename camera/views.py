from django.shortcuts import render
import numpy as np
import cv2 as cv
from django.http import StreamingHttpResponse
import threading
from django.views.decorators import gzip

# Create your views here.
class VideoCamera(object):

    def __init__(self):
        """
        docstring
        """
        self.camera = cv.VideoCapture(0, cv.CAP_DSHOW)
        (self.grabbed, self.frame) = self.camera.read()
        threading.Thread(target=self.update, args=()).start()
    
    def __del__(self):
        """
        docstring
        """
        self.camera.release()

    def get_frame(self):
        image = self.frame
        _, jpeg = cv.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.camera.read()

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@gzip.gzip_page
def cap0(request):
    camera = VideoCamera()
    return StreamingHttpResponse(gen(camera), content_type="multipart/x-mixed-replace; boundary=frame")

