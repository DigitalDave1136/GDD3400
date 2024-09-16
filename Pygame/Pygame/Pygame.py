#Main script
#Imports
import pygame;
import Player as Player;
from pygame.locals import*;
#Initialization
pygame.init();
screen = pygame.display.set_mode((800, 600));
done = False;
x=30;
y=30;
clock = pygame.time.Clock();
player = Player.Player(25, 25, 0, 25);
#Loop
while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True;
        #reset screen
        screen.fill((100, 149, 237));
        #update's player position methods
        player.__update__();
        player.__draw__(screen);
        pygame.display.flip();
        #Keep fps standard
        clock.tick(60)