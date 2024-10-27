from abc import ABC, abstractmethod

class GeometricShape(ABC):
    @abstractmethod
    def area(self):
        pass    

    @abstractmethod
    def __repr__(self):
        pass    
      
    @abstractmethod
    def name(cls):
        pass