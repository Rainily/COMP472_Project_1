'''
	Reynald Servera
	40043437
	COMP-472
	Project 1 - Indonesian Dot Puzzle
	February 6th, 2020
'''
import copy

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

def testPuzzle(puzzle):
	puzzleDimension = len(puzzle)
	for x in range(puzzleDimension):
		for y in range(puzzleDimension):
			if puzzle[x][y] == '1':
				return False
	return True

def puzzleToString(puzzle):
	puzzleDimension = len(puzzle)
	puzzleAsString = ''
	for x in range(puzzleDimension):
		for y in range(puzzleDimension):
			puzzleAsString += puzzle[x][y]
	return puzzleAsString

class Vertex:
	def __init__(self, i, p):
		self.index = i
		self.neighbors = []
		self.state = 1
		self.puzzle = copy.deepcopy(p)

		# states: 0 = closed, 1 = open, 3 = ongoing 

	def add_neighbor(self, neighborIndex):
		neighborSet = set(self.neighbors)
		if neighborIndex not in neighborSet:
			self.neighbors.append(neighborIndex)
			self.neighbors.sort()

class Graph:

	def __init__(self):
		self.vertices = {}
		self.depthLevel = 0
		self.solution = False
		self.solutionPath = []

	def add_vertex(self, vertex):
		if isinstance(vertex, Vertex) and vertex.index not in self.vertices: # checks if object passed in is a vertex object and if it is not already in
			self.vertices[vertex.index] = vertex
			return True
		else:
			return False

	def add_edge(self, u, v):
		if u in self.vertices: # check if these vertices exist in the graph
			for key, actualVertex in self.vertices.items():
				if key == u:
					actualVertex.add_neighbor(v)
			return True
		else:
			return False

	def print_graph(self):
		for key in sorted(list(self.vertices.keys())):
			print(str(key) + str(self.vertices[key].neighbors) + " STATE: " +str(self.vertices[key].state))

	def DFS(self, vertex, maxDepth, puzzleNumber):
		print(vertex.index)
		if not self.solution:				
			puzzleDimension = len(vertex.puzzle)
			self.depthLevel += 1
			if self.depthLevel < maxDepth:
				for x in range(1, puzzleDimension**2 + 1):
					self.add_vertex(Vertex(len(self.vertices), flip(vertex.puzzle, x)))
					self.add_edge(vertex.index, len(self.vertices) - 1)			
					for v in vertex.neighbors:
						if self.vertices[v].state == 1:
							self.DFS(self.vertices[v], maxDepth, puzzleNumber)
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
				print(str(puzzleNumber) + ' 0 0 0 ' + puzzleToString(vertex.puzzle), file = f)			

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

	rowLetter = {1:'A', 2:'B', 3:'C', 4:'DA', 5:'E', 6:'F', 7:'G', 8:'H', 9:'I', 10:'J' }

	return rowLetter.get(row, "Invalid row!") + str(collumn)

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

idp_DFS('C:/Users/Rainily/Desktop/Concordia/COMP-472/COMP472_Project_1/SampleFiles/','rey_test_file_DFS_0')