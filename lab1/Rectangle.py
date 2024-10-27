from GeometricShape import *
from ShapeColor import *

class Rectangle(GeometricShape):
    shape_name = "Прямоугольник"    
    def __init__(self, width, height, color):
        self.width = width
        self.height = height
        self.color = ShapeColor(color)

    def area(self):
        return self.width * self.height

    def __repr__(self):
        return "Название: {}, Ширина: {}, Высота: {}, Цвет: {}, Площадь: {}".format(
            self.name(), self.width, self.height, self.color.color, self.area()
        )
  
    def name(cls):
        return cls.shape_name