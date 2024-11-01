import pygame
import random
import Constants

from Vector import *

class DrawableObject(object):
	"""description of class"""
	def __init__(self, image, position, size, color):
		self.upperLeft = position
		self.center = position + size.scale(0.5)
		self.size = size
		self.image = image
		self.angle = 0
		self.calcSurface()
		self.color = color

	def __str__(self):
		return 'DrawableObject (%s, %s)' % (self.center, self.angle)

	def calcSurface(self):
		self.surf = pygame.transform.rotate(self.image, self.angle)
		self.upperLeft = self.center - Vector(self.surf.get_width(), self.surf.get_height()).scale(0.5)
		self.boundingRect = self.surf.get_bounding_rect().move(self.upperLeft.x, self.upperLeft.y)

	def isInCollision(self, agent):
		return pygame.Rect.colliderect(self.boundingRect, agent.boundingRect)

	def draw(self, screen):
		if Constants.DEBUG_BOUNDING_RECTS:
			pygame.draw.rect(screen, (0, 0, 0), self.boundingRect, Constants.DEBUG_LINE_WIDTH)
		screen.blit(self.surf, [self.upperLeft.x, self.upperLeft.y])
