import kivy
from kivy.lang import Builder
from plyer import gps
from kivy.app import App
from kivy.properties import StringProperty
from kivy.clock import mainthread
from kivy.utils import platform
import requests
from kivymd.app import MDApp


mainkv = open('main.kv', 'r').read()
URL = "http://de87793c1849.ngrok.io/"

class ChatApp(MDApp):
    last_message = StringProperty('')
    my_message = StringProperty('')

    def build(self):
        kv = mainkv.replace("<URL_INPUT::TEXT>", '"' + URL + '"')
        return Builder.load_string(kv)

    def get_last_message(self):
        URL = self.root.ids.url_input.text
        try:
            self.last_message = requests.get(URL + "get_last_message").text
        except Exception as e:
            self.last_message = "Error"
            print(e)
        print(self.last_message)

    def send_message(self):
        URL = self.root.ids.url_input.text
        try:
            requests.post(url = URL+"send_message",
                          data = {'message':self.my_message})
        except Exception as e:
            self.last_message = "Error"
            print(e)
        self.my_message = ""
        self.root.ids.my_message_input.text = ""

    def my_message_input_ontext(self):
        text = self.root.ids.my_message_input.text
        self.my_message = text


root = ChatApp()
root.run()







'''
from kivy.lang import Builder
from plyer import gps
from kivy.app import App
from kivy.properties import StringProperty
from kivy.clock import mainthread
from kivy.utils import platform

kv = """
BoxLayout:
    orientation: 'vertical'
    Label:
        text: app.gps_location
    Label:
        text: app.gps_status
    BoxLayout:
        size_hint_y: None
        height: '48dp'
        padding: '4dp'
        ToggleButton:
            text: 'Start' if self.state == 'normal' else 'Stop'
            on_state:
                app.start(1000, 0) if self.state == 'down' else \
                app.stop()
"""

class GpsTest(App):

    gps_location = StringProperty('None')
    gps_status = StringProperty('Click Start to get GPS location updates')

    def request_android_permissions(self):
        """
        Since API 23, Android requires permission to be requested at runtime.
        This function requests permission and handles the response via a
        callback.
        The request will produce a popup if permissions have not already been
        been granted, otherwise it will do nothing.
        """
        from android.permissions import request_permissions, Permission

        def callback(permissions, results):
            """
            Defines the callback to be fired when runtime permission
            has been granted or denied. This is not strictly required,
            but added for the sake of completeness.
            """
            if all([res for res in results]):
                print("callback. All permissions granted.")
            else:
                print("callback. Some permissions refused.")

        request_permissions([Permission.ACCESS_COARSE_LOCATION,
                             Permission.ACCESS_FINE_LOCATION], callback)
        # # To request permissions without a callback, do:
        # request_permissions([Permission.ACCESS_COARSE_LOCATION,
        #                      Permission.ACCESS_FINE_LOCATION])

    def build(self):
        try:
            gps.configure(on_location=self.on_location,
                          on_status=self.on_status)
        except NotImplementedError:
            import traceback
            traceback.print_exc()
            self.gps_status = 'GPS is not implemented for your platform'

        self.gps_location = "build... "
        if platform == "android":
            print("gps.py: Android detected. Requesting permissions")
            self.gps_location = self.gps_location +\
                            "gps.py: Android detected. Requesting permissions"
            self.request_android_permissions()
        self.gps_location = self.gps_location + " ...end"

        return Builder.load_string(kv)

    def start(self, minTime, minDistance):
        gps.start(minTime, minDistance)

    def stop(self):
        gps.stop()

    @mainthread
    def on_location(self, **kwargs):
        self.gps_location = '\n'.join([
            '{}={}'.format(k, v) for k, v in kwargs.items()])

    @mainthread
    def on_status(self, stype, status):
        self.gps_status = 'type={}\n{}'.format(stype, status)

    def on_pause(self):
        gps.stop()
        return True

    def on_resume(self):
        gps.start(1000, 0)
        pass


if __name__ == '__main__':
    GpsTest().run()
'''
