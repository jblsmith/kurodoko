import datetime
from flask import Flask, render_template
import numpy as np
app = Flask(__name__)

from solve_kurodoko import Kurodoko, make_kurodoko_from_file

grid = make_kurodoko_from_file("./grids/7x7-01.csv")
outcome = grid.solve_grid_with_deductions_and_single_conjectures(branched=True)
solution = " ".join(np.concatenate(grid.shades).astype(str))



@app.route('/')
def demo_puzzle():
    return render_template('index.html', grid=grid, solution=solution)


puzzle_names = ['7x7-01','7x7-02','7x7-03','7x7-04']
puzzle_links = {name:next_name for name,next_name in zip(puzzle_names, puzzle_names[1:]+puzzle_names[:1])}

@app.route('/puzzle_<name>')
def show_puzzle(name):
    assert name in puzzle_names
    next_name = "puzzle_" + puzzle_links[name]
    filename = "./grids/"+name+".csv"
    grid = make_kurodoko_from_file(filename)
    grid.solve_grid_with_deductions_and_single_conjectures(branched=True)
    solution = " ".join(np.concatenate(grid.shades).astype(str))
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
