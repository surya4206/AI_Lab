class PuzzleNode:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.cost = 0  # Cost from start node to current node
        self.heuristic = self.calculate_heuristic()  # Heuristic value

    def calculate_heuristic(self):
        # Implement a heuristic function here (e.g., Manhattan distance)
        # For 8-puzzle, one common heuristic is the Manhattan distance
        goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        heuristic = 0
        for i in range(3):
            for j in range(3):
                if self.state[i][j] != 0:
                    goal_row, goal_col = divmod(self.state[i][j] - 1, 3)
                    heuristic += abs(i - goal_row) + abs(j - goal_col)
        return heuristic

    def __lt__(self, other):
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)

def get_blank_position(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

def get_neighbors(node):
    i, j = get_blank_position(node.state)
    neighbors = []
    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Possible moves: right, left, down, up

    for move in moves:
        new_i, new_j = i + move[0], j + move[1]
        if 0 <= new_i < 3 and 0 <= new_j < 3:
            new_state = [row[:] for row in node.state]
            new_state[i][j], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[i][j]
            neighbors.append(PuzzleNode(new_state, node))

    return neighbors

def greedy_best_first_search(initial_state):
    start_node = PuzzleNode(initial_state)
    open_set = [start_node]
    closed_set = set()

    while open_set:
        open_set.sort()  # Sort nodes based on total estimated cost (f = g + h)
        current_node = open_set.pop(0)

        if current_node.state == [[1, 2, 3], [4, 5, 6], [7, 8, 0]]:
            # Goal state found
            path = []
            while current_node:
                path.append(current_node.state)
                current_node = current_node.parent
            return path[::-1]

        closed_set.add(tuple(map(tuple, current_node.state)))

        for neighbor in get_neighbors(current_node):
            if tuple(map(tuple, neighbor.state)) not in closed_set:
                neighbor.cost = current_node.cost + 1
                open_set.append(neighbor)

    return None  # No solution found

# Example usage:
initial_state = [
    [1, 2, 3],
    [4, 0, 5],
    [6, 7, 8]
]

solution = greedy_best_first_search(initial_state)
if solution:
    for step, state in enumerate(solution):
        print(f"Step {step}:")
        for row in state:
            print(row)
        print()
else:
    print("No solution exists.")