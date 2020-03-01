'''
	Reynald Servera
	40043437
	COMP-472
	Project 1 - Indonesian Dot Puzzle
	February 6th, 2020
'''

import copy # used for the deepcopy function
import sys # used to increase the recursion limit

# Function that optimally displays the puzzle
def showPuzzle(puzzle):
	puzzleDimension = len(puzzle) # get dimension of the puzzle

	for x in range(puzzleDimension):
		print(puzzle[x])

# Function that creates the shape of a puzzle of a specific dimension, and fill it with zeroes
def makePuzzleShape(dimension):
	puzzleShape = [] # create an empty list

	for x in range(dimension):
		puzzleShape.append([]) # create rows
		for y in range(dimension):
			puzzleShape[x].append(0) # fill every collumn with zeroes

	return puzzleShape

# Populates a puzzle shape with a given setup
def loadPuzzle(puzzleShape, puzzleState):
	puzzleDimension = len(puzzleShape) # get dimension of the puzzle
	puzzleIndex = 0 # keeps track of index in the puzzle

	# Check if given puzzle state is valid for the puzzle shape
	if(len(puzzleState) != puzzleDimension**2):
		return "Invalid Puzzle State!"

	for x in range(puzzleDimension):
		for y in range(puzzleDimension):
			puzzleShape[x][y] = puzzleState[puzzleIndex] # cast the puzzleState into a string to access each digit by index, and cast back to int when entered in the puzzle
			puzzleIndex += 1

	return puzzleShape

def flip(originalPuzzle, index):

	puzzle = copy.deepcopy(originalPuzzle)
	puzzleDimension = len(puzzle) # get dimension of the puzzle

	row = 1
	collumn = 1

	# find out which row the index is in
	while index > row * puzzleDimension:
		row += 1

	# find out which collumn the index is in
	while index > (row - 1) * puzzleDimension + collumn:
		collumn += 1

	# list that will hold all the tokens to be flipped
	indexesToChange = [index]

	# find the token(s) above and below the token at index
	if row == 1:
		indexesToChange.append(index + puzzleDimension)
	elif row == puzzleDimension:
		indexesToChange.append(index - puzzleDimension)
	else:
		indexesToChange.append(index + puzzleDimension)
		indexesToChange.append(index - puzzleDimension)

	# find the token(s) to the left and to the right of the token at index
	if collumn == 1:
		indexesToChange.append(index + 1)
	elif collumn == puzzleDimension:
		indexesToChange.append(index - 1)
	else:
		indexesToChange.append(index + 1)
		indexesToChange.append(index - 1)

	indexesToChange.sort() # sort the indexes to be changed in ascending order

	currentIndex = 0

	# flip all tokens at the indexes listed in indexesToChange
	for x in range(puzzleDimension):
		for y in range(puzzleDimension):
			if(len(indexesToChange) != 0):
				if currentIndex == indexesToChange[0] - 1:
					if puzzle[x][y] == '0':
						puzzle[x][y] = '1'
					else:
						puzzle[x][y] = '0'
					indexesToChange.pop(0)
			currentIndex += 1
	return puzzle

# test if puzzle is equal to the goal state (all zeroes)
def testPuzzle(puzzle):
	puzzleDimension = len(puzzle)

	for x in range(puzzleDimension):
		for y in range(puzzleDimension):
			if puzzle[x][y] == '1':
				return False

	return True

# converts the puzzle from list[n][n] form to string form
def puzzleToString(puzzle):
	puzzleDimension = len(puzzle)
	puzzleAsString = ''

	for x in range(puzzleDimension):
		for y in range(puzzleDimension):
			puzzleAsString += puzzle[x][y]

	return puzzleAsString

# a Vertex object will represent a node in the state space
class Vertex:
	def __init__(self, i, p):
		self.index = i # index of the vertex
		self.neighbors = [] # list of neighboring vertices
		self.state = 1 # state of the vertex (1 = open, 2 = closed)
		self.puzzle = copy.deepcopy(p) # puzzle state of the vertex
		self.depthLevel = 1 # depth level of the vertex in the graph
		self.BFS_info = [None, None] # list that will hold the heuristic information of the vertex. [0] = number of 0s, [1] = first occurance of a 0
		self.parent = None # parent vertex
		self.lastMove = None # last move played to reach this vertex

	# adds another vertex as the current one's neighbor
	def add_neighbor(self, neighborIndex):
		neighborSet = set(self.neighbors)
		if neighborIndex not in neighborSet:
			self.neighbors.append(neighborIndex)
			self.neighbors.sort()

	# adds another vertex as teh current one's parent
	def add_parent(self, parentVertex):
		self.parent = parentVertex

