import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

class Puzzle8:
    def __init__(self, initial, goal):
        self.initial = tuple(map(tuple, initial)) # Convert to immutable tuples
        self.goal = tuple(map(tuple, goal))
        self.rows, self.cols = 3, 3
        self.moves = [(-1, 0), (1, 0), (0, -1), (0, 1)] # Up, Down, Left, Right

    def get_blank_position(self, state):
        """Find the row and column of the blank tile (0)."""
        for i in range(self.rows):
            for j in range(self.cols):
                if state[i][j] == 0:
                    return i, j

    def move_tile(self, state, row, col, new_row, new_col):
        """Swap the blank tile (0) with an adjacent tile."""
        new_state = [list(r) for r in state]
        new_state[row][col], new_state[new_row][new_col] = new_state[new_row][new_col], new_state[row][col]
        return tuple(map(tuple, new_state))

    def bfs(self):
        """Breadth-First Search to explore all possible states."""
        queue = deque([(self.initial, None, 0)]) # (current state, parent state, cost)
        visited = set()
        visited.add(self.initial)
        tree = nx.DiGraph() # Directed graph for the tree
        tree.add_node(self.initial)

        while queue:
            state, parent, cost = queue.popleft()

            if parent:
                tree.add_edge(parent, state) # Add parent-child relation

            if state == self.goal:
                print(f"Goal state reached in {cost} moves!") # Corrected cost
                return tree

            blank_row, blank_col = self.get_blank_position(state)

            for dr, dc in self.moves:
                new_row, new_col = blank_row + dr, blank_col + dc

                if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
                    new_state = self.move_tile(state, blank_row, blank_col, new_row, new_col)
                    if new_state not in visited:
                        visited.add(new_state)
                        queue.append((new_state, state, cost + 1)) # Increment cost

        return tree

    def draw_tree(self, tree):
        """Visualize the BFS tree with the initial state at the top and child nodes below."""
        pos = self.vertical_layout(tree) # Custom vertical layout for BFS tree
        plt.figure(figsize=(10, 8))
        # Convert state tuples into readable labels
        labels = {node: "\n".join([" ".join(map(str, row)) for row in node]) for node in tree.nodes}
        nx.draw(tree, pos, with_labels=True, labels=labels, node_size=2000, node_color="lightblue",
                font_size=8, font_weight="bold")
        plt.title("BFS Tree of Puzzle 8", fontsize=14)
        plt.show()

    def vertical_layout(self, tree):
        """Custom vertical layout to position the nodes from top to bottom."""
        pos = {}
        level = {self.initial: 0} # Initialize the root level
        level_positions = {}
        # Perform BFS to assign levels (depth) to each node
        queue = deque([self.initial])
        while queue:
            node = queue.popleft()
            current_level = level[node]
            if current_level not in level_positions:
                level_positions[current_level] = []
            level_positions[current_level].append(node)
            for neighbor in tree.neighbors(node):
                if neighbor not in level:
                    level[neighbor] = current_level + 1
                    queue.append(neighbor)

        # Adjust vertical and horizontal spacing to avoid overlap
        pos = {}
        for depth, nodes_at_depth in level_positions.items():
            # Assign unique x-coordinates to nodes at the same depth to avoid overlap
            for i, node in enumerate(nodes_at_depth):
                # x = the horizontal position, y = depth (vertical level)
                pos[node] = (i * 2, -depth * 2) # Adjust spacing by multiplying by 2 to avoid overlap
        return pos

def get_puzzle_input(prompt):
    """Function to take input for the puzzle in 3x3 grid format."""
    print(prompt)
    puzzle = []
    for i in range(3):
        row_str = input(f"Enter row {i + 1} (3 numbers separated by space): ")
        row = list(map(int, row_str.split()))
        while len(row) != 3:
            print("Please enter exactly 3 numbers for the row.")
            row_str = input(f"Enter row {i + 1} (3 numbers separated by space): ")
            row = list(map(int, row_str.split()))
        puzzle.append(row)
    return puzzle

# Get initial and goal states from the user
initial_state = get_puzzle_input("Enter the initial state of the puzzle (3x3 grid):")
goal_state = get_puzzle_input("Enter the goal state of the puzzle (3x3 grid):")

# Run BFS and visualize the tree
puzzle = Puzzle8(initial_state, goal_state)
bfs_tree = puzzle.bfs()
if bfs_tree:
    puzzle.draw_tree(bfs_tree)
else:
    print("Goal state not reachable within the explored states.")