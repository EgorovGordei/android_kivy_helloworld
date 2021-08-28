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

import imutils

from plyer import accelerometer


mainkv = """
<AccelerometerTest>:
    BoxLayout:
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
            id: accel_status
            text: ''

        BoxLayout:
            size_hint_y: None
            height: '48dp'
            padding: '4dp'

            ToggleButton:
                id: toggle_button
                text: 'Start accelerometer'
                on_press: root.do_toggle()
"""

class AccelerometerTest(BoxLayout):
    def __init__(self):
        super().__init__()
        self.sensorEnabled = False

    def do_toggle(self):
        try:
            if not self.sensorEnabled:
                accelerometer.enable()
                Clock.schedule_interval(self.get_acceleration, 1 / 20.)

                self.sensorEnabled = True
                self.ids.toggle_button.text = "Stop Accelerometer"
            else:
                accelerometer.disable()
                Clock.unschedule(self.get_acceleration)

                self.sensorEnabled = False
                self.ids.toggle_button.text = "Start Accelerometer"
        except NotImplementedError:
            import traceback
            traceback.print_exc()
            status = "Accelerometer is not implemented for your platform"
            self.ids.accel_status.text = status

    def get_acceleration(self, dt):
        val = accelerometer.acceleration[:3]

        if not val == (None, None, None):
            self.ids.x_label.text = "X: " + str(val[0])
            self.ids.y_label.text = "Y: " + str(val[1])
            self.ids.z_label.text = "Z: " + str(val[2])


class AccelerometerTestApp(MDApp):
    def build(self):
        Builder.load_string(mainkv)
        return AccelerometerTest()

    def on_pause(self):
        return True


if __name__ == '__main__':
    AccelerometerTestApp().run()