# a Graph object will represent the state space that contains nodes (vertices)
class Graph:
	def __init__(self):
		self.vertices = {} # whole dictionary of vertices where the keys are their respective indexes
		self.depthLevel = 1 # current level of the search algorithm
		self.solution = False # boolean that keeps track whether a solution is found
		self.solutionPath = [] # list that will contain the path to the solution once it is found
		self.openList = [] # list of open nodes
		self.closedList = [] # list of closed nodes
		self.current_l = 0 # current search length

	# adds a vertex to the graph
	def add_vertex(self, vertex):
		if isinstance(vertex, Vertex) and vertex.index not in self.vertices: # checks if object passed in is a vertex object and if it is not already in
			self.vertices[vertex.index] = vertex
			return True
		else:
			return False
	# adds an edge between vertices
	def add_edge(self, u, v):
		if u in self.vertices: # check if these vertices exist in the graph
			for key, actualVertex in self.vertices.items():
				if key == u:
					actualVertex.add_neighbor(v)
			return True
		else:
			return False

	# displays all the items in vertices along with their neighbors
	def print_graph(self):
		for key in sorted(list(self.vertices.keys())):
			print(str(key) + str(self.vertices[key].neighbors) + " STATE: " +str(self.vertices[key].state))

	# Depth-First Search
	def DFS(self, vertex, maxDepth, puzzleNumber):
		print(vertex.index) # print current vertex that is being searched
		if not self.solution:				
			puzzleDimension = len(vertex.puzzle)
			self.depthLevel += 1
			if self.depthLevel <= maxDepth:
				# create children nodes of the current node where x is the dimension of the puzzle squared
				for x in range(1, puzzleDimension**2 + 1):
					self.add_vertex(Vertex(len(self.vertices), flip(vertex.puzzle, x)))
					self.add_edge(vertex.index, len(self.vertices) - 1)	

					# check neighboring nodes
					for v in vertex.neighbors:
						# if the nodes are open then
						if self.vertices[v].state == 1:
							# recursively call the DFS function
							self.DFS(self.vertices[v], maxDepth, puzzleNumber)
							# if a solution is found, stop searching
							if self.solution:
								self.solutionPath.append(x)	
								break
					if self.solution:
						break		

			self.depthLevel -= 1
			vertex.state = 0

			if testPuzzle(vertex.puzzle):
				self.solution = True

			with open(str(puzzleNumber) + '_dfs_search.txt', 'a') as f:
				print(str(puzzleNumber) + ' 0 0 0 ' + puzzleToString(vertex.puzzle) + ' - Node: ' +  str(vertex.index), file = f)

	# BFS's heuristic function that returns firstly, the first occurence of 0 (if there is one) then the amount of 0's currently on the puzzle board 
	def BFS_h_0(self, currentPuzzle):
		resultList = [0, 0]
		zeroCounter = 0
		positionCounter = 0
		puzzleDimension = len(currentPuzzle)

		for x in range(puzzleDimension):
			for y in range(puzzleDimension):
				if resultList[1] == None and currentPuzzle[x][y] == '0':
					resultList[1] = positionCounter
				if currentPuzzle[x][y] == '0':
					zeroCounter += 1
				positionCounter += 1

		resultList[0] = zeroCounter
		return resultList

	# BFS's heuristic function that returns firstly, the first occurence of 1 (if there is one) then the amount of 1's currently on the puzzle board 
	def BFS_h_1(self, currentPuzzle):

		resultList = [0, 0]
		oneCounter = 0
		positionCounter = 0

		puzzleDimension = len(currentPuzzle)

		for x in range(puzzleDimension):
			for y in range(puzzleDimension):
				if resultList[1] == None and currentPuzzle[x][y] == '1':
					resultList[1] = positionCounter
				if currentPuzzle[x][y] == '1':
					oneCounter += 1
				positionCounter += 1

		resultList[0] = oneCounter

		return resultList

	# function used to insert vertices in the open list. 
	# vertices with a higher value returned by the heuristic functions will be prioritized at the start of the list
	def BFS_addToOpenList(self, currentVertex):
		if len(self.openList) == 0:
			self.openList.append(currentVertex)
		else:
			inserted = False
			currentPosition = 0
			for x in range (len(self.openList)):
				if currentVertex.BFS_info[0] < self.openList[x].BFS_info[0]: 
					currentPosition += 1
				elif currentVertex.BFS_info[0] == self.openList[x].BFS_info[0]:
					if currentVertex.BFS_info[1] >= self.openList[x].BFS_info[1]:
						currentPosition += 1 
					else:
						self.openList.insert(currentPosition, currentVertex)
						inserted = True
						break
				elif (currentVertex.BFS_info[0] > self.openList[x].BFS_info[0]):
					self.openList.insert(currentPosition, currentVertex)
					inserted = True
					break
			if not inserted:
				self.openList.insert(currentPosition, currentVertex)

	# add up all the sequence of last moves from a vertex into the solution path list
	def BFS_pathToRoot(self, vertex):
		currentVertex = vertex
		while currentVertex != None:
			if currentVertex.lastMove != None:
				self.solutionPath.append(currentVertex.lastMove)	
			currentVertex = currentVertex.parent

	# BFS function, where heuristicInt represents which heuristic function to use. 0 for most # of zeroes and 1 for most # of ones
	def BFS(self, vertex, max_l, puzzleNumber, heuristicInt):
		puzzleDimension = len(vertex.puzzle)
		self.depthLevel = vertex.depthLevel

		# for the first node in the state space
		if len(self.openList) == 0 and len(self.closedList) == 0:
			if heuristicInt == 0:
				vertex.BFS_info = self.BFS_h_0(vertex.puzzle)
			else:
				vertex.BFS_info = self.BFS_h_1(vertex.puzzle)
			self.BFS_addToOpenList(vertex)
			self.current_l += 1
		# for nodes after the first, while a solution is not found
		elif self.current_l < max_l and not self.solution:
			# create puzzleDimension^2 children from the current node
			for y in range(1, puzzleDimension**2 + 1):
				if self.current_l >= max_l:
					break
				self.add_vertex(Vertex(len(self.vertices), flip(vertex.puzzle, y))) # create a children vertex in the graph
				self.add_edge(vertex.index, vertex.index + y) # add an edge between them and the current vertex (parent)
				self.vertices[len(self.vertices) - 1].parent = vertex # mark the current as the new node's parent
				self.vertices[len(self.vertices) - 1].lastMove = y # mark the last move performed to get to this state

				# fill in the heuristic info of each vertex (BFS_info) depending on which the heuristic function used
				if heuristicInt == 0:
					self.vertices[len(self.vertices) - 1].BFS_info = self.BFS_h_0(self.vertices[len(self.vertices) - 1].puzzle)
				else:
					self.vertices[len(self.vertices) - 1].BFS_info = self.BFS_h_1(self.vertices[len(self.vertices) - 1].puzzle)

				self.vertices[len(self.vertices) - 1].depthLevel = self.depthLevel + 1 # mark the new vertex's depth level
				self.BFS_addToOpenList(self.vertices[len(self.vertices) - 1]) # add the new children to the open list
				self.current_l += 1 # increment the search length

		if len(self.openList) != 0:
			print(len(self.openList)) # show the number of nodes left to search
			# log the current node that is being searched
			with open(str(puzzleNumber) + '_bfs_search.txt', 'a') as fi:
				print(str(puzzleNumber) + ' ' + str(self.openList[0].BFS_info[0]) + ' 0 ' + str(self.openList[0].BFS_info[0]) + ' ' + puzzleToString(self.openList[0].puzzle) + ' - Node: ' +  str(self.openList[0].index), file = fi)
			if testPuzzle(self.openList[0].puzzle):
				print("Solution Found!")
				self.solution = True
				self.BFS_pathToRoot(self.openList[0])
				return self.openList[0].index
			else:
				self.closedList.append(self.openList.pop(0))
				# tail recursion call on the first vertex in the open list (highest heuristic value)
				self.BFS(self.closedList[len(self.closedList) - 1], max_l, puzzleNumber, heuristicInt)

	# A* function, where heuristicInt represents which heuristic function to use. 0 for most # of zeroes and 1 for most # of ones
	def aStar(self, vertex, max_l, puzzleNumber, heuristicInt):
		puzzleDimension = len(vertex.puzzle)
		self.depthLevel = vertex.depthLevel

		# for the first node in the state space
		if len(self.openList) == 0 and len(self.closedList) == 0:
			if heuristicInt == 0:
				vertex.BFS_info = self.BFS_h_0(vertex.puzzle)
			else:
				vertex.BFS_info = self.BFS_h_1(vertex.puzzle)
			self.BFS_addToOpenList(vertex)
			self.current_l += 1
		# for nodes after the first, while a solution is not found
		elif self.current_l < max_l and not self.solution:
			# create puzzleDimension^2 children from the current node
			for y in range(1, puzzleDimension**2 + 1):
				if self.current_l >= max_l:
					break				
				self.add_vertex(Vertex(len(self.vertices), flip(vertex.puzzle, y))) # create a children vertex in the graph
				self.add_edge(vertex.index, vertex.index + y) # add an edge between them and the current vertex (parent)
				self.vertices[len(self.vertices) - 1].parent = vertex # mark the current as the new node's parent	
				self.vertices[len(self.vertices) - 1].lastMove = y # mark the last move performed to get to this state
				
				# fill in the heuristic info of each vertex (BFS_info) depending on which the heuristic function used
				if heuristicInt == 0:
					self.vertices[len(self.vertices) - 1].BFS_info = self.BFS_h_0(self.vertices[len(self.vertices) - 1].puzzle)
				else:
					self.vertices[len(self.vertices) - 1].BFS_info = self.BFS_h_1(self.vertices[len(self.vertices) - 1].puzzle)

				self.vertices[len(self.vertices) - 1].depthLevel = self.depthLevel + 1 # mark the new vertex's depth level
				
				# substract the depth level of the vertex from its heuristic value (BFS_info[0])
				self.vertices[len(self.vertices) - 1].BFS_info[0] -= self.vertices[len(self.vertices) - 1].depthLevel
	
				self.BFS_addToOpenList(self.vertices[len(self.vertices) - 1]) # add the new children to the open list
				self.current_l += 1 # increment the search length

		if len(self.openList) != 0:
			print(len(self.openList)) # show the number of nodes left to search
			# log the current node that is being searched
			with open(str(puzzleNumber) + '_aStar_search.txt', 'a') as fi:
				print(str(puzzleNumber) + ' ' + str(self.openList[0].BFS_info[0] - self.openList[0].depthLevel) + ' ' + str(self.openList[0].depthLevel) + ' ' + str(self.openList[0].BFS_info[0]) + ' ' + puzzleToString(self.openList[0].puzzle) + ' - Node: ' +  str(self.openList[0].index), file = fi)
			
			if testPuzzle(self.openList[0].puzzle):
				print("Solution Found!")
				self.solution = True
				self.BFS_pathToRoot(self.openList[0])
				return self.openList[0].index
			else:
				self.closedList.append(self.openList.pop(0))
				# tail recursion call on the first vertex in the open list (highest heuristic value)
				self.aStar(self.closedList[len(self.closedList) - 1], max_l, puzzleNumber, heuristicInt)				

