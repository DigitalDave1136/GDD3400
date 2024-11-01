import pygame
import Vector
import random
import math

from Vector import Vector
from Constants import *
from math import atan2

class Agent:

	def __init__(self, position, width, height, speed, image):
		self.position = position
		self.size = Vector(width, height)
		self.speed = speed
		self.image = image
		self.angle = 0
		self.velocity = Vector(random.uniform(-1, 1), random.uniform(-1, 1))
		self.target = Vector(0, 0)
		#self.boundaryAppliedForce = Vector(0, 0)
		#self.boundaryVector = Vector(0, 0)
		self.updateCenter()
		self.updateUpperLeft()
		self.updateRect()
		
		

	def __str__(self):
		return 'Agent (%d, %d, %d, %d)' % (self.size, self.position, self.velocity, self.center)

	def setVelocity(self, velocity):
		self.velocity = velocity.normalize()

	def updateCenter(self):
		self.center = self.position + self.size.scale(0.5)

	def updateUpperLeft(self):
		self.upperLeft = self.center - Vector(self.image.get_width() / 2, self.image.get_height() / 2)

	def updateAngle(self):
		self.angle = math.degrees(atan2(-self.velocity.x, -self.velocity.y))

	def updateRect(self):
		self.surf = pygame.transform.rotate(self.image, self.angle)
		self.rect = self.surf.get_bounding_rect()
		self.rect.move_ip(self.upperLeft.x, self.upperLeft.y)

	def isInCollision(self, agent):
		if pygame.Rect.colliderect(self.rect, agent.rect):
			return True
		else:
			return False

	def clampToBounds(self, bounds):
		#Resets it to 0 so that whenever the clamp is called even when none of the ifs are applied that it doesn't affect the velocity
		#self.boundaryVector = Vector(0, 0)
		#If the position is less than the threshold
		if self.position.x < 0:
			#Have the vector's force be velocity times a multiple of position - threshold divided by the threshold so it goes from 0 to -1 the closer it reaches the boundary
			#self.boundaryVector.x = self.velocity.x * ((self.position.x - BOUNDARY_THRESHOLD)/BOUNDARY_THRESHOLD)	
			self.velocity.x *= -1
		#If the position is greater than the boundary minus the threshold
		if self.position.x > bounds.x - self.size.x:
			#Have the vector's force be velocity times a multiple of position - bounds - threshold divided by the threshold so it goes from 0 to -1 the closer it reaches the boundary
			#self.boundaryVector.x = self.velocity.x * ((self.position.x - bounds.x - BOUNDARY_THRESHOLD - self.size.x)/BOUNDARY_THRESHOLD)
			self.velocity.x *= -1
		#If the position is less than the threshold
		if self.position.y < 0:
			#Have the vector's force be velocity times a multiple of position - threshold divided by the threshold so it goes from 0 to -1 the closer it reaches the boundary
			#self.boundaryVector.y = self.velocity.y * ((self.position.y - BOUNDARY_THRESHOLD)/BOUNDARY_THRESHOLD)
			self.velocity.y *= -1
		#If the position is greater than the boundary minus the threshold
		if self.position.y > bounds.y - self.size.y:
			#Have the vector's force be velocity times a multiple of position - bounds - threshold divided by the threshold so it goes from 0 to -1 the closer it reaches the boundary
			#self.boundaryVector.y = self.velocity.y * ((self.position.x - bounds.y - BOUNDARY_THRESHOLD - self.size.x)/BOUNDARY_THRESHOLD)
			self.velocity.y *= -1
		#Clamp at the bounds anyway so you can't leave the boundary
		self.position.x = max(0, min(self.position.x, bounds.x - self.size.x))
		self.position.y = max(0, min(self.position.y, bounds.y - self.size.y))
		#Scale the vector by the force
		#self.boundaryAppliedForce = self.boundaryVector.scale(BOUNDARY_FORCE)



	def update(self, deltaTime, bounds):
		self.position = self.position + self.velocity.scale(self.speed * deltaTime)
		self.clampToBounds(bounds)
		self.updateCenter()
		self.updateUpperLeft()
		self.updateRect()
		self.updateAngle()

	def draw(self, screen):
		pygame.draw.rect(screen, (0, 0, 0), self.rect, 1)
		self.surf = pygame.transform.rotate(self.image, self.angle)
		screen.blit(self.surf, [self.upperLeft.x, self.upperLeft.y])
		pygame.draw.line(screen, (0, 0, 255), (self.center.x, self.center.y), 
				   (self.center.x + (self.velocity.x * self.size.x * 2), 
					self.center.y + (self.velocity.y * self.size.y * 2)), 3)

