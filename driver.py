import time
import sys
from sets import Set
# import resource

start_time = time.time()

class Board:

	def __init__(self, arr, depth=0, move=None, parent=None):
		self.arr = arr
		self.parent = parent
		# self.children = []
		self.move = move
		#keeps track of it's depth, not sure if it is a problem
		self.depth = depth

	# def append_children(self, other):
	# 	self.children.append(other)

	# for understanding purposes
	def print_board(self):
		print self.move
		print self.arr
		print self.depth
		print "*********"

	# def find(self, elem):
	# 	try:
	# 		position = self.arr.index(elem)
	# 	except ValueError:
	# 		return -1
	# 	return position

	def __eq__(self, other):
		return self.arr == other.arr

	def __ne__(self, other):
		return not self.__eq__(other)

	def __hash__(self):
		return hash(str(self.arr))

class Boards:

	def __init__(self):
		self.boards = []

	# creates one single board shifting the 0 according to X value
	def single_new_board(self, x, move):
		my_list = self.other.arr[:]
		aux = my_list[self.position]
		my_list[self.position] = my_list[self.position + x]
		my_list[self.position + x] = aux
		board = Board(my_list, self.other.depth+1, str(move), self.other)
		return board

	# creates all possible boards and returns an array of boards
	def get_new_boards(self, other):
		self.boards = []
		self.other = other		
		self.position = self.other.arr.index(0)
		# Up	
		if (self.position > 2):
			board = self.single_new_board(-3, "Up")
			self.boards.append(board)
		# Down
		if (self.position < 6):
			board = self.single_new_board(3, "Down")
			self.boards.append(board)
		# Left
		if (self.position % 3 != 0):
			board = self.single_new_board(-1, "Left")
			self.boards.append(board)
		# Right
		if(self.position % 3 != 2):
			board = self.single_new_board(1, "Right")
			self.boards.append(board)

		return self.boards


class Bfs:

	def __init__(self, board_initial):
		self.board_initial = board_initial
		self.board_final = Board([0,1,2,3,4,5,6,7,8])
		self.frontier = [board_initial] 
		self.boards_checked = []
		self.game_end = False
		self.path_to_goal = []
		self.cost_of_path = 0
		self.nodes_expanded = 0
		self.max_frontier_size = 0
		self.solution_depth_size = 0
		self.max_depth_size = 0
		self.start_game()
		self.print_game()

	def start_game(self):
		while(self.game_end == False):
			# update max_frontier_size
			if(len(self.frontier) > self.max_frontier_size):
				self.max_frontier_size = len(self.frontier)
			# gets board from queue
			board_current = self.frontier.pop(0)
			# append to boards_checked
			self.boards_checked.append(board_current)
			# if node is not root node, add as an expanded node
			if(board_current.parent):
				self.nodes_expanded += 1
			# if Goal Board has been achieved
			if(board_current == self.board_final):
				self.game_end = True
				self.solution_depth_size = int(board_current.depth)
				# loops through node parents to find solution path
				while(board_current.parent):
					self.cost_of_path += 1
					self.path_to_goal.append(board_current.move)
					board_current = board_current.parent
			# if Goal Board has not been achieved
			else:
				# get new possible boards from class Boards
				boards = Boards().get_new_boards(board_current)

				for board in boards:
					if (board not in self.boards_checked) and (board not in self.frontier):
						self.frontier.append(board)
						if(board.depth > self.max_depth_size):
							self.max_depth_size = board.depth

	def print_game(self):
		print "path_to_goal: " + str(list(reversed(self.path_to_goal)))
		print "cost_of_path: " + str(self.cost_of_path)
		print "nodes_expanded: " + str(self.nodes_expanded)
		print "frontier_size: " + str(len(self.frontier))
		print "max_frontier_size: " + str(self.max_frontier_size)
		print "search_depth: " + str(self.solution_depth_size)
		print "max_search_depth: " + str(self.max_depth_size)
		print "running_time: " + str(time.time() - start_time)
		# print "max_ram_usage: " + str(1.0 * (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) / 1000)

#####################################################################################################
class Dfs:

	def __init__(self, board_initial):
		self.board_initial = board_initial
		self.board_final = Board([0,1,2,3,4,5,6,7,8])
		self.frontier = [board_initial] # STACK OF BOARDS
		self.boards_checked = Set([]) # WILL KEEP TRACK OF BOTH CHECKED AND ON THE FRONTIER
									  # BECAUSE IT MAKES NO DIFFERENCE
		self.game_end = False
		self.path_to_goal = []
		self.cost_of_path = 0
		self.nodes_expanded = 0
		self.max_frontier_size = 0
		self.solution_depth_size = 0
		self.max_depth_size = 0
		self.start_game()
		self.print_game()

	def start_game(self):
		# while game not over
		while(self.game_end == False):
			# auxiliary list
			aux_list = []
			# update max_frontier_size
			if(len(self.frontier) > self.max_frontier_size):
				self.max_frontier_size = len(self.frontier)
			# gets board from stack
			board_current = self.frontier.pop()
			# append to boards_checked
			self.boards_checked.add(board_current)
			# if node is not root node, add as an expanded node
			if(board_current.parent):
				self.nodes_expanded += 1
			# if Goal Board has been achieved
			if(board_current == self.board_final):
				self.game_end = True
				self.solution_depth_size = int(board_current.depth)
				# loops through node parents to find solution path
				while(board_current.parent):
					self.cost_of_path += 1
					self.path_to_goal.append(board_current.move)
					board_current = board_current.parent
			# if Goal Board has not been achieved
			else:
				# get new possible boards from class Boards
				boards = Boards().get_new_boards(board_current)
				# for each board returned (UDLR order)
				for board in boards:
					# check if it is not already used or on the frontier
					if (board not in self.boards_checked):
						# use auxiliary list to append boards on UDLR order
						aux_list.append(board)
						# update board depth
						if(board.depth > self.max_depth_size):
							self.max_depth_size = board.depth
				# while list is not empty, append to frontier on RLDU order
				# print "********"
				while (aux_list):
					aux_board = aux_list.pop()
					self.frontier.append(aux_board)
					self.boards_checked.add(aux_board)
				# print "NODES EXPANDED " + str(self.nodes_expanded)



	def print_game(self):
		print "path_to_goal: " + str(list(reversed(self.path_to_goal)))
		print "cost_of_path: " + str(self.cost_of_path)
		print "nodes_expanded: " + str(self.nodes_expanded)
		print "frontier_size: " + str(len(self.frontier))
		print "max_frontier_size: " + str(self.max_frontier_size)
		print "search_depth: " + str(self.solution_depth_size)
		print "max_search_depth: " + str(self.max_depth_size)
		print "running_time: " + str(time.time() - start_time)
		# print "max_ram_usage: " + str(1.0 * (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) / 1000)		


if (str(sys.argv[1]) == "bfs"):
	board_initial = Board(eval('[' + str(sys.argv[2]) + ']'))
	Bfs(board_initial)

if (str(sys.argv[1]) == "dfs"):
	board_initial = Board(eval('[' + str(sys.argv[2]) + ']'))
	Dfs(board_initial)

