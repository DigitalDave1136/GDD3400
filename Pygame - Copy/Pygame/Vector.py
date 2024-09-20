#Vector script
#Imports
from pickle import NONE
from re import S
import string
import math;

class Vector:
    #Vector's initialization
    def __init__(self, x, y):
        self.x = x;
        self.y = y;
    #Turning results as a string for printing
    def __str__(x, y):
        return "Vector (" + str(x) + "," + str(y) + ")"
    #Adding vectors together
    def __add__(self = None, other = None):
        if(self != None and other != None):
            x = self.x + other.x;
            y = self.y + other.y;
            return x, y;
    #Subtracting vectors together
    def __sub__(self = None, other = None):
        if(self != None and other != None):
            x = self.x - other.x;
            y = self.y - other.y;
            return x, y;
    #Getting the dot method of 2 vectors
    def __dot__(self, other):
        x = self.x * other.x;
        y = self.y * other.y;
        dot_product = x+y;
        return dot_product;
    #scaling a vector
    def __scale__(self, scalar):
        x = self.x * float (scalar);
        y = self.y * float (scalar);
        return x, y;
    #Getting the length of a vector
    def __length__(self):
        hypotenuse = math.sqrt(self.x**2 + self.y**2);
        return hypotenuse;
    #Normalizing a vector using the length
    def __normalize__(self):
        hypotenuse = self.__length__();
        if hypotenuse == 0:
            return Vector(0,0);
        x = self.x / hypotenuse
        y = self.y / hypotenuse
        return Vector(x, y);
        
        




