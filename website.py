import datetime
from flask import Flask, render_template
import numpy as np
app = Flask(__name__)

from solve_kurodoko import Kurodoko, make_kurodoko_from_file

grid = make_kurodoko_from_file("example_grid.csv")
outcome = grid.solve_grid_with_deductions_and_single_conjectures(branched=True)
solution = " ".join(np.concatenate(grid.shades).astype(str))

@app.route('/')
def hello_world():
    return render_template('index.html', grid=grid, solution=solution)

# [x] Display a grid
# [x] Grid cells are clickable
# [x]   click once to make it blank
# [x]   click twice to make it black
# [x]   click thrice to make it unknown again (start point)
# [ ] Button to verify grid
# [ ]   Count errors
# [ ]   Display errors
# [ ]   Display solution
# [ ] Button to undo action?
# [ ] Button to clear grid
# [ ] Button to request new grid
# [ ] Button to generate random grid from scratch?
