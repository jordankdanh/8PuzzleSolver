import random
import time
import heapq

# Define a class to represent a point
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return (F"({self.x}, {self.y})")

# Define a class to represent the game board
class Board:
    def __init__(self, data):
        self.data = data
        
    def __str__(self):
        return '[' + '\n'.join([str(row) for row in self.data]) + ']'

# Define a class to represent a node in the search tree
class Node:
    def __init__(self, board, blank, parent=None):
        self.board = board
        self.blank = blank
        self.parent = parent
        self.children = []

    def __hash__(self):
        return hash(tuple(tuple(row) for row in self.board.data))

    def __eq__(self, other):
        return isinstance(other, Node) and self.board.data == other.board.data

# Function to check if a given position is safe within the board
def is_safe(x, y):
    return 0 <= x < 3 and 0 <= y < 3

# Function to generate children nodes for a given node
def generate_children(node, visited):
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    for dx, dy in dirs:
        next_x, next_y = node.blank.x + dx, node.blank.y + dy
        if is_safe(next_x, next_y):
            board = [row[:] for row in node.board.data]
            board[next_x][next_y], board[node.blank.x][node.blank.y] = board[node.blank.x][node.blank.y], board[next_x][next_y]
            child_board = Board(board)
            child_node = Node(child_board, Point(next_x, next_y), node)
            if child_node not in visited:
                node.children.append(child_node)

# Function to create a solvable starting state for the puzzle
def createStartState():
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    random.shuffle(numbers)
    startState = Board([numbers[i:i+3] for i in range(0, len(numbers), 3)])
    while not isBoardSolvable(startState.data):
        random.shuffle(numbers)
        startState = Board([numbers[i:i+3] for i in range(0, len(numbers), 3)])
    return startState

# Function to check if a given board configuration is solvable
def isBoardSolvable(board):
    def getInversionCount(flatArray):
        invCount = 0
        emptyValue = 0

        for i in range(0, 9):
            for j in range(i + 1, 9):
                if flatArray[j] != emptyValue and flatArray[i] != emptyValue and flatArray[i] > flatArray[j]:
                    invCount += 1
        return invCount
    
    startStateInvCount = getInversionCount([j for sub in board for j in sub])
 
    return (startStateInvCount % 2 == 1)

# Function to compare two boards for equality
def compareBoards(a: Board, b: Board):
    for i in range(3):
        for j in range(3):
            if a.data[i][j] != b.data[i][j]:
                return False
    return True

# Function to convert a movement vector to a direction string
def vectorToDirection(point: Point):
    x, y = point.x, point.y
    if (x, y) == (1, 0):
        return "Up"
    elif (x, y) == (-1, 0):
        return "Down"
    elif (x, y) == (0, 1):
        return "Left"
    elif (x, y) == (0, -1):
        return "Right"
    elif (x, y) == (0, 0):
        return "Start"
    else:
        return "unknown"

# Function to display the solution path
def showSolution(curr):
    def showMovement(parent: Node, current: Node):
        return Point(current.blank.x - parent.blank.x, current.blank.y - parent.blank.y)
    
    steps = []
    while curr is not None:
        if curr.parent:
            vector = showMovement(curr, curr.parent)
        else:
            vector = (Point(0,0))
        steps.append((curr, vector))
        curr = curr.parent
    
    step_number = 1
    for step, vector in reversed(steps):
        print(f"Step {step_number}: {vectorToDirection(vector)}")
        print(step.board)
        print()
        step_number += 1

# Function to find the position of zero on the board
def find_zero(board):
    for i in range(3):
        for j in range(3):
            if board.data[i][j] == 0:
                return Point(i,j)

# Function to calculate the Manhattan distance heuristic
def manhattan_distance(state: Board, goal: Board):
    sum = 0
    for i in range(3):
        for j in range(3):
            if state.data[i][j] != 0:
                for x in range(3):
                    for y in range(3):
                        if(state.data[i][j] == goal.data[x][y]):
                            sum += abs(i-x) + abs(j-y)
    return sum

# Function to calculate the number of tiles out of place heuristic
def tilesOutOfPlace(start: Board, goal: Board):
    count = 0
    for i in range(3):
        for j in range(3):
            if start.data[i][j] != goal.data[i][j]:
                count += 1
    return count

# Iterative Deepening Depth-First Search Algorithm
def iddfs(root, max_depth):
    for depth_limit in range(max_depth + 1):
        result = dfs(root, depth_limit)
        if result:
            print(F"Depth Search Level: {depth_limit}")
            return result
    return None

