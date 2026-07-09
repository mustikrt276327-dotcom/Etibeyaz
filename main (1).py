from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle, Ellipse
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.clock import Clock

Window.fullscreen = True

class UrunButton(Button):
    def __init__(self, **kwargs):
        self.is_yarim = kwargs.pop('is_yarim', False)
        self.is_geri = kwargs.pop('is_geri', False)
        super().__init__(**kwargs)
        
        self.background_color = (0, 0, 0, 0)
        
        if self.is_yarim:
            self.color = (1, 1, 1, 1)
            self.font_size = 28
        elif self.is_geri:
            self.color = (1, 1, 1, 1)
            self.font_size = 45  
        else:
            self.color = (0, 0, 0, 1)
            self.font_size = 34
            
        self.bold = True
        self.halign = "center"
        self.valign = "middle"

        with self.canvas.before:
            if self.is_yarim:
                Color(0.05, 0.15, 0.3, 1)  
                self.kart = RoundedRectangle(radius=[25], pos=self.pos, size=self.size)
            elif self.is_geri:
                Color(0.2, 0.2, 0.2, 1)    
                self.kart = Ellipse(pos=self.pos, size=self.size)
            else:
                Color(1, 1, 1, 1)          
                self.kart = RoundedRectangle(radius=[25], pos=self.pos, size=self.size)
         