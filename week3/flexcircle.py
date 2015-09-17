from math import pi,sqrt
class FlexCircle(object):
    def __init__(self,radius):
        if not (isinstance(radius,int) or  isinstance(radius,float)):
            raise ValueError("Invalid Input Value")            
        self.__r=radius
    def _setRadius(self,r):
        self.__r=r
    def _getRadius(self):
        return self.__r
    def _setArea(self,area):
        if not (isinstance(area,int) or isinstance(area,float)) :
            raise ValueError("Invalid Input Value")           
        self.__a=area                                                                        
        self.__r=sqrt(area/pi)
        self.__update()
    def _getArea(self):
        self.__update()
        return self.__a
    def _setPerimeter(self,perimeter):
        if not(isinstance(perimeter,int) or isinstance(perimeter,float)) :
            raise ValueError("Invalid Input Value")           
        self.__p=perimeter
        self.__r=perimeter/(2*pi)
        
    def _getPerimeter(self):
        self.__update()
        return self.__p
    def __update(self):
        self.__a=pi*self.radius*self.radius
        self.__p=2*pi*self.radius
    radius=property(fget=_getRadius,fset=_setRadius)
    perimeter=property(fget=_getPerimeter,fset=_setPerimeter)
    area=property(fget=_getArea,fset=_setArea)


        
        