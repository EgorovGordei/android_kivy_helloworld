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
        text: 'Change image state'
        on_press: root.change_image_state()
    Image:
        id: image
"""


class CameraClick(BoxLayout):
    image_state = 0
    def capture(self):
        if self.image_state % 2 == 0:
            camera = self.ids['camera']
            timestr = time.strftime("%Y%m%d_%H%M%S")
            camtexture = camera.texture

            height, width = camtexture.height, camtexture.width
            frame = np.frombuffer(camtexture.pixels, np.uint8)
            frame = frame.reshape(height, width, 4)
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tobytes()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr') 
            texture.blit_buffer(buf, colorfmt='bgr')

        if self.image_state % 2 == 1:
            height = 100
            width = 100
            texture = Texture.create(size=(height, width))
            size = height * width * 3
            buf = [int(x * 255 / size) for x in range(size)]
            for i in range(height):
                buf[3*(i*width+i)] = 1000
            buf = ''.join(map(chr, buf)).encode('utf-8')
            texture.blit_buffer(buf, colorfmt='bgr')
        
        self.ids['image'].texture = texture
        """
        height, width = camera.texture.height, camera.texture.width
        newvalue = np.frombuffer(camera.texture.pixels, np.uint8)
        newvalue = newvalue.reshape(height, width, 4)
        gray = cv2.cvtColor(newvalue, cv2.COLOR_RGBA2GRAY)

        buf1 = cv2.flip(gray, 0)
        buf = buf1.tobytes()
        texture1 = Texture.create(size=(gray.shape[1], gray.shape[0]), colorfmt='bgr') 

        #if working on RASPBERRY PI, use colorfmt='rgba' here instead, but stick with "bgr" in blit_buffer. 
        texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.ids['image'].texture = texture1
        """
    def change_image_state(self):
        self.image_state += 1


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
