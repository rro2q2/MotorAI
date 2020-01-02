import main

visited_states = []
action = {
    "UP": 1,
    "DOWN": 1,
    "LEFT": 1,
    "RIGHT": 1,
    "STOP": 0
}

class Node():
    def __init__(self, pos: tuple, heuristic: int, curCost: int, pathCost: int, value: str, action: str, parent):
        self.pos = pos
        self.heuristic = heuristic
        self.curCost = curCost
        self.pathCost = pathCost
        self.value = value
        self.action = action
        self.parent = parent

    # Will expand the node based on given constraints
    # Returns the set of states (successors) in a list
    def graphExpand(self, grid):
        newStates = []
        curNode = Node((self.pos[0], self.pos[1]), self.heuristic, self.curCost, self.pathCost, self.value, self.action,
                       self)
        if self.isVisitedState(curNode) == False:
            if self.pos[0] != 0 and grid[self.pos[0]-1][self.pos[1]] != 'X': # UP
                heuristic = manhattanDistance(grid, self.pos[0]-1, self.pos[1])
                curCost = self.curCost + action["UP"]
                newNode = Node((self.pos[0]-1, self.pos[1]), heuristic, self.curCost + 1, (curCost + heuristic),
                               grid[self.pos[0]-1][self.pos[1]], "UP", self)
                if self.isVisitedState(newNode) == False:
                    newStates.append(newNode)

            if self.pos[0] != len(grid)-1 and grid[self.pos[0]+1][self.pos[1]] != 'X': # DOWN
                heuristic = manhattanDistance(grid, self.pos[0]+1, self.pos[1])
                curCost = self.curCost + action["DOWN"]
                newNode = Node((self.pos[0]+1, self.pos[1]), heuristic, self.curCost + 1, (curCost + heuristic),
                               grid[self.pos[0]+1][self.pos[1]], "DOWN", self)
                if self.isVisitedState(newNode) == False:
                    newStates.append(newNode)

            if self.pos[1] != 0 and grid[self.pos[0]][self.pos[1]-1] != 'X': # LEFT
                heuristic = manhattanDistance(grid, self.pos[0], self.pos[1]-1)
                curCost = self.curCost + action["LEFT"]
                newNode = Node((self.pos[0], self.pos[1]-1), heuristic, self.curCost + 1, (curCost + heuristic),
                               grid[self.pos[0]][self.pos[1]-1], "LEFT", self)
                if self.isVisitedState(newNode) == False:
                    newStates.append(newNode)

            if self.pos[1] != len(grid)-1 and grid[self.pos[0]][self.pos[1]+1] != 'X': # RIGHT
                heuristic = manhattanDistance(grid, self.pos[0], self.pos[1]+1)
                curCost = self.curCost + action["RIGHT"]
                newNode = Node((self.pos[0], self.pos[1]+1), heuristic, self.curCost + 1, (curCost + heuristic),
                               grid[self.pos[0]][self.pos[1]+1], "RIGHT", self)
                if self.isVisitedState(newNode) == False:
                    newStates.append(newNode)

            heuristic = manhattanDistance(grid, self.pos[0], self.pos[1])
            curCost = self.curCost + action["STOP"]
            newNode = Node((self.pos[0], self.pos[1]), heuristic, self.curCost, (curCost + heuristic),
                           grid[self.pos[0]][self.pos[1]], "STOP", self) # STOP
            if self.isVisitedState(newNode) == False:
                newStates.append(newNode)

            # Add node into the visited list
            if self.isVisitedState(curNode) == False:
                visited_states.append(curNode)
        return newStates

    # Check if state has already been visited
    # Returns True if already visited, otherwise False
    def isVisitedState(self, node):
        for state in visited_states:
            if node.pos == state.pos:
                return True
        return False

# Checks to see whether the node is in the list or not
# Returns true if it is, otherwise false
def inClosedList(node, closed):
    for item in closed:
        if node.pos == item.pos:
            return True
    return False

# Performs the A* graph search algorithm of finding the goal state
# Returns the goal state, if found, otherwise a list of states
def aStarSearch(node, grid):
    open = []
    closed = []
    states = []
    open.append(node)
    while len(open) > 0:
        temp_node = findMinimumPathCost(open)
        if temp_node.heuristic == 0 and temp_node.value == 'G':
            visited_states.append(temp_node)
            open.append(temp_node)
            return temp_node # Goal has been found
        else:
            if inClosedList(temp_node, closed) == False:
                closed.append(temp_node) # Store node in closed list
            # Expand the current temp node and return the successors in a list
            states = temp_node.graphExpand(grid)
            for item in states:
                open.append(item)
    print("Not Reachable")
    return states


# Find the minimum f in the open list and pops it off
# Returns the temp node of the indicated minimum pathCost f
# and the index in which it was found in the list
def findMinimumPathCost(open):
    temp = open[0]
    index = 0
    min_pc = temp.pathCost
    for i in range(len(open)):
        if open[i].pathCost < min_pc:
            min_pc = open[i].pathCost
            temp = open[i]
            index = i # Assign to the index in which it was found
    open.pop(index) # Pop it from list
    return temp

# Runs a the City Block distance formula for estimated heuristic from goal state
# Returns the value of each coordinate node and assigns it to the heuristic
def manhattanDistance(grid, x, y):
    value = 0
    for i in range(len(grid)):
        for j in range(len(grid)):
            if (i, j) == (x, y):
                value = abs(main.goal_coord["Mason"][0] - i) + abs(main.goal_coord["Mason"][1] - j)
    return value

# Finds the path from start to goal node
# Returns the path to goal state
def pathToGoal(leaf):
    path = []
    current = leaf
    while current != None:
        path.insert(0, current)
        current = current.parent
    return path
