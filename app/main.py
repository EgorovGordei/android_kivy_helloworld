import kivy
from kivy.lang import Builder
from kivy.app import App
from kivy.properties import StringProperty
from kivy.clock import mainthread
from kivy.utils import platform
from kivymd.app import MDApp
from kivy.uix.boxlayout import BoxLayout
import time
import os

from plyer import gps
from plyer import camera
import requests

from kivy.graphics.texture import Texture
from kivy.uix.camera import Camera
from kivy.clock import Clock
import numpy as np
import cv2


import imutils


mainkv = """
<CameraClick>:
    orientation: 'vertical'
    Camera:
        id: camera
        resolution: (640, 480)
        play: False
    ToggleButton:
        text: 'Play'
        on_press: camera.play = not camera.play
        size_hint_y: None
        height: '48dp'
    Button:
        text: 'Capture'
        size_hint_y: None
        height: '48dp'
        on_press: root.capture()
    Button:
        id: button_change_image_state
        text: 'Image state: 0'
        on_press: root.change_image_state()
    Image:
        id: image
"""


class CameraClick(BoxLayout):
    image_state = 0
    def capture(self):
        camera = self.ids['camera']
        camtexture = camera.texture

        height, width = camtexture.height, camtexture.width
        frame = np.frombuffer(camtexture.pixels, np.uint8)
        frame = frame.reshape(height, width, 4)

        #"""
        font = cv2.FONT_HERSHEY_SIMPLEX
        org = (50, 50)
        fontScale = 1
        color = (255, 0, 0)
        thickness = 2
        cv2.putText(frame, 'OpenCV', org, font, 
                    fontScale, color, thickness, cv2.LINE_AA)
        if self.image_state % 7 == 0:
            buf = cv2.flip(frame, -1)
            buf = buf.tobytes()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]))
            texture.blit_buffer(buf, colorfmt='rgba')
            self.ids['image'].texture = texture
            return

        greenLower = (29, 86, 6)
        greenUpper = (64, 255, 255)
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, greenLower, greenUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        center = None
        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            if radius > 10:
                cv2.circle(frame, (int(x), int(y)), int(radius),
                           (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)
        #"""
            
        buf = cv2.flip(frame, -1)
        buf = buf.tobytes()
        texture = Texture.create(size=(frame.shape[1], frame.shape[0])) 
        if self.image_state % 7 == 1:
            texture.blit_buffer(buf, colorfmt='rgba')
        if self.image_state % 7 == 2:
            texture.blit_buffer(buf, colorfmt='bgra')
        if self.image_state % 7 == 3:
            texture.blit_buffer(buf, colorfmt='rgb')
        if self.image_state % 7 == 4:
            texture.blit_buffer(buf, colorfmt='bgr')
        if self.image_state % 7 == 5:
            texture.blit_buffer(buf, colorfmt=camtexture.colorfmt)
        if self.image_state % 7 == 6:
            texture = camtexture

        #texture = camtexture
        self.ids['image'].texture = texture

    def change_image_state(self):
        self.image_state += 1
        self.ids["button_change_image_state"].text = 'Image state:' +\
                                                    str(self.image_state % 7)


class TestCamera(MDApp):
    def build(self):
        if platform == "android":
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.CAMERA,
                                 Permission.WRITE_EXTERNAL_STORAGE,
                                 Permission.READ_EXTERNAL_STORAGE])
        Builder.load_string(mainkv)
        return CameraClick()


TestCamera().run()
