import Constants
import Node
import pygame
import Vector

from pygame import *
from Vector import *
from Node import *
from enum import Enum

class SearchType(Enum):
	BREADTH = 0
	DJIKSTRA = 1
	A_STAR = 2
	BEST_FIRST = 3

class Graph():
	def __init__(self):
		""" Initialize the Graph """
		self.nodes = []			# Set of nodes
		self.obstacles = []		# Set of obstacles - used for collision detection

		# Initialize the size of the graph based on the world size
		self.gridWidth = int(Constants.WORLD_WIDTH / Constants.GRID_SIZE)
		self.gridHeight = int(Constants.WORLD_HEIGHT / Constants.GRID_SIZE)

		# Create grid of nodes
		for i in range(self.gridHeight):
			row = []
			for j in range(self.gridWidth):
				node = Node(i, j, Vector(Constants.GRID_SIZE * j, Constants.GRID_SIZE * i), Vector(Constants.GRID_SIZE, Constants.GRID_SIZE))
				row.append(node)
			self.nodes.append(row)

		## Connect to Neighbors
		for i in range(self.gridHeight):
			for j in range(self.gridWidth):
				# Add the top row of neighbors
				if i - 1 >= 0:
					# Add the upper left
					if j - 1 >= 0:		
						self.nodes[i][j].neighbors += [self.nodes[i - 1][j - 1]]
					# Add the upper center
					self.nodes[i][j].neighbors += [self.nodes[i - 1][j]]
					# Add the upper right
					if j + 1 < self.gridWidth:
						self.nodes[i][j].neighbors += [self.nodes[i - 1][j + 1]]

				# Add the center row of neighbors
				# Add the left center
				if j - 1 >= 0:
					self.nodes[i][j].neighbors += [self.nodes[i][j - 1]]
				# Add the right center
				if j + 1 < self.gridWidth:
					self.nodes[i][j].neighbors += [self.nodes[i][j + 1]]
				
				# Add the bottom row of neighbors
				if i + 1 < self.gridHeight:
					# Add the lower left
					if j - 1 >= 0:
						self.nodes[i][j].neighbors += [self.nodes[i + 1][j - 1]]
					# Add the lower center
					self.nodes[i][j].neighbors += [self.nodes[i + 1][j]]
					# Add the lower right
					if j + 1 < self.gridWidth:
						self.nodes[i][j].neighbors += [self.nodes[i + 1][j + 1]]

	def getNodeFromPoint(self, point):
		""" Get the node in the graph that corresponds to a point in the world """
		point.x = max(0, min(point.x, Constants.WORLD_WIDTH - 1))
		point.y = max(0, min(point.y, Constants.WORLD_HEIGHT - 1))

		# Return the node that corresponds to this point
		return self.nodes[int(point.y/Constants.GRID_SIZE)][int(point.x/Constants.GRID_SIZE)]

	def placeObstacle(self, point, color):
		""" Place an obstacle on the graph """
		node = self.getNodeFromPoint(point)

		# If the node is not already an obstacle, make it one
		if node.isWalkable:
			# Indicate that this node cannot be traversed
			node.isWalkable = False		

			# Set a specific color for this obstacle
			node.color = color
			for neighbor in node.neighbors:
				neighbor.neighbors.remove(node)
			node.neighbors = []
			self.obstacles += [node]

	def reset(self):
		""" Reset all the nodes for another search """
		for i in range(self.gridHeight):
			for j in range(self.gridWidth):
				self.nodes[i][j].reset()

	def buildPath(self, endNode):
		""" Go backwards through the graph reconstructing the path """
		path = []
		node = endNode
		while node is not 0:
			node.isPath = True
			path = [node] + path
			node = node.backNode

		# If there are nodes in the path, reset the colors of start/end
		if len(path) > 0:
			path[0].isPath = False
			path[0].isStart = True
			path[-1].isPath = False
			path[-1].isEnd = True
		return path

	def getDistance(self, node1, node2):
		return sqrt((node1.x - node2.x)**2 +(node1.y - node2.y)**2)  

	def findPath_Breadth(self, start, end):
		""" Breadth Search """
		#print("Breadth")
		self.reset()
		#Convert vectors to nodes and set those nodes to isStart and say that the starting node has been visited and isEnd
		startNode = self.getNodeFromPoint(start)
		startNode.isStart = True
		endNode = self.getNodeFromPoint(end)
		endNode.isEnd = True
		#Deque the visit list
		toVisit = [startNode]
		#set the visited set to the start node's set
		visited = set([startNode])
		startNode.costFromStart = 0           #Set start node's cost from start to 0

		#While there are nodes to visit
		while toVisit:
			currentNode = toVisit.popleft()    #FIFO Queue 
			currentNode.isEplored = True   

			#If the current node is the end node, then build a new path
			if currentNode.isEnd:
				return self.buildPath(endNode)

			#for every neighbor next to the current node
			for neighbor in currentNode.neighbors:
				#If the neighbor is not in visited and the neighbor is walkable
				if neighbor not in visited and neighbor.isWalkable:
					#Add the neighbor to the visited list and set it to true
					visited.add(neighbor) 
					neighbor.isVisited = True             
					toVisit.append(neighbor)
					#set the neighbor's cost from start to the current node's cost from start plus 1 and set the neighbor's back node to current node
					neighbor.costFromStart = currentNode.costFromStart + 1
					neighbor.backNode = currentNode
		return []

	def findPath_Djikstra(self, start, end):
		""" Djikstra's Search """
		#print("DJIKSTRA")
		self.reset()
		#Convert vectors to nodes and set those nodes to isStart and say that the starting node has been visited and isEnd
		startNode = self.getNodeFromPoint(start)
		startNode.isStart = True
		startNode.isVisited = True
		endNode = self.getNodeFromPoint(end)
		endNode.isEnd = True

		#set the to visit list to the ones from the start node
		toVisit = [startNode]              
		startNode.costFromStart = 0 #Set the original cost from start to 0

		#While there are nodes to visit
		while toVisit:
			toVisit.sort(key = lambda node:node.costFromStart)  #sort by cost from start
			currentNode = toVisit.pop(0)
			currentNode.isExplored = True 

			#If the current node is the end node, then build a new path
			if currentNode.isEnd:
				return self.buildPath(endNode)

			#for every neighbor next to the current node
			for neighbor in currentNode.neighbors:
				#get new cost based on cost from start and the distance between current node and the neighbor node
				newCost = currentNode.costFromStart + self.getDistance(currentNode, neighbor)
				#If the neighbor is walkable, and not explored yet, and the new cost is less than the neighbor's cost from start
				if neighbor.isWalkable and not neighbor.isExplored and newCost < neighbor.costFromStart:
					#set neighbor's cost from start to be the new cost and set the neighbor's back node to be the current node
					neighbor.costFromStart = newCost
					neighbor.backNode = currentNode
					#If the neighbor isn't visited, add it to the toVisit list and set it to true
					if not neighbor.isVisited:
						toVisit.append(neighbor)
						neighbor.isVisited = True
		return []

	def findPath_AStar(self, start, end):
		""" A Star Search """
		#print("A_STAR")
		self.reset()
		#Convert vectors to nodes and set those nodes to isStart and say that the starting node has been visited and isEnd
		startNode = self.getNodeFromPoint(start)
		startNode.isStart = True
		startNode.isVisited = True
		endNode = self.getNodeFromPoint(end)
		endNode.isEnd = True 

		toVisit = [startNode]
		startNode.costFromStart = 0 #Set the original cost from start to 0
		startNode.costToEnd = self.getDistance(startNode,endNode) #set the cost to end to be based on the distance between start and end
		startNode.cost = startNode.costFromStart + startNode.costToEnd #set the total cost to both combined

		#While there are nodes to visit
		while toVisit:
			toVisit.sort(key = lambda n:n.cost)  #Sort by total cost
			currentNode = toVisit.pop(0)
			currentNode.isExplored = True

			#If the current node is the end node, then build a new path
			if currentNode.isEnd:
				return self.buildPath(endNode)

			#for every neighbor next to the current node
			for neighbor in currentNode.neighbors:
				#If the neighbor is walkable and we haven't explored it
				if neighbor.isWalkable and not neighbor.isExplored:
					#Get a new cost from start by getting original cost plus the distance between current node and neighbor
					newCostFromStart = currentNode.costFromStart + self.getDistance(currentNode, neighbor)
					#if the new cost is less than the neighbor's cost from start
					if(newCostFromStart < neighbor.costFromStart):
						#neighbor's cost from start is now the new cost from start and the neighbor's back node is the current node
						neighbor.costFromStart = newCostFromStart
						neighbor.backNode = currentNode
						#If we haven't visited the neighbor
						if not neighbor.isVisited:
							#set it to visited, and set cost to end from neighbor to end node and add the neighbor to visit
							neighbor.isVisited = True
							neighbor.costToEnd = self.getDistance(neighbor, endNode)
							toVisit.append(neighbor)
						#set the neighbor's total cost to the neighbor's cost from start and to end
						neighbor.cost = neighbor.costFromStart + neighbor.costToEnd
		return []

	def findPath_BestFirst(self, start, end):
		""" Best First Search """
		#print("BEST_FIRST")
		self.reset()
		#Convert vectors to nodes and set those nodes to isStart and say that the starting node has been visited and isEnd
		startNode = self.getNodeFromPoint(start)
		startNode.isStart = True
		startNode.isVisited = True
		endNode = self.getNodeFromPoint(end)
		endNode.isEnd = True 

		toVisit = [startNode]
		startNode.costToEnd = self.getDistance(startNode,endNode) #set the cost to end to be based on the distance between start and end

		#While there are nodes to visit
		while toVisit:
			toVisit.sort(key = lambda n:n.costToEnd) #Sort by total cost to reach the end
			currentNode = toVisit.pop(0)
			currentNode.isExplored = True

			#If the current node is the end node, then build a new path
			if currentNode.isEnd:
				return self.buildPath(endNode)
			#for every neighbor next to the current node
			for neighbor in currentNode.neighbors:
				#If the node can be walked on, and haven't visited it
				if neighbor.isWalkable and not neighbor.isVisited:
					#Set the current node to the back node, set the neighbor visiting to true, and get new cost to end
					neighbor.backNode = currentNode
					neighbor.isVisited = True
					neighbor.costToEnd = self.getDistance(neighbor, endNode)
					toVisit.append(neighbor)
		return []

	def draw(self, screen):
		""" Draw the graph """
		for i in range(self.gridHeight):
			for j in range(self.gridWidth):
				self.nodes[i][j].draw(screen)