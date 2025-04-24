from constraint import Problem
import matplotlib.pyplot as plt
import networkx as nx

# Define the problem
problem = Problem()

# Variables (Regions of Australia)
states = ["Western Australia", "Northern Territory", "South Australia", "Queensland", "New South Wales", "Victoria", "Tasmania"]

# Domains (Colors available)
colors = {"Red": "#FF0000", "Blue": "#0000FF", "Green": "#008000"}

# Take user input for first two initial color constraints
initial_colors = {}
print("Enter initial colors for the first two regions (Red/Blue/Green), then colors will be assigned automatically:")
for i in range(2):
    state = states[i]
    color = input(f"{state}: ").strip().capitalize()
    if color in colors:
        initial_colors[state] = color

# Add variables to the problem
for state in states:
    if state in initial_colors:
        problem.addVariable(state, [initial_colors[state]])  # Fixed color
    else:
        problem.addVariable(state, list(colors.keys()))  # Allow any color

# Constraints: Adjacent states cannot have the same color
adjacent_states = [
    ("Western Australia", "Northern Territory"),
    ("Western Australia", "South Australia"),
    ("Northern Territory", "South Australia"),
    ("Northern Territory", "Queensland"),
    ("South Australia", "Queensland"),
    ("South Australia", "New South Wales"),
    ("South Australia", "Victoria"),
    ("Queensland", "New South Wales"),
    ("New South Wales", "Victoria")
]

for state1, state2 in adjacent_states:
    problem.addConstraint(lambda c1, c2: c1 != c2, (state1, state2))

# Solve the problem
solution = problem.getSolution()

# Print the solution
if solution:
    for state, color in solution.items():
        print(f"{state}: {color}")

    # Visualizing the map
    G = nx.Graph()
    
    # Add nodes
    for state in states:
        G.add_node(state)
    
    # Add edges (adjacent states)
    for state1, state2 in adjacent_states:
        G.add_edge(state1, state2)
    
    # Positioning the nodes
    pos = {
        "Western Australia": (-2, 0),
        "Northern Territory": (-1, 1),
        "South Australia": (-1, -1),
        "Queensland": (1, 1),
        "New South Wales": (2, 0),
        "Victoria": (1, -1),
        "Tasmania": (1, -2)  # Tasmania is placed below
    }
    
    # Assign colors based on solution
    node_colors = [colors[solution[state]] for state in states]

    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color="black", node_size=3000, font_size=10, font_weight="bold")
    plt.title("Australia Map Coloring")
    plt.show()
else:
    print("No solution found.")