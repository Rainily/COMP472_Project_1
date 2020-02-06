# Reynald Servera
# 40043437
# COMP-472
# Project 1 - Indonesian Dot Puzzle
# February 6th, 2020

path = 'C:/Users/Rainily/Desktop/Concordia/COMP-472/COMP472_Project_1/SampleFiles/'
inputFileName = 'test.txt'
fullPath = path + inputFileName

puzzleSize = 0
maxDepth = 0
maxSPL = 0
initialPuzzle = 0

counter = 0
with open(fullPath) as f:
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
		print(puzzleSize)
		print(maxDepth)
		print(maxSPL)
		print(initialPuzzle)

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
	if(len(str(puzzleState)) != puzzleDimension**2):
		return "Invalid Puzzle State!"

	for x in range(puzzleDimension):
		for y in range(puzzleDimension):
			puzzleShape[x][y] = int(str(puzzleState)[puzzleIndex]) # cast the puzzleState into a string to access each digit by index, and cast back to int when entered in the puzzle
			puzzleIndex += 1

	return puzzleShape

def flip(puzzle, index):
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
					if puzzle[x][y] == 0:
						puzzle[x][y] = 1
					else:
						puzzle[x][y] = 0
					indexesToChange.pop(0)
			currentIndex += 1


#def DFS(puzzle, max_d):
#	currentPath = []
#	currentPuzzleState = flip(puzzle, 0)

b = makePuzzleShape(3)
print(b)
print()
c = loadPuzzle(b, 111111111)
print(c)
print()
showPuzzle(c)
flip(c, 3)
print()
showPuzzle(c)