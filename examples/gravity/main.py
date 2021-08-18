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
from kivy.clock import Clock
import numpy as np
import cv2

import imutils

from plyer import accelerometer
from plyer import gravity


main_kv = '''
<GravityInterface>:
    orientation: 'vertical'
    MDLabel:
        id: x_label
        text: 'X: '
    MDLabel:
        id: y_label
        text: 'Y: '
    MDLabel:
        id: z_label
        text: 'Z: '
    MDLabel:
        id: status
        text: ''
    BoxLayout:
        size_hint_y: None
        height: '48dp'
        padding: '4dp'
        ToggleButton:
            id: toggle_button
            text: 'Start Gravity Sensor'
            on_press: root.do_toggle()
'''


class GravityInterface(BoxLayout):
    def __init__(self):
        super().__init__()
        self.sensorEnabled = False

    def do_toggle(self):
        try:
            if not self.sensorEnabled:
                gravity.enable()
                Clock.schedule_interval(self.get_gravity, 1 / 20.)

                self.sensorEnabled = True
                self.ids.toggle_button.text = "Stop Gravity Sensor"
            else:
                gravity.disable()
                Clock.unschedule(self.get_gravity)

                self.sensorEnabled = False
                self.ids.toggle_button.text = "Start Gravity Sensor"
        except NotImplementedError:
            import traceback
            traceback.print_exc()
            status = "Gravity sensor is not implemented " \
                     "for your platform"
            self.ids.status.text = status

    def get_gravity(self, dt):
        val = gravity.gravity

        if not val == (None, None, None):
            self.ids.x_label.text = "X: " + str(val[0])
            self.ids.y_label.text = "Y: " + str(val[1])
            self.ids.z_label.text = "Z: " + str(val[2])


class GravityApp(MDApp):
    def build(self):
        Builder.load_string(main_kv)
        return GravityInterface()


if __name__ == '__main__':
    GravityApp().run()
