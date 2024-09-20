#Player script
#Imports
import Vector as Vector;
import pygame;
from pygame.locals import*;
import Constants;
import Vector as Vector;
import math;
import random;


class Enemy(object):
    #initialize player script
    def __init__(self, position, speed, size, color):
        self.size = size;
        self.position = position;
        print(self.position.x, self.position.y)
        self.speed = speed;
        self.center = self.__calcCenter__();
        print(self.center.x, self.center.y);
        self.velocity = Vector.Vector(0, 0);
        self.color = color;
    def __str__(self, x, y, speed, size, velocity):
        return "Vector (" + str(x) + "," + str(y) + ")";
    #draw the player originally
    def __draw__(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.position.x, self.position.y, self.size, self.size));
        pygame.draw.line(screen, (0, 0, 255), (self.center.x, self.center.y), (self.center.x + self.size * self.velocity.x, self.center.y + self.size * self.velocity.y), 5);
    #Everything in the update method is called around every second
    def __update__(self, player = None):
        
        if(self.position.x < Constants.PLAYER_RANGE):
            # flee from the player
            # calculate the vector from the player to the enemy
            dx = self.position.x - player.position.x
            dy = self.position.y - player.position.y
            # normalize the vector
            magnitude = math.sqrt(dx**2 + dy**2)
            if (magnitude < 200):
                # set the velocity of enemy to the normalized vector
                self.velocity = Vector.Vector(dx/magnitude, dy/magnitude)
                # multiply the speed by the velocity and time
                self.position.x += self.velocity.x * self.speed
                self.position.y += self.velocity.y * self.speed
        else:
            # wander randomly by selecting a random direction similar to previous vector
            self.position.x += random.randint(-1, 1)
            self.position.y += random.randint(-1, 1)   
    def __calcCenter__(self):
        centerx = self.position.x + self.size/2;
        centery = self.position.y + self.size/2;
        center = Vector.Vector (centerx, centery);
        return center;        
    def __distance_to__(self, player):
        hypotenuse = math.sqrt(self.position.x**2 + player.position.x**2 + self.y**2 + player.y**2);
            
        
    




