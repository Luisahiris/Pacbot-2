# Asyncio (for concurrency)
import asyncio
from operator import itemgetter

# Game state
from gameState import *

from search import bfs
from variables import *

cherry_pattern = [('l', 'w'), ('d', 'w'), ('l', 'w'), ('d', 'w'), ('r', 'w'), ('u', 3), ('l', 5), ('u', 3), ('l', 9), ('u', 3), ('l', 6), ('u', 15), ('r', 12), ('d', 3), ('l', 3), ('d', 3), ('r', 3), ('d',6), ('l', 7)]

FREQUENCY = 30
PELLET_WEIGHT = 0.65
GHOST_WEIGHT = 0.35
FRIGHTENED_GHOST_WEIGHT = .3 * GHOST_WEIGHT
GHOST_CUTOFF = 10

class DecisionModule:
	'''
	Sample implementation of a decision module for high-level
	programming for Pacbot, using asyncio.
	'''

	def __init__(self, state: GameState) -> None:
		'''
		Construct a new decision module object
		'''

		# Game state object to store the game information
		self.state = state

		self.red_ghost = state.ghosts[GhostColors.RED]
		self.pink_ghost = state.ghosts[GhostColors.PINK]
		self.blue_ghost = state.ghosts[GhostColors.CYAN]
		self.orange_ghost = state.ghosts[GhostColors.ORANGE]

		self.direction = Directions.RIGHT
		self.grid = None

		self.pellets = self.state.pelletArr
		

		self.strategy = cherry_pattern # initial strategy
		self.curr_quadrant = 3

	def updatePattern(self):
		curr_v = self.strategy[0][1]
		curr_list = list(self.strategy[0])
		curr_list[1] = curr_v - 1
		self.strategy[0] = tuple(curr_list) 

	def completedStrategyMove(self):
		self.strategy.pop(0)

	# def avoidCorners(self):
	# 	#set path away from corners

	# def getPathToPowerPellet(self):
	# 	# get safest path to power pellet
	
	# def areGhostInSameQuadrant(self):
	# 	# return true if the current location of a ghost is in the same quadrant as pacman

	# def getSafestPath(self):
		# look for best path and check its safety.
	
	def getQuadrant(self, row: int, col: int):
		limits = [(16,32),(16,16),(32,16),(32,32)]
		for t in limits:
			if(row <= t[0] and col <= t[1]):
				return(limits.index(t) + 1)
		return -1

	# old code
	def _get_direction(self, p_loc, next_loc):
		if p_loc[0] == next_loc[0]:
			if p_loc[1] < next_loc[1]:
				return Directions.RIGHT
			else:
				return Directions.LEFT
		else:
			if p_loc[0] < next_loc[0]:
				return Directions.DOWN
			else:
				return Directions.UP
			
	def _find_paths_to_closest_ghosts(self, pac_loc):
		ghosts = [self.red_ghost, self.pink_ghost, self.orange_ghost, self.blue_ghost]
		print('ghost')
		print(ghosts[0].state)
		state_paths = [(ghost.state, bfs(self.grid, pac_loc, (ghost.location.col, ghost.location.row), GHOST_CUTOFF)) for ghost in ghosts]
		
		return [sp for sp in state_paths if sp[1] is not None]
	
	def _find_distance_of_closest_pellet(self, target_loc):
		# print('pellets arr')
		# print(self.state.pelletArr)
		return len(bfs(self.grid, target_loc, [o])) - 1
	
	def _target_is_invalid(self, target_loc):
		return self.state.wallAt(target_loc[0], target_loc[1])

	def _is_power_pellet_closer(self, path):
		print('is power pellet closer def path: ', path)
		isPowerPelletClose = False
		for (row, col) in path:
			if self.state.superPelletAt(row, col):
				isPowerPelletClose = True
				break
				
		return isPowerPelletClose
	
	# def _is_power_pellet_closer(self, path):
    #     return O in path
	
	def _get_num_turns(self, p_dir, n_dir):
		lat = [Directions.LEFT, Directions.RIGHT]
		lng = [Directions.DOWN, Directions.UP]

		if p_dir == n_dir:
			return 0
		elif (p_dir in lat and n_dir in lat) or (p_dir in lng and n_dir in lng):
			return 2
		else:
			return 1
	
	def _get_target_with_min_turning_direction(self, mins):
		turns = [(self._get_num_turns(self.direction, direct), targ) for direct, targ in mins]
		return min(turns, key=itemgetter(0))[1]

	def _find_best_target(self, p_loc):
		targets = [p_loc, (p_loc[0] - 1, p_loc[1]), (p_loc[0] + 1, p_loc[1]), (p_loc[0], p_loc[1] - 1), (p_loc[0], p_loc[1] + 1)]
		directions =  [Directions.NONE, Directions.UP, Directions.DOWN, Directions.LEFT, Directions.RIGHT]
		heuristics = []
		for target_loc in targets:
			if self._target_is_invalid(target_loc):
				heuristics.append(float('inf'))
				continue
			dist_to_pellet = self._find_distance_of_closest_pellet(target_loc)
			paths_to_ghosts = self._find_paths_to_closest_ghosts(target_loc)

			closest_ghost = (None, float('inf'))
			ghosts = []
			for state, path in paths_to_ghosts:
				dist = len(path) - 1
				closest_ghost = (state, dist) if dist < closest_ghost[1] else closest_ghost
				ghosts.append((state, dist))
				if self._is_power_pellet_closer(path): 
					if target_loc == p_loc:
						return path[1]
					else:
						return path[0]

			ghost_heuristic = 0
			for state, dist in ghosts:
				if dist < GHOST_CUTOFF:
					if self.state.gameMode == GameModes.SCATTER:
						ghost_heuristic += pow((GHOST_CUTOFF - closest_ghost[1]), 2) * GHOST_WEIGHT
					else:
						ghost_heuristic += pow((GHOST_CUTOFF - closest_ghost[1]), 2) * -1 * FRIGHTENED_GHOST_WEIGHT

			pellet_heuristic = dist_to_pellet * PELLET_WEIGHT
			heuristics.append(ghost_heuristic + pellet_heuristic)
		print(heuristics)
		mins = []
		min_heur = float('inf')
		for i, heur in enumerate(heuristics):
			if heur < min_heur:
				min_heur = heur
				mins = [(directions[i], targets[i])]
			elif heur == min_heur:
				mins.append((directions[i], targets[i]))
		return self._get_target_with_min_turning_direction(mins)

	def updateGrid(self):
		grid = []
		# Loop over all 31 rows
		for row in range(31):
			new_row = []
			# For each cell, choose a character based on the entities in it
			for col in range(28):
				if self.state.wallAt(row, col):
					new_row.append(I)
				elif self.state.superPelletAt(row, col):
					new_row.append(O)
				elif self.state.pelletAt(row, col):
					new_row.append(o)
				else:
					new_row.append(e)
			grid.append(new_row)

		self.grid = grid
		# print(grid)



	async def decisionLoop(self) -> None:
		'''
		Decision loop for Pacbot
		'''

		# Receive values as long as we have access
		while self.state.isConnected():

			'''
			WARNING: 'await' statements should be routinely placed
			to free the event loop to receive messages, or the
			client may fall behind on updating the game state!
			'''

			# If the current messages haven't been sent out yet, skip this iteration
			if len(self.state.writeServerBuf):
				await asyncio.sleep(0)
				continue

			# Lock the game state
			self.state.lock()

			# Decision making
			self.updateGrid()
			# print(self.grid)

			row = self.state.pacmanLoc.row
			col = self.state.pacmanLoc.col

			p_loc = (row, col)
			print(p_loc)
			next_loc = self._find_best_target(p_loc)
			if next_loc != p_loc:
				# print('diff')
				nextDir = self._get_direction(p_loc, next_loc)
				print('next dir: ', nextDir)
				self.state.queueAction(3, nextDir)
				# self._send_command_message_to_target(p_loc, next_loc)

			# first pattern
			# pattern = self.strategy
			# if len(pattern) > 0:
			# 	if pattern[0][0] == 'l':
			# 			new_row = row
			# 			new_col = col - 1
			# 			if pattern[0][1] == 'w':
			# 				wall = self.state.wallAt(new_row, new_col)
			# 				futherWall = self.state.wallAt(new_row, new_col-1)
			# 				if not wall:
			# 					self.state.queueAction(4, Directions.LEFT)
			# 				if futherWall:
			# 					self.completedStrategyMove()
			# 			else:
			# 				if pattern[0][1] > 0:
			# 					self.state.queueAction(4, Directions.LEFT)
			# 					self.updatePattern()
			# 				else:
			# 					self.completedStrategyMove()
			# 	elif pattern[0][0] == 'r':
			# 			new_row = row
			# 			new_col = col + 1
			# 			if pattern[0][1] == 'w':
			# 				wall = self.state.wallAt(new_row, new_col)
			# 				futherWall = self.state.wallAt(new_row, new_col+1)
			# 				if not wall:
			# 					self.state.queueAction(4, Directions.RIGHT)
			# 				if futherWall:
			# 					self.completedStrategyMove()
			# 			else:
			# 				if pattern[0][1] > 0:
			# 					self.state.queueAction(4, Directions.RIGHT)
			# 					self.updatePattern()
			# 				else:
			# 					self.completedStrategyMove()
			# 	elif pattern[0][0] == 'd':
			# 			new_row = row + 1
			# 			new_col = col
			# 			if pattern[0][1] == 'w':
			# 				wall = self.state.wallAt(new_row, new_col)
			# 				futherWall = self.state.wallAt(new_row+1, new_col)
			# 				if not wall:
			# 					self.state.queueAction(4, Directions.DOWN)
			# 				if futherWall:
			# 					self.completedStrategyMove()
			# 			else:
			# 				if pattern[0][1] > 0:
			# 					self.state.queueAction(4, Directions.DOWN)
			# 					self.updatePattern()
			# 				else:
			# 					self.completedStrategyMove()
			# 	elif pattern[0][0] == 'u':
			# 			new_row = row - 1
			# 			new_col = col
			# 			if pattern[0][1] == 'w':
			# 				wall = self.state.wallAt(new_row, new_col)
			# 				futherWall = self.state.wallAt(new_row - 1, new_col)
			# 				if not wall:
			# 					self.state.queueAction(4, Directions.UP)
			# 				if futherWall:
			# 					self.completedStrategyMove()
			# 			else:
			# 				if pattern[0][1] > 0:
			# 					self.state.queueAction(4, Directions.UP)
			# 					self.updatePattern()
			# 				else:
			# 					self.completedStrategyMove()
			# # if self.state.gameMode == 2: #CHASE
			# # print('Ghost', self.state.ghosts[GhostColors.RED].location.row)
			# quadrant = self.getQuadrant(row,col)
			# print('Quadrant', quadrant)
			

			# check for walls
			
			
			# if(not isWall):
			# 	# Write back to the server, as a test (move right)
			# 	self.state.queueAction(4, Directions.RIGHT)
			# else:
			# 	# Write back to the server, as a test (move left)
			# 	self.state.queueAction(4, Directions.DOWN)
			

			# Unlock the game state
			self.state.unlock()

			# Print that a decision has been made
			# print('decided')

			# Free up the event loop
			await asyncio.sleep(0)
