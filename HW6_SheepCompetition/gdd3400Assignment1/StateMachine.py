from Constants import *
from pygame import *
from random import *
from Vector import *
from Agent import *
from Sheep import *
from Dog import *
from Graph import *
from Node import *
from GameState import *

class StateMachine:
	""" Machine that manages the set of states and their transitions """

	def __init__(self, startState):
		""" Initialize the state machine and its start state"""
		self.__currentState = startState
		self.__currentState.enter()

	def getCurrentState(self):
		""" Get the current state """
		return self.__currentState

	def update(self, gameState):
		""" Run the update on the current state and determine if we should transition """
		nextState = self.__currentState.update(gameState)

		# If the nextState that is returned by current state's update is not the same
		# state, then transition to that new state
		if nextState != None and type(nextState) != type(self.__currentState):
			self.transitionTo(nextState)

	def transitionTo(self, nextState):
		""" Transition to the next state """
		self.__currentState.exit()
		self.__currentState = nextState
		self.__currentState.enter()

	def draw(self, screen):
		""" Draw any debugging information associated with the states """
		self.__currentState.draw(screen)

class State:
	def enter(self):
		""" Enter this state, perform any setup required """
		print("Entering " + self.__class__.__name__)
		
	def exit(self):
		""" Exit this state, perform any shutdown or cleanup required """
		print("Exiting " + self.__class__.__name__)

	def update(self, gameState):
		""" Update this state, before leaving update, return the next state """
		print("Updating " + self.__class__.__name__)

	def draw(self, screen):
		""" Draw any debugging info required by this state """
		pass

			   
class HerdSheepState(State):
	""" This is an example state that simply picks the first sheep to target """

	def update(self, gameState):
		""" Update this state using the current gameState """
		super().update(gameState)
		dog = gameState.getDog()

		herd = gameState.getHerd()
		# Exception
		if not herd:
			return Idle()
		#Find the side of the pen entrance that is closest to the dog
		eRect = gameState.getPenBounds()[0]
		entrancePosition = Vector2(eRect.center[0], eRect.center[1])
		if (dog.center.x - eRect.left)**2 < (dog.center.x - eRect.right)**2:
			entrancePosition.x = eRect.left
		else:
			entrancePosition.x = eRect.right

		#Pick furthest sheep
		herd = gameState.getHerd()
		farthestSheep = herd[0]
		farthestCost = -float('inf')
		for sheep in herd:
			#path = gameState.getGraph().findPath_AStar(Vector2(farthestSheep.center.x, farthestSheep.center.y), Vector2(entrancePosition[0], entrancePosition[0]))
			#if(path):
				#newCost = path[-1].cost
			newCost = entrancePosition.distance_to((sheep.center.x, sheep.center.y))
			newCost /= (dog.center - sheep.center).length() + 1
			if farthestCost < newCost:
				farthestCost = newCost
				farthestSheep = sheep

		dog.setTargetSheep(farthestSheep)

		# You could add some logic here to pick which state to go to next
		# depending on the gameState

		
		ctr = dog.getTargetSheep().center
		sheepVec = Vector2(ctr.x, ctr.y)
		#Get vector from center of pen entrance to target sheep location
		targetVector = sheepVec - entrancePosition

		#scale the vector by the radius that results in the sheep to run
		targetVector.scale_to_length(DRIVING_RADIUS)

		#if dog is closer to pen than the sheep
		if entrancePosition.distance_to((farthestSheep.center.x, farthestSheep.center.y)) > entrancePosition.distance_to((dog.center.x, dog.center.y)):
			#use flank vector instead
			targetVector = Vector2(-targetVector.y, targetVector.x)
			targetVector.scale_to_length(DOG_FLANKING_RADIUS)
			targetVector2 = -targetVector
			if (dog.center - (sheepVec + targetVector2)).length() < (dog.center - (sheepVec + targetVector)).length():
				targetVector = targetVector2

		#Get the target location to head to so that the dog herds the sheep to the pen
		targetLoc = sheepVec + targetVector
		#turn the target location into a node
		targetNode = gameState.getGraph().getNodeFromPoint(targetLoc)
		#
		#if targetNode.isWalkable:
		#	dog.calculatePathToNewTarget(targetNode.center)
		#else:
		#	dog.calculatePathToNewTarget(dog.getTargetSheep().center)
		currRadius = targetVector.length()
		while not targetNode.isWalkable:
			#Scale down the target vector
			currRadius = currRadius - GRID_SIZE
			targetVector.scale_to_length(currRadius)
			#calculate target location again
			targetLoc = sheepVec + targetVector
			#find new target node at new location
			targetNode = gameState.getGraph().getNodeFromPoint(targetLoc)
			pass
		dog.calculatePathToNewTarget(targetNode.center)


		return Idle()

class Idle(State):
	""" This is an idle state where the dog does nothing """

	def update(self, gameState):
		super().update(gameState)
		dog = gameState.getDog()
		targetNode = dog.path[-1] if dog.path else None
		targetDist = -float('inf')
		if targetNode:
			targetDist = (dog.center - targetNode.center).length()
		# If sheep exist and we haven't reached our target, find sheep to herd
		if len(gameState.getHerd()) > 0 and targetDist < TARGET_RADIUS:
			return HerdSheepState()
		else:
			return Idle()