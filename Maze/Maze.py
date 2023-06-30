import tkinter as tk
import random
import time

# Constants
GRID_SIZE = 30
SQUARE_SIZE = 20
LINE_DELAY = 0.00001

maze = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

root = tk.Tk()
canvas = tk.Canvas(root, width=GRID_SIZE*SQUARE_SIZE, height=GRID_SIZE*SQUARE_SIZE)
canvas.pack()

green_squares = []
blue_squares = []
black_squares = []
yellow_squares = []


def draw_maze():
    canvas.delete("all")

   #for i in range(GRID_SIZE+1):
       # canvas.create_line(0, i*SQUARE_SIZE, GRID_SIZE*SQUARE_SIZE, i*SQUARE_SIZE)
       # canvas.create_line(i*SQUARE_SIZE, 0, i*SQUARE_SIZE, GRID_SIZE*SQUARE_SIZE)

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if maze[row][col]:
                canvas.create_rectangle(
                    col*SQUARE_SIZE,
                    row*SQUARE_SIZE,
                    (col+1)*SQUARE_SIZE,
                    (row+1)*SQUARE_SIZE,
                    fill="black"
                )

    for square in green_squares:
        row, col = square
        canvas.create_rectangle(
            col*SQUARE_SIZE,
            row*SQUARE_SIZE,
            (col+1)*SQUARE_SIZE,
            (row+1)*SQUARE_SIZE,
            outline="green",
            fill="green"
        )

    for square in blue_squares:
        row, col = square
        canvas.create_rectangle(
            col*SQUARE_SIZE,
            row*SQUARE_SIZE,
            (col+1)*SQUARE_SIZE,
            (row+1)*SQUARE_SIZE,
            outline="gray",
            fill="gray"
        )
        
    for square in yellow_squares:
        row, col = square
        canvas.create_rectangle(
            col*SQUARE_SIZE,
            row*SQUARE_SIZE,
            (col+1)*SQUARE_SIZE,
            (row+1)*SQUARE_SIZE,
            outline="yellow",
            fill="yellow"
        )

def add_line():
    row = random.randint(0, GRID_SIZE - 1)
    col = random.randint(0, GRID_SIZE - 1)

    if random.choice([True, False]):
        maze[row][col] = True
    else:
        maze[row][col] = True
    
    draw_maze()
    root.update()

def handle_click(event):
    if len(green_squares) < 2: 
        col = event.x // SQUARE_SIZE
        row = event.y // SQUARE_SIZE

        if row >= 0 and row < GRID_SIZE and col >= 0 and col < GRID_SIZE:
            green_squares.append((row, col))

            draw_maze()

            if len(green_squares) == 2:
                complete_maze()

def build_maze():
    for _ in range(GRID_SIZE * GRID_SIZE // 3):  # Number of lines 
        add_line()
        time.sleep(LINE_DELAY)

def heuristic(node, goal):
    # Calculate the Manhattan distance between two nodes
    row1, col1 = node
    row2, col2 = goal
    return abs(row1 - row2) + abs(col1 - col2)

def get_adjacent_nodes(node):
    row, col = node
    adjacent_nodes = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

    for direction in directions:
        adj_row = row + direction[0]
        adj_col = col + direction[1]

        if (
            adj_row >= 0 and adj_row < GRID_SIZE and
            adj_col >= 0 and adj_col < GRID_SIZE and
            (adj_row, adj_col) not in black_squares
        ):
            adjacent_nodes.append((adj_row, adj_col))

    return adjacent_nodes

def a_star(start, goal):
    open_list = [start]
    closed_list = set()
    
    g_scores = {green_squares[0]: 0}
    f_scores = {green_squares[0]: heuristic(green_squares[0], green_squares[1])}
    parents = {}

    while open_list:
        # Find the node with the lowest f score
        current = min(open_list, key=lambda node: f_scores[node])

        if current == goal:
            # Path found, reconstruct and return the path
            path = []
            while current in parents:
                path.insert(0, current)
                current = parents[current]
            return path

        # Move current node from open list to closed list
        open_list.remove(current)
        closed_list.add(current)

        adjacent_nodes = get_adjacent_nodes(current)

        for adjacent_node in adjacent_nodes:
            if adjacent_node in closed_list:
                continue

            # Calculate the tentative g score
            g_score = g_scores[current] + 1

            if adjacent_node not in open_list:
                open_list.append(adjacent_node)
            elif g_score >= g_scores[adjacent_node]:
                continue

            g_scores[adjacent_node] = g_score
            f_scores[adjacent_node] = g_score + heuristic(adjacent_node, goal)

            parents[adjacent_node] = current

            blue_squares.append(adjacent_node)

        draw_maze()
        root.update()
        time.sleep(LINE_DELAY)

    return []


def complete_maze():  

    print("Maze completed!")
    print("Green Squares:", green_squares)
    
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if maze[row][col]:
                black_squares.append((row, col))
    
    print("Black Squares:", black_squares)
    a_star(green_squares[0], green_squares[1])
    print("Blue Squares:", blue_squares)
    path = a_star(green_squares[0], green_squares[1])
    print("Path:", path)
    yellow_squares.extend(path[:-1])
    
    draw_maze()
    row, col = green_squares[1]
    canvas.create_rectangle(
            col*SQUARE_SIZE,
            row*SQUARE_SIZE,
            (col+1)*SQUARE_SIZE,
            (row+1)*SQUARE_SIZE,
            outline="green",
            fill="green"
        ) 

build_maze()
canvas.bind("<Button-1>", handle_click)
root.mainloop()