# Requirements:
# x grid of m x n cells
# x all cells initially blank
# x some cells initially designated with digits and are white
# x cells can become black
# x cells can become white
# x count visible cells in any direction
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
    assert grid.numbers.shape == (5,7)

def test_grid_initially_blank():
    grid = Kurodoko((5,5))
    assert np.all(grid.numbers == 0)

def test_set_number():
    grid = Kurodoko((5,5))
    grid.set_number(0,0,9)
    assert grid.numbers[0,0] == 9

def test_set_grid():
    grid = Kurodoko((5,5))
    grid.set_numbers([(0,0,9), (1,1,3), (1,2,7)])
    assert grid.numbers[0,0] == 9
    assert grid.numbers[1,1] == 3
    assert grid.numbers[0,1] == 0
    assert grid.shades[0,0] == grid.shades[1,1] == 1
    assert grid.shades[0,1] == 0

def test_check_grid_is_solved():
    # Grid is solved when all squares are black or white
    grid = Kurodoko((3,3))
    grid.shades = np.array([[-1,1,1], [1,-1,1], [1,1,1]])
    assert grid.grid_filled_out()

def test_count_cells_in_each_direction():
    grid = Kurodoko((9,4))
    for i in range(9):
        for j in range(4):
            assert sum(grid.count_cells_in_each_direction(i,j).values()) == 11

grid_5_5_incomplete = Kurodoko((5,5))
grid_5_5_incomplete.shades = np.array([
    [ 1, 1, 1, 1, 1],
    [-1, 1, 1,-1, 1],
    [ 1,-1, 1, 1,-1],
    [ 1, 1, 1, 0, 0],
    [ 1, 1,-1, 0, 0]]
)

def test_count_cells_from_3_2_correct():
    assert grid_5_5_incomplete.count_visible_cells_in_direction(3,2,'north',1) == 3
    assert grid_5_5_incomplete.count_visible_cells_in_direction(3,2,'south',1) == 0
    assert grid_5_5_incomplete.count_visible_cells_in_direction(3,2,'west',1) == 2
    assert grid_5_5_incomplete.count_visible_cells_in_direction(3,2,'east',1) == 0
    assert grid_5_5_incomplete.count_visible_cells_in_direction(3,2,'north',0) == 3
    assert grid_5_5_incomplete.count_visible_cells_in_direction(3,2,'south',0) == 0
    assert grid_5_5_incomplete.count_visible_cells_in_direction(3,2,'west',0) == 2
    assert grid_5_5_incomplete.count_visible_cells_in_direction(3,2,'east',0) == 2

def test_count_cells_from_4_3_correct():
    assert grid_5_5_incomplete.count_visible_cells_in_direction(4,3,'north',1) == 0
    assert grid_5_5_incomplete.count_visible_cells_in_direction(4,3,'south',1) == 0
    assert grid_5_5_incomplete.count_visible_cells_in_direction(4,3,'west',1) == 0
    assert grid_5_5_incomplete.count_visible_cells_in_direction(4,3,'east',1) == 0
    assert grid_5_5_incomplete.count_visible_cells_in_direction(4,3,'north',0) == 2
    assert grid_5_5_incomplete.count_visible_cells_in_direction(4,3,'south',0) == 0
    assert grid_5_5_incomplete.count_visible_cells_in_direction(4,3,'west',0) == 0
    assert grid_5_5_incomplete.count_visible_cells_in_direction(4,3,'east',0) == 1

def test_count_visible_cells_from():
    assert grid_5_5_incomplete.count_visible_cells_from(2,2,1) == 4
    assert grid_5_5_incomplete.count_visible_cells_from(3,3,1) == 0
    assert grid_5_5_incomplete.count_visible_cells_from(3,3,0) == 6
    assert grid_5_5_incomplete.count_visible_cells_from(0,1,0) == 5

def test_cell_is_valid():
    grid = Kurodoko((3,3))
    grid.numbers 
    grid.shades = np.array([[-1,1,1], [1,-1,1], [1,1,1]])
    # assert /