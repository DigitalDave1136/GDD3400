import pygame
import random
import Vector
import Sheep
import Agent
import Dog
import Constants

from pygame import *
from random import *
from Vector import *
from Sheep import *
from Agent import *
from Dog import *

#Debug handler
def handleDebugging():        
    # Handle the Debugging for Forces
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYUP:

            # Toggle Dog Influence
            if event.key == pygame.K_1:
                Constants.ENABLE_DOG = not Constants.ENABLE_DOG
                print("Toggle Dog Influence", Constants.ENABLE_DOG)

            # Toggle Alignment Influence
            if event.key == pygame.K_2: 
                Constants.ENABLE_ALIGNMENT = not Constants.ENABLE_ALIGNMENT
                print("Toggle Alignment Influence", Constants.ENABLE_ALIGNMENT)

            # Toggle Separation Influence
            if event.key == pygame.K_3: 
                Constants.ENABLE_SEPARATION = not Constants.ENABLE_SEPARATION
                print("Toggle Separation Influence", Constants.ENABLE_SEPARATION)

            # Toggle Cohesion Influence
            if event.key == pygame.K_4: 
                Constants.ENABLE_COHESION = not Constants.ENABLE_COHESION
                print("Toggle Cohesion Influence", Constants.ENABLE_COHESION)

            # Toggle Boundary Influence
            if event.key == pygame.K_5: 
                Constants.ENABLE_BOUNDARIES = not Constants.ENABLE_BOUNDARIES
                print("Toggle Boundary Influence", Constants.ENABLE_BOUNDARIES)

            # Toggle Dog Influence Lines
            if event.key == pygame.K_6: 
                Constants.DEBUG_DOG_INFLUENCE = not Constants.DEBUG_DOG_INFLUENCE
                print("Toggle Dog Influence Lines", Constants.DEBUG_DOG_INFLUENCE)
    
            # Toggle Velocity Lines
            if event.key == pygame.K_7: 
                Constants.DEBUG_VELOCITY = not Constants.DEBUG_VELOCITY
                print("Toggle Velocity Lines", Constants.DEBUG_VELOCITY)

            # Toggle Neighbor Lines
            if event.key == pygame.K_8: 
                Constants.DEBUG_NEIGHBORS = not Constants.DEBUG_NEIGHBORS
                print("Toggle Neighbor Lines", Constants.DEBUG_NEIGHBORS)

            # Toggle Boundary Force Lines
            if event.key == pygame.K_9: 
                Constants.DEBUG_BOUNDARIES = not Constants.DEBUG_BOUNDARIES
                print("Toggle Boundary Force Lines", Constants.DEBUG_BOUNDARIES)

            # Toggle Bounding Box Lines
            if event.key == pygame.K_0: 
                Constants.DEBUG_BOUNDING_RECTS = not Constants.DEBUG_BOUNDING_RECTS
                print("Toggle Bounding Box Lines", Constants.DEBUG_BOUNDING_RECTS)

#Method to calculate the sheep's neighbors and assign them to each other for the herd scripts
def calculateNeighbors(herd):
    for sheep in herd:
        sheep.neighbors = []
        for other in herd:
            if sheep != other:
                distanceFrom = sheep.position - other.position
                distanceFrom = distanceFrom.length()
                if distanceFrom < Constants.SHEEP_NEIGHBOR_RADIUS:
                    sheep.neighbors.append(other)

pygame.init();

screen = pygame.display.set_mode((Constants.WORLD_WIDTH, Constants.WORLD_HEIGHT))
clock = pygame.time.Clock()
bounds = Vector(Constants.WORLD_WIDTH, Constants.WORLD_HEIGHT)
sheepImage = pygame.image.load('sheep.png')
dogImage = pygame.image.load('dog.png')

sheep = []
if(Constants.ENABLE_DOG):
    dog = Dog(dogImage, Vector(Constants.WORLD_WIDTH / 2, Constants.WORLD_HEIGHT / 2), 
				    Vector(Constants.DOG_WIDTH, Constants.DOG_HEIGHT), Constants.DOG_SPEED, (255, 255, 255))

for x in range(100):
	sheep += [Sheep(sheepImage, Vector(randrange(1,int(bounds.x + 1)), randrange(1,int(bounds.y + 1))), 
					  Vector(Constants.DOG_WIDTH, Constants.DOG_HEIGHT), Constants.SHEEP_SPEED, (0, 255, 0))]

# While the user has not selected quit
hasQuit = False

while not hasQuit:
    
    handleDebugging()
	# Clear the screen
    screen.fill(Constants.BACKGROUND_COLOR)
    
	# Process all in-game events
    for event in pygame.event.get():
        if event.type == pygame.QUIT \
			or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            hasQuit = True

    deltaTime = clock.get_time() / 1000
    calculateNeighbors(sheep)
	# Update the agents onscreen
    if(Constants.ENABLE_DOG):
        dog.update(deltaTime, bounds, sheep)
    for enemy in sheep:
        enemy.update(deltaTime, bounds, dog)
    
	# Draw the agents onscreen
    if(Constants.ENABLE_DOG):
        dog.draw(screen)
    for enemy in sheep:
        enemy.draw(screen)

	# Double buffer
    pygame.display.flip()

	# Limit to 60 FPS
    clock.tick(Constants.FRAME_RATE)

# Quit
pygame.quit()

