# Requirements:
# - grid of m x n cells
# - all cells initially blank
# - some cells initially designated with digits and are white
# - cells can become black
# - cells can become white
# - detect whether space of white cells is contiguous
# - detect whether black cells cut off any portion of the grid
# - confirm whether grid is solved and valid
# - logical deductions:
#     - if number is larger than amount of space in row, then some must spill into column
#     - if adding a white space introduces a contradiction, it must be black
#     - if adding a black space introduces a contradiction, it must be white
# - can print grid
#     - with numbers
#     - with blank vs white vs black squares


from solve_kurodoko import *

def test_make_grid():
    grid = Kurodoko((5,7))
    assert grid.cells.shape == (5,7)