import sys
import numpy as np

class Mine:
	def __init__(self, loc, d):
		self.location = loc
		self.depth = d

class MinefieldRun:

	def __init__(self, flist):

		#Initialize patterns and directions
		self.patterns = {
		'alpha': np.array([[-1,-1],[-1,1],[1,-1],[1,1]]), 
		'beta': np.array([[-1,0],[0,-1],[0,1],[1,0]]), 
		'gamma': np.array([[-1,0],[0,0],[1,0]]), 
		'delta': np.array([[0,-1],[0,0],[0,1]])
		}
		self.directions = {'north': np.array([0, -1]), 
		'south': np.array([0, 1]), 
		'east': np.array([1, 0]), 
		'west': np.array([-1, 0])}

		#Other various parameters
		self.movePenalty = 0
		self.shotPenalty = 0
		self.finished = False
		self.success = False
		self.stepsRun = 0

		#Find center of grid
		center = np.array([int(len(flist[0])/2), int(len(flist)/2)])
		
		#Find mines and keep their locations relative to the center of the grid
		#x and y indexing is reversed because of the grid vs. matrix representations
		self.mines = []
		for y in range(0, len(flist)):
			for x in range(0, len(flist[y])):
					if(flist[y][x] is not '.'):
						#An integer value for the depth is obtained using the integer value of the ASCII character, with some modular arithmetic
						self.mines.append(Mine(np.array([x, y]-center),(ord(flist[y][x])-38)%58 ))

		
		self.initialMines = len(self.mines)
		

	def moveShip(self, dir):

		#Subtract the movement vector from the relative locations of all mines
		for m in self.mines:
			m.location-=self.directions[dir]

		#Update move penalty
		self.movePenalty = min(self.initialMines*3, self.movePenalty+2)


	def fire(self, patt):

		#Obtain relative locations of torpedoes for given pattern
		relLocs = self.patterns[patt]

		toRemove = []
		#If any of these locations match with the relative locations of a mine, mark mine to be removed
		#so as not to alter a list while iterating through it
		for m in self.mines:
			for r in relLocs:
				if(m.location==r).all():
					toRemove.append(m)

		for i in toRemove:
			self.mines.remove(i)

		#Update shot penalty
		self.shotPenalty = min(self.initialMines*5, self.shotPenalty+5)


	def runLine(self, comms):

		if(not self.finished):
		#If both a firing pattern and directional move are present:
			if(len(comms)==2):
				self.fire(comms[0])
				self.moveShip(comms[1])
			#If there is a single command, find out which type it is and execute
			elif(len(comms)==1):
				if(comms[0] in self.patterns.keys()):
					self.fire(comms[0])
				elif(comms[0] in self.directions.keys()):
					self.moveShip(comms[0])

			#No matter what, descend 1 unit, check for passing a mine
			for m in self.mines:
				m.depth-=1
				if(m.depth<=0):
					self.finished = True
					self.success = False

			#If all mines are gone, success
			if(len(self.mines)==0):
				self.finished = True
				self.success = True

			self.stepsRun+=1


	def depthToLetter(self, d):
		#Simply converts a depth value, d, to it's letter representation for printing

		if(1<=d<=26):
			return chr(d+96)
		elif(27<=d<=52):
			return chr(d+38)
		elif(d<=0):
			#Use a * to represent a mine that has been 'passed'
			return '*'

	def getFieldString(self):
		#Finds the smallest representation of the grid that includes all current mines and has
		#the ship in the center, returns a string of this

		maxX = 0
		maxY = 0

		#Find max x and y deltas, set the size equal to 2 times this + 1, so the ship is in the center
		for m in self.mines:
			maxX = max(maxX, abs(m.location[0]))
			maxY = max(maxY, abs(m.location[1]))
		width = 2*maxX + 1
		height = 2*maxY + 1

		#Create empty field
		currentField = []
		for y in range(0, height):
			currentField.append([])
			for x in range(0, width):
				currentField[y].append('.')

		#Add in mines relative to ship at the center [maxX, maxY]		
		for m in self.mines:
			currentField[m.location[1]+maxY][m.location[0]+maxX] = self.depthToLetter(m.depth)
		s = ''

		#Convert to string
		for y in range(0, height):
			for x in range(0, width):
				s += currentField[y][x] + ' '
			s+='\n'

		return s 

	def getScore(self):
		return self.initialMines*10-self.movePenalty-self.shotPenalty


def readField(filename):
	#Reads in field from filename, returns 2D list
	contents = []
	f = open(filename, 'r')
	s = f.readline()
	while(s):
		s = s.strip('\n')
		contents.append(list(s))
		s = f.readline()
	f.close()
	return contents

def readScript(filename):
	#Reads in script file, returns 2D list of command sets
	contents = []
	f = open(filename, 'r')
	s = f.readline()
	while(s):
		s = s.strip('\n')
		contents.append(s.split())
		s = f.readline()
	f.close()
	return contents


if(len(sys.argv)<3):
	print('\n\nMust provide field filename followed by script filename as arguments\n\n')
	exit()

#Read in files
field = readField(sys.argv[1])
script = readScript(sys.argv[2])

#Create simulation object
simulation = MinefieldRun(field)

#Loop through, run commands, print relative info
for i in range(0, len(script)):
	print('Step '+str(i+1)+'\n')
	print(simulation.getFieldString())
	print(' '.join(script[i])+'\n')
	simulation.runLine(script[i])
	print(simulation.getFieldString())

	#Break if finished
	if(simulation.finished):
		break

#Print success value and score
if(simulation.success):
	if(simulation.stepsRun==len(script)):
		score = simulation.getScore()
	else:
		score = 1
	print('pass ('+str(score)+')')
else:
	print('fail (0)')