# converts index to a letter/number combination (for the output file)
def indexToLetterNumber(index, dimension):
	row = 1
	collumn = 1

	# find out which row the index is in
	while index > row * dimension:
		row += 1

	# find out which collumn the index is in
	while index > (row - 1) * dimension + collumn:
		collumn += 1

	rowLetter = {1:'A', 2:'B', 3:'C', 4:'D', 5:'E', 6:'F', 7:'G', 8:'H', 9:'I', 10:'J' }

	return rowLetter.get(row, "Invalid row!") + str(collumn)

# run the the DFS function on the input file
def idp_DFS(path, fileName):
	p = path # path to the folder with input files
	f = fileName + '.txt' # the name of input file
	fullPath = p + f # full path

	puzzleNumber = 0
	puzzleSize = 0
	maxDepth = 0
	maxSPL = 0
	initialPuzzle = 0

	counter = 0

	# read the input file
	with open(fullPath) as f:
		# split every number in a line
		for line in f:
			for word in line.split():
				if counter == 0:
					puzzleSize = word
					counter += 1 
				elif counter == 1:
					maxDepth = word
					counter += 1
				elif counter == 2:
					maxSPL = word
					counter += 1
				else:
					initialPuzzle = word
					counter = 0	
			# write the output of the algorithm into a solution text file
			with open(str(puzzleNumber) + '_dfs_solution.txt', 'w') as f:
				print(str(puzzleNumber) + ' ' + str(initialPuzzle), file = f)

				puzzleShape = makePuzzleShape(int(puzzleSize))
				loadedPuzzle = loadPuzzle(puzzleShape, str(initialPuzzle)) 

				# create a graph that will hold vertices
				g = Graph()

				# initial node in the graph
				g.add_vertex(Vertex(0, loadedPuzzle))

				# create an initial text file that will keep track of the searches
				with open(str(puzzleNumber) + '_dfs_search.txt', 'w') as searchFile:
					g.DFS(g.vertices[0], int(maxDepth), puzzleNumber) # recursive DFS function

				# create an appropriate matrix for the puzzle
				puzzleShape = makePuzzleShape(int(puzzleSize))
				# load the puzzle into the matrix
				loadedPuzzle = loadPuzzle(puzzleShape, str(initialPuzzle))

				# a reverse is needed to show the solution path in order
				g.solutionPath.reverse()

				for x in range(len(g.solutionPath)):
					loadedPuzzle = flip(loadedPuzzle, g.solutionPath[x])
					print(indexToLetterNumber(g.solutionPath[x], int(puzzleSize)) + ' ' + puzzleToString(loadedPuzzle), file = f)

				if len(g.solutionPath) == 0:
					print('No solution!', file = f)

			puzzleNumber += 1

