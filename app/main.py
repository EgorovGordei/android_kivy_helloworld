import kivy
from kivy.lang import Builder
from plyer import gps
from kivy.app import App
from kivy.properties import StringProperty
from kivy.clock import mainthread
from kivy.utils import platform
import requests
from kivymd.app import MDApp


mainkv = """
BoxLayout:
    orientation: 'vertical'
    MDLabel:
        text: app.gps_location
    Button:
        text: "Just kivy settings"
        on_release: app.open_settings()
 """

class GpsTest(MDApp):
    gps_location = StringProperty('None')
    def build(self):
        try:
            gps.configure(on_location=self.on_location)
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.ACCESS_COARSE_LOCATION,
                             Permission.ACCESS_FINE_LOCATION])
        except NotImplementedError:
            self.gps_location = "Not implemented"
        return Builder.load_string(mainkv)
    @mainthread
    def on_location(self, **kwargs):
        self.gps_location = '\n'.join([
            '{}={}'.format(k, v) for k, v in kwargs.items()])
        print(self.gps_location)
    def on_resume(self):
        gps.start()
        pass
    def on_pause(self):
        gps.stop()
        return True
        
GpsTest().run()
