from locale import normalize
import pygame

import Vector
import Agent
import random

from Vector import Vector
from Agent import *

isPlayer = False

class Dog(Agent):

	def __init__(self, position, width, height, speed, image):
		super().__init__(position, width, height, speed, image)
		self.targetEnemy = None

	def update(self, deltaTime, bounds, enemies):
		self.enemies = enemies

		# Let the user control the player
		if isPlayer:
			keys = Vector(0, 0)

			# adjust the velocity based on input from the user
			# Handle arrow keys and WASD
			pressed = pygame.key.get_pressed()
			if pressed[pygame.K_UP] or pressed[pygame.K_w]: 
				keys.y -= 1
			if pressed[pygame.K_DOWN] or pressed[pygame.K_s]: 
				keys.y += 1
			if pressed[pygame.K_LEFT] or pressed[pygame.K_a]: 
				keys.x -= 1
			if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]: 
				keys.x += 1
			super().setVelocity(keys)
		else:
			# If we don't have a target enemy, select and enemy at random to chase
			if self.targetEnemy == None or self.isInCollision(self.targetEnemy):
				self.targetEnemy = self.enemies[random.randrange(0, len(self.enemies))]
			
			# Get our current direction
			#currentDirection = Vector(-self.velocity.y, self.velocity.x)
			# Set our direction to chase the enemy we've targetted
			targetDirection = self.targetEnemy.position - self.position
			#normalize the applied force
			normalizedTargetDirection = targetDirection.normalize()
			#normalizedCurrentDirection = currentDirection.normalize()
			#differenceVector = normalizedTargetDirection - normalizedCurrentDirection
			#differenceVectorLength = differenceVector.length()
			#if(differenceVectorLength < DOG_TURNING_SPEED):
			#	normalizedCurrentDirection = normalizedTargetDirection
			#else: 
			#	normalizedDifferenceVector = differenceVector.normalize()
			#	appliedDifferenceVector = normalizedDifferenceVector.scale(DOG_TURNING_SPEED)
			#	normalizedCurrentDirection = normalizedCurrentDirection + appliedDifferenceVector

				
			#Scale the direction by the force
			appliedForce = normalizedTargetDirection.scale(DOG_FORCE)
			#Add the normalized applied force to the applied force
			#appliedForce += self.boundaryAppliedForce
			#Set normalize the velocity for use
			super().setVelocity(appliedForce)

		# Set the velocity and update position
		super().update(deltaTime, bounds)

	def draw(self, screen):
		super().draw(screen)
		pygame.draw.line(screen, (255, 0, 0), (self.center.x, self.center.y), 
			(self.targetEnemy.center.x, self.targetEnemy.center.y), 3)
