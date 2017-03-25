N = 8

def grid(cars, N=N):
    """Return a tuple of (object, locations) pairs -- the format expected for
    this puzzle.  This function includes a wall pair, ('|', (0, ...)) to 
    indicate there are walls all around the NxN grid, except at the goal 
    location, which is the middle of the right-hand wall; there is a goal
    pair, like ('@', (31,)), to indicate this. The variable 'cars'  is a
    tuple of pairs like ('*', (26, 27)). The return result is a big tuple
    of the 'cars' pairs along with the walls and goal pairs."""
    goals = ((N**2)//2 - 1,)
    walls = (locs(0, N) + locs(N*(N-1), N) + locs(N, N-2, N) 
             + locs(2*N-1, N-2, N))
    walls = tuple(w for w in walls if w not in goals)
    return cars + (('|', walls), ('@', goals))

def locs(start, n, incr=1):
    "Return a tuple of n locations, starting at start and go up by incr."
    return tuple(start+i*incr for i in range(n))


###
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


def solve_parking_puzzle(start, N=N):
    """Solve the puzzle described by the starting position (a tuple 
    of (object, locations) pairs).  Return a path of [state, action, ...]
    alternating items; an action is a pair (object, distance_moved),
    such as ('B', 16) to move 'B' two squares down on the N=8 grid."""
    return shortest_path_search(grid(start, N), psuccessors, is_goal)

def is_goal(state):
    "Goal is when the car (*) overlaps a goal square (@)."
    d = dict(state)
    return set(d['*']) & set(d['@'])


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
    return path[1::2]

def update(tuples, key, val):
    "Return a new (key, val) tuple, dropping old value of key and adding new."
    # Sort the keys to make sure the result is canonical.
    d = dict(tuples)
    d[key] = val
    return tuple(sorted(d.items())) 
###
def psuccessors(state):
    """State is a tuple of (('c': sqs),...); return a {state:action} dict
    where action is of form ('c', dir), where dir is +/-1 or +/-N."""
    results = {}
    occupied = set(s for (c, sqs) in state for s in sqs if c != '@')
    for (c, sqs) in state:
        if c not in '|@': # Walls and goals can't move
            diff = sqs[1]-sqs[0]
            # Either move the max of sqs up, or the min of sqs down
            for (d, start) in [(diff, max(sqs)), (-diff, min(sqs))]:
                for i in range(1, N-2):
                    s = start + d*i
                    if s in occupied:
                        break # Stop when you hit something
                    results[update(state,c,tuple(q+d*i for q in sqs))]=(c,d*i)
    return results

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
    succs = psuccessors(state1)
    return state2 in succs and succs[state2] == action

def same_state(state1, state2):
    "Two states are the same if all corresponding sets of locs are the same."
    d1, d2 = dict(state1), dict(state2)
    return all(set(d1[key]) == set(d2[key]) for key in set(d1) | set(d2))
# test_parking()
# print(path_actions(solve_parking_puzzle(puzzle4)))

print(path_actions(solve_parking_puzzle(puzzle1)))
print(path_actions(solve_parking_puzzle(puzzle2)))
print(path_actions(solve_parking_puzzle(puzzle3)))
print(path_actions(solve_parking_puzzle(puzzle4)))