import math

from GeometricShape import *
from ShapeColor import *

class Circle(GeometricShape):
    shape_name = "Круг"    
    def __init__(self, radius, color):
        self.radius = radius
        self.color = ShapeColor(color)

    def area(self):
        return math.pi * self.radius ** 2    
    
    def __repr__(self):
        return "Название: {}, Радиус: {}, Цвет: {}, Площадь: {:.2f}".format(
            self.name(), self.radius, self.color.color, self.area()
        )
   
    def name(cls):
        return cls.shape_name