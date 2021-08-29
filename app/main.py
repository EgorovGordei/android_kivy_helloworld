import kivy 
from kivy.app import App 
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivymd.app import FpsMonitoring, MDApp
from kivy.clock import Clock


FPS = 60

class CanvasWidget(Widget):
    rect_movement_line = []

    def __init__(self, **kwargs):
        global FPS
        
        super(CanvasWidget, self).__init__(**kwargs)
        Clock.schedule_interval(self.tick, 1.0/ FPS)
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
    
    def tick(self, something):
        if self.rect_movement_line != []:
            self.rect2.pos = (self.rect_movement_line[0][0], self.rect_movement_line[0][1])
            self.rect_movement_line = self.rect_movement_line[1:]

    def on_touch_down(self, touch):
        #self.rect2.pos = touch.pos
        x = self.rect2.pos[0]
        y = self.rect2.pos[1]
        if self.rect_movement_line != []:
            x = self.rect_movement_line[-1][0]
            y = self.rect_movement_line[-1][1]
        dx = (touch.x - x) / 100.0
        dy = (touch.y - y) / 100.0
        for i in range(100):
            self.rect_movement_line.append([int(x + dx * i), int(y + dy * i)])

    def on_touch_move(self, touch):
        #self.rect2.pos = touch.pos
        pass


class CanvasApp(MDApp):
    def build(self):
        return CanvasWidget()
  

CanvasApp().run()
