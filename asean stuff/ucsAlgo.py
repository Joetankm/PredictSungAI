# ucs_module.py

class Node:
    def __init__(self, state=None, parent=None, cost=0):
        self.state = state
        self.parent = parent
        self.children = []
        self.cost = cost

    def addChildren(self, children):
        self.children.extend(children)

def expandAndReturnChildren(state_space, node):
    children = []
    for [m, n, c] in state_space:
        if m == node.state:
            children.append(Node(n, node.state, node.cost + c))
        elif n == node.state:
            children.append(Node(m, node.state, node.cost + c))
    return children

def appendAndSort(frontier, node):
    duplicated = False
    removed = False
    for i, f in enumerate(frontier):
        if f.state == node.state:
            duplicated = True
            if f.cost > node.cost:
                del frontier[i]
                removed = True
                break    
    if (not duplicated) or removed:
        insert_index = len(frontier)
        for i, f in enumerate(frontier):
            if f.cost > node.cost:
                insert_index = i
                break
        frontier.insert(insert_index, node)
    return frontier

# 🧠 THIS is your exported function to be used in Flask
def find_shortest_path(initial_state, goal_state):
    state_space = [
        ["Pahang", "Kelantan", 306.95],
        ["Pahang", "Johor", 357.58],
        ["Pahang", "Negeri Sembilan", 176.37],
        ["Pahang", "Terengganu", 275.92],
        ["Pahang", "Selangor", 211.98],
        ["Pahang", "Sarawak", 1198.86],
        ["Pahang", "Perak", 458.99],

        ["Kelantan", "Terengganu", 267.44],
        ["Kelantan", "Perak", 242.48],
     
        ["Johor", "Melaka", 215.45],
        ["Johor", "Negeri Sembilan", 181.42],
        ["Johor", "Sarawak", 1088.71],

        ["Melaka", "Negeri Sembilan", 79.72],

        ["Negeri Sembilan", "Selangor", 112.37],

        ["Sarawak", "Sabah", 511.83],
        ["Sarawak", "Terengganu", 1197.66],

        ["Penang", "Perak", 176.98],
        ["Penang", "Kedah", 136.81],

        ["Perak", "Selangor", 267.47],
        ["Perak", "Kedah", 186.87],

        ["Kedah", "Perlis", 91.42],
        
    ]

    frontier = []
    explored = []
    found_goal = False
    goalie = Node()
    frontier.append(Node(initial_state, None))

    while not found_goal and frontier:
        if frontier[0].state == goal_state:
            found_goal = True
            goalie = frontier[0]
            break

        children = expandAndReturnChildren(state_space, frontier[0])
        frontier[0].addChildren(children)
        explored.append(frontier[0])
        del frontier[0]

        for child in children:
            if not (child.state in [e.state for e in explored]):
                frontier = appendAndSort(frontier, child)

    # Backtrack to find path
    solution = [goalie.state]
    path_cost = goalie.cost
    while goalie.parent is not None:
        solution.insert(0, goalie.parent)
        for e in explored:
            if e.state == goalie.parent:
                goalie = e
                break
       
    return solution, path_cost