# run the the BFS function on the input file with heuristic function 0
def idp_BFS_0(path, fileName):
	p = path # path to the folder with input files
	f = fileName + '.txt' # the name of input file
	fullPath = p + f # full path

	puzzleNumber = 0
	puzzleSize = 0
	maxDepth = 0
	maxSPL = 0
	initialPuzzle = 0

	counter = 0

	# read the input file
	with open(fullPath) as f:
		# split every number in a line
		for line in f:
			for word in line.split():
				if counter == 0:
					puzzleSize = word
					counter += 1 
				elif counter == 1:
					maxDepth = word
					counter += 1
				elif counter == 2:
					maxSPL = word
					counter += 1
				else:
					initialPuzzle = word
					counter = 0	
			# write the output of the algorithm into a solution text file
			with open(str(puzzleNumber) + '_bfs_solution.txt', 'w') as f:
				print(str(puzzleNumber) + ' ' + str(initialPuzzle), file = f)

				puzzleShape = makePuzzleShape(int(puzzleSize))
				loadedPuzzle = loadPuzzle(puzzleShape, str(initialPuzzle)) 

				# create a graph that will hold vertices
				g = Graph()

				# initial node in the graph
				g.add_vertex(Vertex(0, loadedPuzzle))

				# create an initial text file that will keep track of the searches
				with open(str(puzzleNumber) + '_bfs_search.txt', 'w') as searchFile:
					g.BFS(g.vertices[0], int(maxSPL), puzzleNumber, 0) # recursive DFS function

				# create an appropriate matrix for the puzzle
				puzzleShape = makePuzzleShape(int(puzzleSize))
				# load the puzzle into the matrix
				loadedPuzzle = loadPuzzle(puzzleShape, str(initialPuzzle))

				# a reverse is needed to show the solution path in order
				g.solutionPath.reverse()
				print(len(g.solutionPath))

				for x in range(len(g.solutionPath)):
					print(g.solutionPath[x])

				for x in range(len(g.solutionPath)):
					loadedPuzzle = flip(loadedPuzzle, g.solutionPath[x])
					print(indexToLetterNumber(g.solutionPath[x], int(puzzleSize)) + ' ' + puzzleToString(loadedPuzzle), file = f)

				if len(g.solutionPath) == 0:
					print('No solution!', file = f)

			puzzleNumber += 1

