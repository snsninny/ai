import tkinter as tk

# Hill Climbing function for Block World Problem
def hill_climbing_block_world(initial, target):
    steps = []
    block_details = []

    # Define numbering: Start from -3, -2, -1, 0
    initial_numbering = list(range(-3, 1))  # [-3, -2, -1, 0]
    goal_numbering = list(range(len(target)))  # [0, 1, 2, 3]

    steps.append(f"Initial State: {initial} -> {initial_numbering}")
    block_details.append((initial, initial_numbering))

    # Step 1: Remove from top-to-bottom in the order A → D → C → B
    remove_order = "ADCB"
    for char in remove_order:
        initial = initial.replace(char, "", 1)  # Remove only first occurrence
        if initial_numbering:
            initial_numbering = initial_numbering[1:]
        steps.append(f"Step {len(steps)}: {initial} -> {initial_numbering}")
        block_details.append((initial, initial_numbering))

    # Step 2: Rebuild ABCD step by step
    current_solution = ""
    current_numbering = []
    for i in range(len(target)):
        current_solution += target[i]
        current_numbering.append(goal_numbering[i])
        steps.append(f"Step {len(steps)}: {current_solution} -> {current_numbering}")
        block_details.append((current_solution, current_numbering))

    steps.append(f"Goal State: {target} -> {goal_numbering}")
    block_details.append((target, goal_numbering))

    return steps, block_details

# GUI Implementation
def start_algorithm():
    initial_state = initial_entry.get().upper()
    target_state = target_entry.get().upper()

    if not initial_state.isalpha() or not target_state.isalpha():
        result_label.config(text="Please enter valid states containing only letters.")
        return

    if len(initial_state) != len(target_state):
        result_label.config(text="Initial and Goal states must have the same length.")
        return

    steps, block_details = hill_climbing_block_world(initial_state, target_state)
    result_text = "\n".join(steps)
    result_label.config(text=result_text)

# Main Tkinter Window
root = tk.Tk()
root.title("Hill Climbing: Block World Problem")

# Input Section
tk.Label(root, text="Enter Initial State (e.g., BCDA):").pack(pady=5)
initial_entry = tk.Entry(root)
initial_entry.pack(pady=5)

tk.Label(root, text="Enter Goal State (e.g., ABCD):").pack(pady=5)
target_entry = tk.Entry(root)
target_entry.pack(pady=5)

tk.Button(root, text="Start", command=start_algorithm).pack(pady=10)

# Result Section
result_label = tk.Label(root, text="", justify="left", anchor="w")
result_label.pack(pady=10)

root.mainloop()