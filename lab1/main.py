from GeometricShape import *
from ShapeColor import *
from Rectangle import *
from Circle import *
from Square import *

if __name__ == "__main__":
    N = 8    
    rect = Rectangle(N, N + 2, 'синий')
    circ = Circle(N, 'зеленый')
    sq = Square(N, 'красный')
    print(rect)
    print(circ)
    print(sq)