# run the the BFS function on the input file with heuristic function 1
def idp_BFS_1(path, fileName):
	p = path # path to the folder with input files
	f = fileName + '.txt' # the name of input file
	fullPath = p + f # full path

	puzzleNumber = 0
	puzzleSize = 0
	maxDepth = 0
	maxSPL = 0
	initialPuzzle = 0

	counter = 0

	# read the input file
	with open(fullPath) as f:
		# split every number in a line
		for line in f:
			for word in line.split():
				if counter == 0:
					puzzleSize = word
					counter += 1 
				elif counter == 1:
					maxDepth = word
					counter += 1
				elif counter == 2:
					maxSPL = word
					counter += 1
				else:
					initialPuzzle = word
					counter = 0	
			# write the output of the algorithm into a solution text file
			with open(str(puzzleNumber) + '_bfs_solution.txt', 'w') as f:
				print(str(puzzleNumber) + ' ' + str(initialPuzzle), file = f)

				puzzleShape = makePuzzleShape(int(puzzleSize))
				loadedPuzzle = loadPuzzle(puzzleShape, str(initialPuzzle)) 

				# create a graph that will hold vertices
				g = Graph()

				# initial node in the graph
				g.add_vertex(Vertex(0, loadedPuzzle))

				# create an initial text file that will keep track of the searches
				with open(str(puzzleNumber) + '_bfs_search.txt', 'w') as searchFile:
					g.BFS(g.vertices[0], int(maxSPL), puzzleNumber, 1) # recursive DFS function

				# create an appropriate matrix for the puzzle
				puzzleShape = makePuzzleShape(int(puzzleSize))
				# load the puzzle into the matrix
				loadedPuzzle = loadPuzzle(puzzleShape, str(initialPuzzle))

				# a reverse is needed to show the solution path in order
				g.solutionPath.reverse()
				print(len(g.solutionPath))

				for x in range(len(g.solutionPath)):
					print(g.solutionPath[x])

				for x in range(len(g.solutionPath)):
					loadedPuzzle = flip(loadedPuzzle, g.solutionPath[x])
					print(indexToLetterNumber(g.solutionPath[x], int(puzzleSize)) + ' ' + puzzleToString(loadedPuzzle), file = f)

				if len(g.solutionPath) == 0:
					print('No solution!', file = f)

			puzzleNumber += 1

