from math import pi
class Circle(object):
    """
    This class get radius in its constructor and can calculate and return the
    area and perimeter of the circle.
    """
    def __init__(self,radius=10):
        """
        constructor get radius which has a default value of 10 and assign that
        value to the local variable
        """
        self.radius=radius
    def area(self):
        """
        area: returns computed area of the circle
        """
        return pi*self.radius*self.radius
    def perimeter(self):
        """
        perimeter: returns computed perimeter of the circle
        """
        return 2*pi*self.radius