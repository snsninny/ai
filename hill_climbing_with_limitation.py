import copy

class Puzzle:
    def __init__(self, initial, goal):
        self.initial = initial
        self.goal = goal
        self.size = 3  # 8-puzzle (3x3)
        self.directions = [("UP", -1, 0), ("DOWN", 1, 0), ("LEFT", 0, -1), ("RIGHT", 0, 1)]

    def find_blank(self, state):
        for i in range(self.size):
            for j in range(self.size):
                if state[i][j] == 0:
                    return i, j

    def h(self, state):
        misplaced = 0
        misplaced_tiles = []
        for i in range(self.size):
            for j in range(self.size):
                if state[i][j] != 0 and state[i][j] != self.goal[i][j]:
                    misplaced += 1
                    misplaced_tiles.append(state[i][j])
        return misplaced, misplaced_tiles

    def get_neighbors(self, state, prev_state):
        x, y = self.find_blank(state)
        moves = []
        
        for move, dx, dy in self.directions:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < self.size and 0 <= new_y < self.size:
                new_state = copy.deepcopy(state)
                new_state[x][y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[x][y]
                if new_state == prev_state:
                    continue  # Prevent moving back to the previous state
                h_value, misplaced_tiles = self.h(new_state)
                moves.append((move, new_state, h_value, misplaced_tiles))
        
        return moves

    def hill_climb(self):
        current = self.initial
        current_h, misplaced_tiles = self.h(current)
        prev_state = None
        print("\nStarting state (h =", current_h, ") Misplaced tiles ->", misplaced_tiles)
        self.print_state(current)

        step = 1
        while True:
            neighbors = self.get_neighbors(current, prev_state)
            if not neighbors:
                print("\n🚩 No valid moves left! Stopping...")
                break

            print(f"\nStep {step}: Evaluating possible moves from current state:")
            for move, state, h_val, misplaced in neighbors:
                print(f"  - Move {move}: h = {h_val}, Misplaced tiles -> {misplaced}")
                self.print_state(state)

            next_state = None
            next_h = float('inf')
            chosen_move = None

            for move, state, h_val, _ in neighbors:
                if h_val < next_h:
                    next_state = state
                    next_h = h_val
                    chosen_move = move

            if next_h >= current_h:
                print("\n🚩 Plateau reached! No better moves available. Stopping...")
                print(f"Final plateau state (h = {current_h}):")
                self.print_state(current)
                break

            prev_state = current  # Store previous state to avoid backtracking
            current, current_h, misplaced_tiles = next_state, *self.h(next_state)
            print(f"\nStep {step}: Moving {chosen_move} (h = {current_h}): Misplaced tiles -> {misplaced_tiles}")
            self.print_state(current)
            step += 1

            if current == self.goal:
                print("\n🎯 Goal reached in", step - 1, "steps!")
                break

    def print_state(self, state):
        for row in state:
            print(" ".join(str(num) if num != 0 else " " for num in row))
        print("-" * 10)


def get_input_matrix(name):
    print(f"Enter the {name} state (use 0 for blank space, row by row):")
    matrix = []
    for i in range(3):
        row = list(map(int, input().split()))
        matrix.append(row)
    return matrix

initial_state = get_input_matrix("initial")
goal_state = get_input_matrix("goal")

puzzle = Puzzle(initial_state, goal_state)
puzzle.hill_climb()