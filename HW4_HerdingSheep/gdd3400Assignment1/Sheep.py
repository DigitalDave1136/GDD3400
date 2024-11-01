import pygame
import Vector
import Agent
import Constants
import random

from pygame import *
from Vector import Vector
from Agent import *

class Sheep(Agent):
	def __init__(self, image, position, size, speed, color):
		super().__init__(image, position, size, speed, color)
		self.player = 0
		self.timer = 0
		self.angularSpeed = Constants.SHEEP_TURNING_SPEED
		self.neighbors = []

	#Method used to get dog influence
	def computeDogInfluence(self, player):
		vectToDog = self.position - player.position
		self.target = player
		if vectToDog.length() < Constants.MIN_ATTACK_DIST:
			self.drawDogInfluence = True
			return vectToDog
		else:
			self.drawDogInfluence = False
		return Vector(0, 0)

	#Method used to get the vectors for alignment
	def computeAlignment(self):
		vectors = Vector(0, 0)
		if len(self.neighbors) == 0:
			return vectors
		for sheep in self.neighbors:
			if sheep != self:
					vectors += sheep.velocity
					vectors = vectors.scale(1/len(self.neighbors))
					vectors.normalize()
		return vectors
					

	#Method used to get the vectors for cohesion
	def computeCohesion(self):
		vectors = Vector(0, 0)
		if len(self.neighbors) == 0:
			return vectors
		for sheep in self.neighbors:
			if sheep != self:
					vectors += sheep.position - self.position
					vectors = vectors.scale(1/len(self.neighbors))
					#vectors = Vector(vectors.x - self.position.x, vectors.y - self.position.y)
					#vectors -= self.position
					vectors.normalize()
		return vectors

	#Method used to get the vectors for separation
	def computeSeparation(self):
		vectors = Vector(0, 0)
		if len(self.neighbors) == 0:
			return vectors
		for sheep in self.neighbors:
			if sheep != self:
					vectors += sheep.position - self.position
					vectors = vectors.scale(1/len(self.neighbors))
					vectors = vectors.scale(-1)
					vectors.normalize()
		return vectors

	def update(self, deltaTime, bounds, player):
		#print(self.timer)
		self.timer += 1
		self.player = player
		#Get the herd functions
		alignment = self.computeAlignment();
		cohesion = self.computeCohesion();
		separation = self.computeSeparation();
		# Flee from the player
		if (self.position - player.position).length() < Constants.MIN_ATTACK_DIST:
			dogInfluence = self.computeDogInfluence(player).normalize()
			#print("dogInfluence", dogInfluence)
			self.targetVelocity = dogInfluence.scale(Constants.SHEEP_DOG_INFLUENCE_WEIGHT * int(Constants.ENABLE_DOG))					
		#Recalculate our Wander direction

		boundsInfluence = self.computeBoundaryInfluence(bounds).normalize()

		#Forces all together now
		forces = ((alignment.scale(Constants.SHEEP_ALIGNMENT_WEIGHT * int(Constants.ENABLE_ALIGNMENT))) + 
						(separation.scale(Constants.SHEEP_SEPARATION_WEIGHT * int(Constants.ENABLE_SEPARATION))) + 
						(cohesion.scale(Constants.SHEEP_COHESION_WEIGHT * int(Constants.ENABLE_COHESION))) + 
						(boundsInfluence.scale(Constants.SHEEP_BOUNDARY_INFLUENCE_WEIGHT * Constants.ENABLE_BOUNDARIES)))
		#Adds all forces not already added to the velocity and normalize it
		self.targetVelocity += forces
		self.targetVelocity = self.targetVelocity.normalize()

		# Reset the timer
		if self.timer == Constants.SHEEP_WANDER_FRAMERATE:
			self.timer = 0

		super().update(deltaTime, bounds)

	#Draw specific to sheep script
	def draw(self, screen):
		super().draw(screen)

		#Show debug lines showing the neighbors of the sheep
		if Constants.DEBUG_NEIGHBOR_LINES:
			for sheep in self.neighbors:
				pygame.draw.line(screen, (0, 255, 0), (self.center.x, self.center.y), 
                                (sheep.center.x, sheep.center.y), 2)
		#Show debug lines showing the influence the dog has on the sheep
		if (self.position - self.player.position).length() < Constants.MIN_ATTACK_DIST:
			if Constants.DEBUG_DOG_INFLUENCE:
				pygame.draw.line(screen, (0, 0, 255), (self.center.x, self.center.y), 
								   (self.player.center.x, self.player.center.y), 2)

	
