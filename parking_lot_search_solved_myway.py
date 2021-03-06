"""
UNIT 4: Search

Your task is to maneuver a car in a crowded parking lot. This is a kind of 
puzzle, which can be represented with a diagram like this: 

| | | | | | | |  
| G G . . . Y |  
| P . . B . Y | 
| P * * B . Y @ 
| P . . B . . |  
| O . . . A A |  
| O . S S S . |  
| | | | | | | | 

A '|' represents a wall around the parking lot, a '.' represents an empty square,
and a letter or asterisk represents a car.  '@' marks a goal square.
Note that there are long (3 spot) and short (2 spot) cars.
Your task is to get the car that is represented by '**' out of the parking lot
(on to a goal square).  Cars can move only in the direction they are pointing.  
In this diagram, the cars GG, AA, SSS, and ** are pointed right-left,
so they can move any number of squares right or left, as long as they don't
bump into another car or wall.  In this diagram, GG could move 1, 2, or 3 spots
to the right; AA could move 1, 2, or 3 spots to the left, and ** cannot move 
at all. In the up-down direction, BBB can move one up or down, YYY can move 
one down, and PPP and OO cannot move.

You should solve this puzzle (and ones like it) using search.  You will be 
given an initial state like this diagram and a goal location for the ** car;
in this puzzle the goal is the '.' empty spot in the wall on the right side.
You should return a path -- an alternation of states and actions -- that leads
to a state where the car overlaps the goal.

An action is a move by one car in one direction (by any number of spaces).  
For example, here is a successor state where the AA car moves 3 to the left:

| | | | | | | |  
| G G . . . Y |  
| P . . B . Y | 
| P * * B . Y @ 
| P . . B . . |  
| O A A . . . |  
| O . . . . . |  
| | | | | | | | 

And then after BBB moves 2 down and YYY moves 3 down, we can solve the puzzle
by moving ** 4 spaces to the right:

| | | | | | | |
| G G . . . . |
| P . . . . . |
| P . . . . * *
| P . . B . Y |
| O A A B . Y |
| O . . B . Y |
| | | | | | | |

You will write the function

	solve_parking_puzzle(start, N=N)

where 'start' is the initial state of the puzzle and 'N' is the length of a side
of the square that encloses the pieces (including the walls, so N=8 here).

We will represent the grid with integer indexes. Here we see the 
non-wall index numbers (with the goal at index 31):

 |  |  |  |  |  |  |  |
 |  9 10 11 12 13 14  |
 | 17 18 19 20 21 22  |
 | 25 26 27 28 29 30 31
 | 33 34 35 36 37 38  |
 | 41 42 43 44 45 46  |
 | 49 50 51 52 53 54  |
 |  |  |  |  |  |  |  |

The wall in the upper left has index 0 and the one in the lower right has 63.
We represent a state of the problem with one big tuple of (object, locations)
pairs, where each pair is a tuple and the locations are a tuple.  Here is the
initial state for the problem above in this format:
"""

puzzle1 = (
 ('@', (31,)),
 ('*', (26, 27)), 
 ('G', (9, 10)),
 ('Y', (14, 22, 30)), 
 ('P', (17, 25, 33)), 
 ('O', (41, 49)), 
 ('B', (20, 28, 36)), 
 ('A', (45, 46)), 
 ('|', (0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 23, 24, 32, 39,
		40, 47, 48, 55, 56, 57, 58, 59, 60, 61, 62, 63)))

# A solution to this puzzle is as follows:

#     path = solve_parking_puzzle(puzzle1, N=8)
#     path_actions(path) == [('A', -3), ('B', 16), ('Y', 24), ('*', 4)]

# That is, move car 'A' 3 spaces left, then 'B' 2 down, then 'Y' 3 down, 
# and finally '*' moves 4 spaces right to the goal.

# Your task is to define solve_parking_puzzle:
from copy import deepcopy

N = 8

def solve_parking_puzzle(start, N=N):
	"""Solve the puzzle described by the starting position (a tuple 
	of (object, locations) pairs).  Return a path of [state, action, ...]
	alternating items; an action is a pair (object, distance_moved),
	such as ('B', 16) to move 'B' two squares down on the N=8 grid."""
	return(shortest_path_search(grid(start,N),successors,is_goal))
# But it would also be nice to have a simpler format to describe puzzles,
# and a way to visualize states.
# You will do that by defining the following two functions:

