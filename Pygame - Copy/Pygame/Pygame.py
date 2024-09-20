#Main script
#Imports
import pygame;
import Player as Player;
import Enemy as Enemy;
from pygame.locals import*;
import Constants;
#Initialization
pygame.init();
screen = pygame.display.set_mode((Constants.WORLD_WIDTH, Constants.WORLD_HEIGHT));
done = False;
x=30;
y=30;
clock = pygame.time.Clock();
player = Player.Player(Constants.PLAYER_POSITION, Constants.PLAYER_SPEED, Constants.PLAYER_SIZE, Constants.PLAYER_COLOR);
enemy = Enemy.Enemy(Constants.ENEMY_POSITION, Constants.ENEMY_SPEED, Constants.ENEMY_SIZE, Constants.ENEMY_COLOR);
#Loop
enemies = list();
while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True;
        #reset screen
        screen.fill((100, 149, 237));
        #update's player position methods
        enemy.__update__(player);
        enemy.__draw__(screen);
        player.__update__(enemies);
        player.__draw__(screen);
        pygame.display.flip();
        #Keep fps standard
        clock.tick(60)