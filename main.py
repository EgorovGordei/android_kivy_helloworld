import kivy
kivy.require("1.9.1")

from kivy.app import App
from kivy.uix.button import Button


class ButtonApp(App):
    def build(self):
        self.btn = Button(text ="Tap",
                   font_size ="20sp",
                   background_color =(1, 0.1, 0.1, 1),
                   color =(1, 1, 1, 1),
                   size =(32, 32),
                   size_hint =(.2, .2),
                   pos =(300, 250))
        self.btn.bind(on_press = self.callback)
        return self.btn

    def callback(self, event):
        if self.btn.text == "Tap":
            self.btn.text = "1"
        else:
            self.btn.text = str(int(self.btn.text) + 1)


root = ButtonApp()
root.run()
