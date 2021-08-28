import kivy 
from kivy.app import App 
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivymd.app import MDApp


class CanvasWidget(Widget):
    def __init__(self, **kwargs):
        super(CanvasWidget, self).__init__(**kwargs)
        with self.canvas:
            Color(1, 1, 1, 1) 
            self.rect = Rectangle(source ="Egypt_human_torches.png",
                                  pos = self.pos, size = self.size)
            self.pos[0] += 100
            self.pos[1] += 100
            self.rect2 = Rectangle(source ="Egypt_human_torches.png",
                                  pos = self.pos, size = self.size)
            self.pos[0] -= 100
            self.pos[1] -= 100
            self.rect3 = Rectangle(source ="Egypt_human_torches.png",
                                  pos = self.pos, size = (150, 150))
            self.pos[0] += 0
            self.pos[1] += 0
            self.bind(pos = self.update_rect,
                  size = self.update_rect)
  
    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
    
    def on_touch_down(self, touch):
        self.rect2.pos = touch.pos

    def on_touch_move(self, touch):
        self.rect2.pos = touch.pos


class CanvasApp(MDApp):
    def build(self):
        return CanvasWidget()
  

CanvasApp().run()
