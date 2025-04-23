import re

def parse_input(prompt):
    while True:
        user_input = input(prompt)
        match = re.match(r"\((\d+),(\d+)\)", user_input)
        if match:
            return int(match.group(1)), int(match.group(2))
        print("Invalid input format. Please enter in (x,y) format.")

def water_jug_dfs(jug1_capacity, jug2_capacity, goal_jug1, goal_jug2, visited=None, path=None,
                   jug1=0, jug2=0):
    if visited is None:
        visited = set()
    if path is None:
        path = []

    if (jug1, jug2) in visited:
        return False

    path.append((jug1, jug2))
    print(f"Current state: ({jug1}, {jug2})")
    visited.add((jug1, jug2))

    if jug1 == goal_jug1 and jug2 == goal_jug2:
        print("Goal state reached!")
        print("Path:", path)
        print("Path Cost:", len(path) - 1)  # Cost is the number of steps
        return True

    # Possible operations
    next_states = [
        (jug1_capacity, jug2),  # Fill Jug 1
        (jug1, jug2_capacity),  # Fill Jug 2
        (0, jug2),              # Empty Jug 1
        (jug1, 0),              # Empty Jug 2
    ]

    # Transfer from Jug1 to Jug2
    transfer = min(jug1, jug2_capacity - jug2)
    next_states.append((jug1 - transfer, jug2 + transfer))

    # Transfer from Jug2 to Jug1
    transfer = min(jug2, jug1_capacity - jug1)
    next_states.append((jug1 + transfer, jug2 - transfer))

    for state in next_states:
        if water_jug_dfs(jug1_capacity, jug2_capacity, goal_jug1, goal_jug2, visited, list(path), state[0], state[1]):
            return True

    path.pop()  # Backtrack
    return False

# User Input
jug1_capacity = int(input("Enter capacity of Jug 1: "))
jug2_capacity = int(input("Enter capacity of Jug 2: "))
initial_jug1, initial_jug2 = parse_input("Enter initial state (x,y): ")
goal_jug1, goal_jug2 = parse_input("Enter goal state (x,y): ")

# Solve using DFS
if water_jug_dfs(jug1_capacity, jug2_capacity, goal_jug1, goal_jug2, visited=None, path=None,
                  jug1=initial_jug1, jug2=initial_jug2):
    print("Solution exists!")
else:
    print("No solution.")