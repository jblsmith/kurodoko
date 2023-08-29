import datetime
from flask import Flask, render_template
app = Flask(__name__)
import os

class MinimalKurodoko(object):
    def __init__(self, grid_size, numbers):
        self.grid_size = grid_size
        self.numbers = numbers

def load_kurodoko_from_file(filepath):
    with open(filepath) as textfile:
        text = textfile.readlines()
    text_lines = [line.strip().split(",") for line in text]
    grid_size = (len(text_lines), len(text_lines[0]))
    return MinimalKurodoko(grid_size, text_lines)

def get_grid_and_solution_for_puzzle(puzzle_name):
    grid = load_kurodoko_from_file(f"./grids/{puzzle_name}.csv")
    solution_grid = load_kurodoko_from_file(f"./grids/{puzzle_name}-solution.csv")
    solution = " ".join([" ".join(item) for item in solution_grid.numbers])
    return grid, solution

@app.route('/')
def demo_puzzle():
    grid, solution = get_grid_and_solution_for_puzzle(puzzle_name="7x7-01")
    return render_template('index.html', grid=grid, solution=solution, next_name="puzzle_7x7-02")

@app.route('/puzzle_<name>')
def show_puzzle(name):
    puzzle_names = ['7x7-01','7x7-02','7x7-03','7x7-04','7x7-05']
    puzzle_links = {name:next_name for name,next_name in zip(puzzle_names, puzzle_names[1:]+puzzle_names[:1])}
    asset_path_name = f"./grids/{name}-solution.csv"
    assert os.path.exists(asset_path_name)
    next_name = "puzzle_" + puzzle_links[name]
    grid, solution = get_grid_and_solution_for_puzzle(puzzle_name=name)
    return render_template('index.html', grid=grid, solution=solution, next_name=next_name)


# [x] Display a grid
# [x] Grid cells are clickable
# [x]   click once to make it blank
# [x]   click twice to make it black
# [x]   click thrice to make it unknown again (start point)
# [x] Button to verify grid
# [x]   Count errors
# [ ]   Display errors
# [ ]   Display solution
# [ ] Button to undo action?
# [x] Button to clear grid
# [x] Button to request new grid
# [ ] Button to generate random grid from scratch?