# run the the A* function on the input file with heuristic function 0
def idp_aStar(path, fileName):
	p = path # path to the folder with input files
	f = fileName + '.txt' # the name of input file
	fullPath = p + f # full path

	puzzleNumber = 0
	puzzleSize = 0
	maxDepth = 0
	maxSPL = 0
	initialPuzzle = 0

	counter = 0

	# read the input file
	with open(fullPath) as f:
		# split every number in a line
		for line in f:
			for word in line.split():
				if counter == 0:
					puzzleSize = word
					counter += 1 
				elif counter == 1:
					maxDepth = word
					counter += 1
				elif counter == 2:
					maxSPL = word
					counter += 1
				else:
					initialPuzzle = word
					counter = 0	
			# write the output of the algorithm into a solution text file
			with open(str(puzzleNumber) + '_aStar_solution.txt', 'w') as f:
				print(str(puzzleNumber) + ' ' + str(initialPuzzle), file = f)

				puzzleShape = makePuzzleShape(int(puzzleSize))
				loadedPuzzle = loadPuzzle(puzzleShape, str(initialPuzzle)) 

				# create a graph that will hold vertices
				g = Graph()

				# initial node in the graph
				g.add_vertex(Vertex(0, loadedPuzzle))

				# create an initial text file that will keep track of the searches
				with open(str(puzzleNumber) + '_aStar_search.txt', 'w') as searchFile:
					g.aStar(g.vertices[0], int(maxSPL), puzzleNumber, 0) # recursive DFS function

				# create an appropriate matrix for the puzzle
				puzzleShape = makePuzzleShape(int(puzzleSize))
				# load the puzzle into the matrix
				loadedPuzzle = loadPuzzle(puzzleShape, str(initialPuzzle))

				# a reverse is needed to show the solution path in order
				g.solutionPath.reverse()
				print(len(g.solutionPath))

				for x in range(len(g.solutionPath)):
					print(g.solutionPath[x])

				for x in range(len(g.solutionPath)):
					loadedPuzzle = flip(loadedPuzzle, g.solutionPath[x])
					print(indexToLetterNumber(g.solutionPath[x], int(puzzleSize)) + ' ' + puzzleToString(loadedPuzzle), file = f)

				if len(g.solutionPath) == 0:
					print('No solution!', file = f)

			puzzleNumber += 1			


# main

sys.setrecursionlimit(10000)
idp_DFS('./','test')
idp_BFS_0('./','test')
idp_aStar('./','test')
