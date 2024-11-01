import pygame
import Vector
import random
import Constants
import DrawableObject

from Vector import Vector
from DrawableObject import *

class Agent(DrawableObject):

	def __init__(self, image, position, size, speed, color):
		super().__init__(image, position, size, color)
		self.position = position
		self.size = size
		self.speed = speed
		self.velocity = Vector(random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0))
		self.targetVelocity = self.velocity
		self.color = color
		self.updateCenter()
		self.updateRect()
		self.angularSpeed = 0

	def __str__(self):
		return 'Agent (%s, %s, %s, %s)' % (self.size, self.position, self.velocity, self.center)

	def moveTowardTargetVelocity(self):
		velocityDiff = self.targetVelocity - self.velocity
		#print("velocityDiff", velocityDiff)
		#print("velocityDiff.length()", velocityDiff.length())
		if (velocityDiff.length() < self.angularSpeed):
			self.velocity = self.targetVelocity
		else:
			self.velocity += velocityDiff.normalize().scale(self.angularSpeed)
		self.velocity = self.velocity.normalize()
		#print("velocity", self.velocity)

	def updateCenter(self):
		self.center = self.position + self.size.scale(0.5)

	def updateRect(self):
		self.boundingRect = pygame.Rect(self.position.x, self.position.y, self.size.x, self.size.y)

	def clampToBounds(self, bounds):
		self.position.x = max(0, min(self.position.x, bounds.x - self.size.x))
		self.position.y = max(0, min(self.position.y, bounds.y - self.size.y))

	def computeBoundaryInfluence(self, bounds):
		boundsInfluence = Vector(0, 0)
		self.boundaries = []

		# If at the left wall
		if self.position.x < Constants.SHEEP_BOUNDARY_RADIUS:
			boundsInfluence += Vector(Constants.SHEEP_BOUNDARY_RADIUS - self.position.x, 0)
			self.boundaries += [Vector(0, self.position.y)]
		# If at the right wall
		elif self.position.x > bounds.x - Constants.SHEEP_BOUNDARY_RADIUS:
			boundsInfluence += Vector((bounds.x - self.position.x) - Constants.SHEEP_BOUNDARY_RADIUS, 0)
			self.boundaries += [Vector(bounds.x, self.position.y)]

		# If at the top wall
		if self.position.y < Constants.SHEEP_BOUNDARY_RADIUS:
			boundsInfluence += Vector(0, Constants.SHEEP_BOUNDARY_RADIUS - self.position.y)
			self.boundaries += [Vector(self.position.x, 0)]
		# If at the bottom wall
		elif self.position.y > bounds.y - Constants.SHEEP_BOUNDARY_RADIUS:
			boundsInfluence += Vector(0, (bounds.y - self.position.y) - Constants.SHEEP_BOUNDARY_RADIUS)
			self.boundaries += [Vector(self.position.x, bounds.y)]

		return boundsInfluence


	def update(self, deltaTime, bounds):

		self.moveTowardTargetVelocity()
		self.position = self.position + self.velocity.scale(self.speed * deltaTime)
		self.clampToBounds(bounds)
		self.updateCenter()
		self.updateRect()
		self.calcSurface()

	def draw(self, screen):
		self.angle = math.degrees(math.atan2(-self.velocity.y, self.velocity.x)) - 90
		super().draw(screen)
		if Constants.DEBUG_VELOCITY:
			pygame.draw.line(screen, (0, 0, 255), (self.center.x, self.center.y), 
					   (self.center.x + (self.velocity.x * self.size.x * 2), 
						self.center.y + (self.velocity.y * self.size.y * 2)), Constants.DEBUG_LINE_WIDTH)
			
		if Constants.DEBUG_BOUNDARIES:
			for boundary in self.boundaries:
				pygame.draw.line(screen, (255, 0, 255), (self.center.x, self.center.y), 
								 (boundary.x, boundary.y), Constants.DEBUG_LINE_WIDTH)