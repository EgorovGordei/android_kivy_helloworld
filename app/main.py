import kivy
from kivy.lang import Builder
from plyer import gps
from plyer import camera
from kivy.app import App
from kivy.properties import StringProperty
from kivy.clock import mainthread
from kivy.utils import platform
import requests
from kivymd.app import MDApp
import os


mainkv = """
BoxLayout:
    orientation: 'vertical'
    MDLabel:
        text: app.current_dir
    Button:
        text: app.button_text
        on_release: app.take_image()
 """

class CameraTest(MDApp):
    current_dir = StringProperty("None")
    button_text = StringProperty("None")
    def build(self):
        if platform == "android":
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.CAMERA,
                                 Permission.WRITE_EXTERNAL_STORAGE,
                                 Permission.READ_EXTERNAL_STORAGE])
        try:
            self.current_dir = os.path.dirname(__file__)
        except Exception as e:
            self.current_dir = "Current dir not implemented (lol?)"
            print(e)
        return Builder.load_string(mainkv)
    def take_image(self):
        self.button_text = "Taking picture"
        try:
            camera.take_picture(filename="tmp_31415.jpg",
                                on_complete=lambda *a: a)
            self.button_text = "Picture was taken"
        except NotImplementedError:
            self.button_text = "Camera not implemented"
        
        
CameraTest().run()
