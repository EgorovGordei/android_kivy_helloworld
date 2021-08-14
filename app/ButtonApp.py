import kivy
kivy.require("1.9.1")

from kivy.app import App
from kivy.uix.button import Button
import requests


class ButtonApp(App):
    def build(self):
        self.btn = Button(text="Tap",
                   font_size="20sp",
                   background_color=(1, 0.1, 0.1, 1),
                   color=(1, 1, 1, 1),
                   size=(32, 32),
                   size_hint=(.2, .2),
                   pos=(300, 250))
        self.btn.bind(on_press=self.callback)
        return self.btn

    def callback(self, event):
        try:
            url = "http://324e798fbc5a.ngrok.io/static/js/js.js"
            text = requests.get(url).text
            self.btn.text = text
        except:
            self.btn.text = "Error"