# Depth-First Search Algorithm
def dfs(root, depth_limit):
    global nodesVisited
    if not root or depth_limit < 0:
        return
    
    stack = [(root, 0)]
    visited = set()
    while stack:
        node, depth = stack.pop()
        visited.add(node)
        nodesVisited += 1
        if compareBoards(node.board, goalState):
            return node
        if depth < depth_limit:
            generate_children(node, visited)

            for child in node.children:
                if child not in visited:
                    stack.append((child, depth + 1))

# Uniform Cost Search Algorithm
def ucs(root):
    global nodesVisited
    priorityQueue = []
    heapq.heappush(priorityQueue, (0, id(root),root))
    visited = set()
    depth = 0
    while priorityQueue:
        depth += 1
        nodeDepth, tag, node = heapq.heappop(priorityQueue)
        
        if compareBoards(node.board, goalState):
            return node
        
        if node not in visited:
            visited.add(node)
            nodesVisited+= 1

            if not node.children:
                generate_children(node, visited)
            for child in node.children:
                heapq.heappush(priorityQueue, (depth, id(child), child))
    return None

# Best-First Search Algorithm
def bfs(root):
    global nodesVisited
    priorityQueue = []
    heapq.heappush(priorityQueue, (0, id(root),root))
    visited = set()
    while priorityQueue:
        nodeDepth, tag, node = heapq.heappop(priorityQueue)
        if compareBoards(node.board, goalState):
            return node
        
        if node not in visited:
            visited.add(node)
            nodesVisited+= 1

            if not node.children:
                generate_children(node, visited)
            for child in node.children:
                heapq.heappush(priorityQueue, (manhattan_distance(child.board, goalState), id(child), child))
    return None

# A* Search Algorithm
def astar(root):
    global nodesVisited
    priorityQueue = []
    heapq.heappush(priorityQueue, (0, id(root),root))
    visited = set()
    depth = 0
    while priorityQueue:
        depth+= 1
        nodeDepth, tag, node = heapq.heappop(priorityQueue)
        
        if compareBoards(node.board, goalState):
            return node
        
        if node not in visited:
            visited.add(node)
            nodesVisited+= 1

            if not node.children:
                generate_children(node, visited)
            for child in node.children:
                heapq.heappush(priorityQueue, ((tilesOutOfPlace(child.board, goalState) + depth), id(child), child))
    return None

nodesVisited = 0

goalState = Board([[1, 2, 3], 
                    [8, 0, 4], 
                    [7, 6, 5]])

startState = createStartState()
print("Random Starting Position")
print(startState)
print()

print("Goal State:")
print(goalState)
print()

while True:
        print("Menu:")
        print("1. DFS Algorithm (IDDFS)")
        print("2. UCS Algorithm")
        print("3. BFS Algorithm")
        print("4. A*")
        print("0. Exit")
        print()

        choice = input("Enter your choice: ")

        if choice == "1":
            startTime = time.time()
            root = Node(startState, find_zero(startState))
            dfsSolution = iddfs(root, 64)
            showSolution(dfsSolution)
            endTime = time.time()
            runTime = (endTime - startTime) * 1000
            print("Runtime of the program: {:.2f} milliseconds".format(runTime))
            break

        elif choice == "2":
            startTime = time.time()
            root = Node(startState, find_zero(startState))
            ucsSolution = ucs(root)
            showSolution(ucsSolution)
            endTime = time.time()
            runTime = (endTime - startTime) * 1000
            print("Runtime of the program: {:.2f} milliseconds".format(runTime))
            break

        elif choice == "3":
            startTime = time.time()
            root = Node(startState, find_zero(startState),)
            bfsSolution = bfs(root)
            showSolution(bfsSolution)
            endTime = time.time()
            runTime = (endTime - startTime) * 1000
            print("Runtime of the program: {:.2f} milliseconds".format(runTime))
            break

        elif choice == "4":
            startTime = time.time()
            root = Node(startState, find_zero(startState),)
            astarSolution = astar(root)
            showSolution(astarSolution)
            endTime = time.time()
            runTime = (endTime - startTime) * 1000
            print("Runtime of the program: {:.2f} milliseconds".format(runTime))
            break

        elif choice == "0":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please enter a number between 0 and 4.")

print(F"Amount of nodes Visited: {nodesVisited}")