def locs(start, n, incr=1):
	"Return a tuple of n locations, starting at start and incrementing by incr."
	return tuple([loc for loc in range(start, start + n * incr, incr)])

def grid(cars, N=N):
	"""Return a tuple of (object, locations) pairs -- the format expected for
	this puzzle.  This function includes a wall pair, ('|', (0, ...)) to 
	indicate there are walls all around the NxN grid, except at the goal 
	location, which is the middle of the right-hand wall; there is a goal
	pair, like ('@', (31,)), to indicate this. The variable 'cars'  is a
	tuple of pairs like ('*', (26, 27)). The return result is a big tuple
	of the 'cars' pairs along with the walls and goal pairs."""
	top = list(range(N))
	bottom = list(range(N**2-N, N**2))
	right = [side for side in range(top[-1],bottom[-1],N)]
	goal_pos = right[len(right) // 2]
	goal = [('@',tuple([goal_pos]))]
	left = [side for side in range(top[0],bottom[0],N)]
	#set bc left border and right border share one el with top / bottom
	border = [('|',tuple(set(top+bottom+left+right)-{goal_pos}))]
	return tuple(border + goal + list(cars))

def show(state, N=N, pretty=False):
	"Print a representation of a state as an NxN grid."
	# Initialize and fill in the board.
	board = ['.'] * N**2
	for (c, squares) in state:
		for s in squares:
			board[s] = c
	# Now print it out
	if pretty:
		for i,s in enumerate(board):
			# print (s,)
			# print (s,end='')
			if i % N == N - 1: print()
		return
	return board

# Here we see the grid and locs functions in use:

puzzle1 = grid((
	('*', locs(26, 2)),
	('G', locs(9, 2)),
	('Y', locs(14, 3, N)),
	('P', locs(17, 3, N)),
	('O', locs(41, 2, N)),
	('B', locs(20, 3, N)),
	('A', locs(45, 2))))

puzzle2 = grid((
	('*', locs(26, 2)),
	('B', locs(20, 3, N)),
	('P', locs(33, 3)),
	('O', locs(41, 2, N)),
	('Y', locs(51, 3))))

puzzle3 = grid((
	('*', locs(25, 2)),
	('B', locs(19, 3, N)),
	('P', locs(36, 3)),
	('O', locs(45, 2, N)),
	('Y', locs(49, 3))))

# Here are the shortest_path_search and path_actions functions from the unit.
# You may use these if you want, but you don't have to.

def shortest_path_search(start, successors, is_goal):
	"""Find the shortest path from start state to a state
	such that is_goal(state) is true."""
	if is_goal(start):
		return [start]
	explored = set() # set of states we have visited
	frontier = [ [start] ] # ordered list of paths we have blazed
	while frontier:
		path = frontier.pop(0)
		s = path[-1]
		for (state, action) in successors(s).items():
			if state not in explored:
				explored.add(state)
				path2 = path + [action, state]
				if is_goal(state):
					return path2
				else:
					frontier.append(path2)
	return []

def path_actions(path):
	"Return a list of actions in this path."
	#why i couldnt FIND the tuple vs list bug... i changed the ANSWER
	#here to have tuple as actions, so printing out the main function
	#appeared correct.  But the internal representation (see line 230)
	#was still a list until i made the change, so the grader was picking
	#up on that representation before it got to this one.
	return list(map(tuple,path[1::2]))

def get_orientation(car):
	carsymbol,loc = car
	if carsymbol not in '@|':
		return 'H' if loc[1] - loc[0] == 1 else 'V'

def update_grid(new_locs,car,grid):
	N = int((max(dict(grid)['|'])+1) ** 0.5)
	old_locs = car[1]
	direction = {'H':1,'V':N}
	d = direction[get_orientation(car)]
	gridmap = dict(grid)
	new_grids = []
	for nl in new_locs:
		grid = deepcopy(gridmap)
		if nl < min(old_locs):
			grid[car[0]] = locs(nl,len(old_locs),d)
			action = tuple([car[0],nl - min(old_locs)])#made tuple
		elif nl > max(old_locs):
			grid[car[0]] = locs(nl - d * (len(old_locs)-1),len(old_locs),d)
			action = tuple([car[0],nl - max(old_locs)])#made tuple
		new_grids.append((tuple(grid.items()),action))#all that time.. failed because
													  #"action" needs to be a tuple.
													  #chg either here or both above as shown
	return new_grids

def legal_moves(car,grid):
	N = int((max(dict(grid)['|'])+1) ** 0.5)
	pos, locs  = get_orientation(car), car[1]
	dirs = {'V':N,'H':1}
	full = {l for c in grid for l in c[1] if c[0] not in car[0]+'@'}
	maxcar, mincar = max(locs), min(locs)
	moves = []
	if pos == 'V':
		while maxcar not in full:
			maxcar += N
			moves.append(maxcar)
		while mincar not in full:
			mincar -=N
			moves.append(mincar)
	elif pos == 'H':
		while maxcar not in full:
			maxcar += 1
			moves.append(maxcar)
		while mincar not in full:
			mincar -=1
			moves.append(mincar)    
	return set(moves) - full

def successors(state):      
	succ = {}
	for car,old_locs in state:
		if car not in '|@':
			new_locs = legal_moves((car,old_locs),state) #e.g. (20,28)
			carsize = len(old_locs)
			if new_locs:
				new_state = [(s,action) for s,action in update_grid(new_locs,(car,old_locs),state)]
				for s,action in new_state:
					succ[s] = action
	return succ

def is_goal(state):
	"Goal is when the car (*) overlaps a goal square (@)."
	d = dict(state)
	return set(d['*']) & set(d['@'])

def test():
	assert  legal_moves(('B', (20,28,36)),puzzle1) == set([12,44,52])
	assert  legal_moves(('G', (9, 10)),puzzle1) == set([11,12,13])
	assert  legal_moves(('O', (41, 49)),puzzle1) == set([])
	assert  legal_moves(('A', (45, 46)),puzzle1) == set([44,43,42])
	assert  legal_moves(('Y', (14,22,30)),puzzle1) == set([38])
	print('tests pass!')
# test()

def test_parking():
	assert valid_solution(puzzle1, 4)
	assert valid_solution(puzzle2, 7)
	assert valid_solution(puzzle3, 7)
	assert valid_solution(puzzle4, 8)
	assert locs(26, 2) == (26, 27)
	assert locs(20, 3, 8) == (20, 28, 36)
	assert same_state(
		grid((('*', locs(25, 2)),
			  ('B', locs(19, 3, N)),
			  ('P', locs(36, 3)),
			  ('O', locs(45, 2, N)),
			  ('Y', locs(49, 3)))),
		(('*', (25, 26)), ('B', (19, 27, 35)), ('P', (36, 37, 38)), 
		 ('O', (45, 53)), ('Y', (49, 50, 51)), 
		 ('|', (0, 1, 2, 3, 4, 5, 6, 7, 56, 57, 58, 59, 60, 61, 62, 63, 
				8, 16, 24, 32, 40, 48, 15, 23, 39, 47, 55)), 
			('@', (31,))))
	print('tests pass!')

puzzle4 = grid((
	('*', locs(26, 2)),
	('G', locs(9, 2)),
	('Y', locs(14, 3, N)),
	('P', locs(17, 3, N)),
	('O', locs(41, 2, N)),
	('B', locs(20, 3, N)),
	('A', locs(45, 2)),
	('S', locs(51, 3))))

def valid_solution(puzzle, length):
	"Does solve_parking_puzzle solve this puzzle in length steps?"
	path = solve_parking_puzzle(puzzle)
	return (len(path_actions(path)) == length and
			same_state(path[0], puzzle) and
			is_goal(path[-1]) and
			all(legal_step(path[i:i+3]) for i in range(0,len(path)-2, 2)))

def legal_step(path):
	"A legal step has an action that leads to a valid successor state."
	# Here the path must be of the form [s0, a, s1].
	state1, action, state2 = path 
	succs = successors(state1)
	return state2 in succs and succs[state2] == action

def same_state(state1, state2):
	"Two states are the same if all corresponding sets of locs are the same."
	d1, d2 = dict(state1), dict(state2)
	return all(set(d1[key]) == set(d2[key]) for key in set(d1) | set(d2))

# print(show(puzzle3,N=8,pretty=True))
print(path_actions(solve_parking_puzzle(puzzle1,N)))
# print(path_actions(solve_parking_puzzle(puzzle2,N)))
# print(path_actions(solve_parking_puzzle(puzzle3,N)))
# print(path_actions(solve_parking_puzzle(puzzle4,N)))
# test_parking()


