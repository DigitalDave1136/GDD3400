import pygame
import Vector
import Agent
import Constants
import random

from pygame import *
from Vector import Vector
from Agent import *

class Sheep(Agent):
	def __init__(self, position, width, height, speed, image):
		super().__init__(position, width, height, speed, image)
		self.player = 0
		self.timer = 0

	def isPlayerClose(self):
		return (self.player.center - self.center).length() < Constants.MIN_ATTACK_DIST

	def update(self, deltaTime, bounds, player):
		print(self.timer)
		self.timer += 1
		self.player = player
		
		# Flee from the player
		if self.isPlayerClose():
			direction = self.center - player.center
			normalizedDirection = direction.normalize()
			appliedForce = normalizedDirection.scale(SHEEP_FORCE_FLEE)
			#appliedForce += self.boundaryAppliedForce
			#appliedForce = appliedForce.__add__(self.boundaryVector)
			super().setVelocity(appliedForce)
		# Wander
		elif self.timer == 30:
			perpendicularVec = Vector(-self.velocity.y, self.velocity.x)
			perpendicularVec = perpendicularVec.scale(random.uniform(-1, 1) * .5)
			direction = self.velocity + perpendicularVec
			normalizedDirection = direction.normalize()
			appliedForce = normalizedDirection.scale(SHEEP_FORCE_WANDER)
			#appliedForce += self.boundaryAppliedForce
			#appliedForce = appliedForce.__add__(self.boundaryVector)
			super().setVelocity(appliedForce)
		
		if self.timer == 30:
			self.timer = 0

		super().update(deltaTime, bounds)

	def draw(self, screen):
		super().draw(screen)
