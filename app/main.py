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
#from plyer import camera
import requests

from kivy.graphics.texture import Texture
from kivy.uix.camera import Camera
from kivy.lang import Builder
from kivy.clock import Clock
import numpy as np
import cv2






class Camera2(Camera):
    firstFrame=None
    def _camera_loaded(self, *largs):
        if kivy.platform=='android':
            self.texture = Texture.create(size=self.resolution,colorfmt='rgb')
            self.texture_size = list(self.texture.size)
        else:
            super(Camera2, self)._camera_loaded()

    def on_tex(self, *l):
        if kivy.platform=='android':
            buf = self._camera.grab_frame()
            if not buf:
                return
            frame = self._camera.decode_frame(buf)
            self.image = frame = self.process_frame(frame)
            buf = frame.tostring()
            self.texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
        super(Camera2, self).on_tex(*l)

    def process_frame(self,frame):
        r,g,b=cv2.split(frame)
        frame=cv2.merge((b,g,r))        
        rows,cols,channel=frame.shape
        M=cv2.getRotationMatrix2D((cols/2,rows/2),90,1)
        dst=cv2.warpAffine(frame,M,(cols,rows))
        frame=cv2.flip(dst,1)
        if self.index==1:
            frame=cv2.flip(dst,-1)
        return frame





Builder.load_string("""
<MyLayout>:
    orientation:'vertical'
    padding:(36,36)

    Label:
        text:'opencv demo'
        halign:'left'
        valign:'top'
        size_hint:(1,None)
        height:'48dp'
    Camera2:
        index:0
        resolution:(960,720)
        id:camera
        play:True
    Label:
        id:label
        halign:'left'
        valign:'top'
        size_hint:(1,None)
        height:'48dp'
    Label:
""")


class MyLayout(BoxLayout):
    pass

class MainApp(App):
    def build(self):
        return MyLayout()
    def on_start(self):
        Clock.schedule_once(self.detect,5)

    def detect(self,nap):
        image=self.root.ids.camera.image
        rows,cols=image.shape[:2]
        ctime=time.ctime()[11:19]
        self.root.ids.label.text='%s image rows:%d cols:%d'%(ctime,rows,cols)
        Clock.schedule_once(self.detect,1)

if __name__ == '__main__':
    MainApp().run()
