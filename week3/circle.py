from math import pi
class Circle(object):
    def __init__(self,radius):
        self.radius=radius
    def area(self):
        return pi*self.radius*self.radius
    def perimeter(self):
        return 2*pi*self.radius