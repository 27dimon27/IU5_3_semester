from Rectangle import *

class Square(Rectangle):
    shape_name = "Квадрат"    
    def __init__(self, side, color):
        super().__init__(side, side, color)
   
    def name(cls):
        return cls.shape_name