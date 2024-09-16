#Player script
#Imports
import Vector as Vector;
import pygame;
from pygame.locals import*;

class Player:
    #initialize player script
    def __init__(self, x, y, velocity, size):
        self.size = size;
        self.x = x;
        self.y = y;
        self.velocity = Vector.Vector(0, 0);
    #draw the player originally
    def __draw__(self, screen):
        pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(self.x, self.y, self.size, self.size));
    #Everything in the update method is called around every second
    def __update__(self):
        #Set velocity to 0 at the start
        self.velocity = Vector.Vector(0, 0);
        #Press up and down changes the velocity to 3 for y in directions and if not then sets it to 0
        pressed = pygame.key.get_pressed();
        if pressed[pygame.K_w]: self.velocity.y -= 3;
        elif pressed[pygame.K_s]: self.velocity.y += 3;
        else: self.velocity.y = 0; 
        #Press left and right changes the velocity to 3 for x in directions and if not then sets it to 0
        if pressed[pygame.K_a]: self.velocity.x -= 3;
        elif pressed[pygame.K_d]: self.velocity.x += 3;
        else: self.velocity.x = 0; 
        #Print the velocity using the string method
        print(Vector.Vector.__str__(self.velocity.x, self.velocity.y));
        #normalize the velocity
        self.velocity = self.velocity.__normalize__();
        #Increase position as velocity amount
        self.x += self.velocity.x;
        self.y += self.velocity.y;




