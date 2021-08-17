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
        id: button_change_code_state
        text: 'Change code state'
        on_press: root.change_code_state()
    Image:
        id: image
"""


class CameraClick(BoxLayout):
    code_state = 0
    def capture(self):
        if self.code_state % 2 == 0:
            camera = self.ids['camera']
            camtexture = camera.texture

            height, width = camtexture.height, camtexture.width
            frame = np.frombuffer(camtexture.pixels, np.uint8)
            frame = frame.reshape(height, width, 4)
            buf = cv2.flip(frame, -1)
            buf = buf.tobytes()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0])) 
            if (self.code_state / 2) % 6 == 0:
                texture.blit_buffer(buf, colorfmt='rgb')
            if (self.code_state / 2) % 6 == 1:
                texture.blit_buffer(buf, colorfmt='bgr')
            if (self.code_state / 2) % 6 == 2:
                texture.blit_buffer(buf, colorfmt='rgba')
            if (self.code_state / 2) % 6 == 3:
                texture.blit_buffer(buf, colorfmt='bgra')
            if (self.code_state / 2) % 6 == 4:
                texture.blit_buffer(buf, colorfmt=camtexture.colorfmt)
            if (self.code_state / 2) % 6 == 5:
                texture = camtexture

        if self.code_state % 2 == 1:
            height = 100
            width = 100
            texture = Texture.create(size=(height, width))
            size = height * width * 3
            buf = [int(64 + x * 127 / size) for x in range(size)]
            for i in range(height):
                buf[3*(i*width+i)] = 0
            buf = bytes(buf)
            if (self.code_state // 2) % 4 == 0:
                texture.blit_buffer(buf, colorfmt='rgb')
            if (self.code_state // 2) % 4 == 1:
                texture.blit_buffer(buf, colorfmt='bgr')
            if (self.code_state // 2) % 4 == 2:
                texture.blit_buffer(buf, colorfmt='rgba')
            if (self.code_state // 2) % 4 == 3:
                texture.blit_buffer(buf, colorfmt='bgra')
            #texture.blit_buffer(buf, colorfmt='bgr')

        #texture = camtexture
        self.ids['image'].texture = texture

    def change_code_state(self):
        self.code_state += 1
        self.ids["button_change_code_state"].text = str(self.code_state)


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
