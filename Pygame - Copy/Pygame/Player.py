#Player script
#Imports
import Vector as Vector;
import pygame;
from pygame.locals import*;
import Constants;
import Enemy as enemy;

class Player:
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
    def __update__(self, enemies):
        # Update the position
        #self.position += self.velocity;
        #Set velocity to 0 at the start
        # and the velocity and rotation
        #velocity += steering.linear * time;
        # Check for speeding and clip
        #if velocity.length() > maxSpeed:
            #velocity.normalize();
        #velocity *= maxSpeed;
        closest_enemy = None
        closest_distance = float('inf')
        for enemy in enemies:
            distance = self.distance_to(enemy)
            if distance < closest_distance:
                closest_enemy = enemy
                closest_distance = distance
                self.position.x -= enemy.position.x
                self.position.y -= enemy.position.y
        self.center = self.__calcCenter__();
    def __calcCenter__(self):
        centerx = self.position.x + self.size/2;
        centery = self.position.y + self.size/2;
        center = Vector.Vector (centerx, centery);
        return center;
    def __seek__(self, target: Vector.Vector):
        distance = Vector.Vector.__sub__(self, target)
        Vector.Vector(distance)
        if(Vector.Vector.__length__() >= Constants.PLAYER_RANGE):
            
        
        
        
        
 
 




