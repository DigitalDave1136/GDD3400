import pygame
import Vector
import Agent
import random
import Constants

from Vector import Vector
from Agent import *

isPlayer = False

class Dog(Agent):

	def __init__(self, image, position, size, speed, color):
		super().__init__(image, position, size, speed, color)
		self.targetEnemy = None
		self.angularSpeed = Constants.DOG_TURNING_SPEED
		#self.velocity = Vector(0, 0)

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
			self.targetVelocity = keys.normalize()
		else:
			# If we don't have a target enemy, select an enemy at random to chase
			if self.targetEnemy == None or self.isInCollision(self.targetEnemy):
				self.targetEnemy = self.enemies[random.randrange(0, len(self.enemies))]
			
			# Set our velocity to chase the enemy we've targetted
			self.targetVelocity = self.targetEnemy.position - self.position
			self.targetVelocity = self.targetVelocity.normalize().scale(Constants.DOG_SEEK_INFLUENCE_WEIGHT)
			
		#Get and normalize bounds influence
		boundsInfluence = self.computeBoundaryInfluence(bounds).normalize()
		#Set velocity to be influenced by boundary
		self.targetVelocity = self.targetVelocity + boundsInfluence.scale(Constants.DOG_BOUNDARY_INFLUENCE_WEIGHT * int(Constants.ENABLE_BOUNDARIES))
		self.targetVelocity = self.targetVelocity.normalize()

		# Set the velocity and update position
		super().update(deltaTime, bounds)
		
	#Draw specific to dog script
	def draw(self, screen):
		super().draw(screen)
		#Debug the line to show what the dog is targetting
		if Constants.DEBUG_DOG_INFLUENCE:
			pygame.draw.line(screen, (255, 0, 0), (self.center.x, self.center.y), 
				(self.targetEnemy.center.x, self.targetEnemy.center.y), 3)
