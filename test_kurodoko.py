# Requirements:
# x grid of m x n cells
# x all cells initially blank
# x some cells initially designated with digits and are white
# x cells can become black
# x cells can become white
# x count visible cells in any direction
# x detect whether space of white cells is contiguous
# x detect whether black cells cut off any portion of the grid
#     x return set of white or blank cells
#     x determine whether all white cells in group contiguous with one of them
# x confirm whether grid is solved and valid. Requires checking contiguity, and:
#     x check number matches white squares seen
#     x check black square's neighbours all white
#     x iterate through cells and make these checks
# - logical deductions:
#     x if number equals visible blank space, then all blank cells white
#     x if number equals visible white space, then next blank cells black
#     x when setting a cell as black, all neighbours must be white
#     x if making a cell black would lead to discontiguous white areas, it must be white
#     - if number is larger than amount of space in row, then some must spill into column
#     - if adding a white space introduces a contradiction, it must be black
#     - if adding a black space introduces a contradiction, it must be white
# - can print grid
#     - with numbers
#     - with blank vs white vs black squares
# x iterate over possible deducations until grid is solved

from solve_kurodoko import *

grid_5_5_incomplete = Kurodoko((5,5))
grid_5_5_incomplete.shades = np.array([
    [ 1, 1, 1, 1, 1],
    [-1, 1, 1,-1, 1],
    [ 1,-1, 1, 1,-1],
    [ 1, 1, 1, 0, 0],
    [ 1, 1,-1, 0, 1]]
)

grid_3_3_incomplete = Kurodoko((3,3))
grid_3_3_incomplete.set_numbers([(0,0,5), (1,2,2)])

grid_3_3_complete = Kurodoko((3,3))
grid_3_3_complete.numbers = np.array([[5,3,4], [3,0,2], [4,2,0]])
grid_3_3_complete.shades = np.array([[1,1,1], [1,-1,1], [1,1,-1]])

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
    assert grid._grid_filled_out()

def test_count_cells_in_each_direction():
    grid = Kurodoko((9,4))
    for i in range(9):
        for j in range(4):
            assert sum(grid.count_cells_in_each_direction(i,j).values()) == 11

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

def test_valid_coords_generates_correctly():
    grid = Kurodoko((2,4))
    valid_coords = sorted([(0,0), (1,0), (0,1), (1,1), (0,2), (1,2), (0,3), (1,3)])
    assert sorted(grid.valid_coords) == valid_coords

def test_get_neighbours():
    grid = Kurodoko((2,4))
    assert sorted(grid.get_neighbours(0,0)) == sorted([(0,1), (1,0)])
    assert sorted(grid.get_neighbours(1,2)) == sorted([(1,1), (1,3), (0,2)])

def test_get_open_neighbours():
    assert grid_5_5_incomplete.get_open_neighbours(0,0,0) == [(0,1)]
    assert set(grid_5_5_incomplete.get_open_neighbours(2,2,0)) == set([(2,3), (1,2), (3,2)])
    assert set(grid_5_5_incomplete.get_open_neighbours(2,3,0)) == set([(2,2), (3,3)])
    assert grid_5_5_incomplete.get_open_neighbours(2,3,1) == [(2,2)]

def test_collect_contiguous_cells_from():
    grid = Kurodoko((3,3))
    grid.shades = np.ones_like(grid.shades)
    grid.shades[(0,0)] = -1
    grid.shades[(1,1)] = -1
    grid.shades[(2,2)] = -1
    top_right_cells = grid.collect_contiguous_cells_from(0,1,1)
    assert top_right_cells == set([(0,1), (0,2), (1,2)])
    bottom_left_cells = grid.collect_contiguous_cells_from(1,0,1)
    assert bottom_left_cells == set([(1,0), (2,0), (2,1)])
    incomplete_grid_cells_strict = grid_5_5_incomplete.collect_contiguous_cells_from(0,0,1)
    incomplete_grid_cells_lax = grid_5_5_incomplete.collect_contiguous_cells_from(0,0,0)
    assert len(incomplete_grid_cells_strict) == 16
    assert len(incomplete_grid_cells_lax) == 20

def test_get_all_white_cells():
    white_cells = grid_3_3_complete.get_all_white_cells(thresh=1)
    expected_cells = [(0,0), (0,1), (0,2), (1,0), (1,2), (2,0), (2,1)]
    assert sorted(white_cells) == sorted(expected_cells)
    white_cells = grid_3_3_incomplete.get_all_white_cells(thresh=1)
    assert sorted(white_cells) == sorted([(0,0), (1,2)])
    white_cells = grid_3_3_incomplete.get_all_white_cells(thresh=0)
    assert sorted(white_cells) == sorted(grid_3_3_incomplete.valid_coords)

def test_grid_for_contiguity():
    assert not grid_3_3_complete._any_regions_cut_off(1)
    grid = Kurodoko((3,3))
    grid.shades[0,1] = -1
    grid.shades[1,0] = -1
    assert grid._any_regions_cut_off(0)
    assert grid_5_5_incomplete._any_regions_cut_off(1)
    assert not grid_5_5_incomplete._any_regions_cut_off(0)

def test_number_is_valid_at():
    grid = Kurodoko((3,4))
    grid.set_numbers([(0,0,5), (1,1,4), (2,2,2)])
    grid.shades = np.ones((3,4),dtype=int)
    grid.shades[1,2] = -1
    grid.shades[2,0] = -1
    grid.shades[2,3] = -1
    for i in range(3):
        assert grid.number_is_valid_at(i, i)
    grid.numbers[0,0] = 6
    grid.numbers[1,1] = 3
    grid.numbers[2,2] = 0
    for i in range(3):
        assert not grid.number_is_valid_at(i, i)

def test_black_cells_valid():
    assert grid_5_5_incomplete.black_cell_is_valid_at(2,1)
    assert not grid_5_5_incomplete.black_cell_is_valid_at(2,2)
    grid = Kurodoko((5,10))
    grid.shades = np.ones_like(grid.shades, dtype=int)
    grid.shades[3,4] = -1
    grid.shades[4,4] = -1
    grid.shades[3,6] = -1
    assert not grid.black_cell_is_valid_at(3,4)
    assert not grid.black_cell_is_valid_at(4,4)
    assert grid.black_cell_is_valid_at(3,6)

def test_cell_is_valid():
    """
    Example grid:
    
    5 . . 5
    . 4 # #
    # . 2 #
    
    There should be a number error at (0,3) and block errors at (1,2), (1,3), and (2,3).
    """
    for coord in grid_3_3_complete.valid_coords:
        assert grid_3_3_complete.cell_is_valid(*coord)
    grid = Kurodoko((3,4))
    grid.set_numbers([(0,0,5), (1,1,4), (2,2,2), (0,3,5)])
    grid.shades = np.ones((3,4),dtype=int)
    set_as_black = [(1,2), (2,0), (2,3), (1,3)]
    for coord in set_as_black:
        grid.shades[coord] = -1
    cell_contains_an_error = np.array([[0,0,0,1], [0,0,1,1], [0,0,0,1]])
    for coord in grid.valid_coords:
        assert grid.cell_is_valid(*coord) == (cell_contains_an_error[coord]==0)

def test_grid_contains_no_errors():
    # Complete example has no errors
    assert grid_3_3_complete.grid_contains_no_errors()

    # Example without errors
    grid = Kurodoko((5,5), set_numbers = [(0,0,9), (2,2,5)], set_shades = [(2,3), (3,2)])
    grid.shades[grid.shades!=-1] = 1
    assert grid.grid_contains_no_errors()

    # Add a black cell adjacent to another black cell
    grid.shades[2,4] = -1
    assert not grid.grid_contains_no_errors()

    # Make a grid with an error of number
    grid = Kurodoko((5,5), [(0,0,8)])
    grid.shades[grid.shades!=-1] = 1
    assert not grid.grid_contains_no_errors()

    # Fail because of disconnected parts of grid
    grid = Kurodoko((5,5))
    grid.shades = np.eye(5, dtype=int)
    grid.shades[grid.shades==1] = -1
    grid.shades[grid.shades==0] = 1
    assert not grid.grid_contains_no_errors()

def test_deduce_max_spacer():
    assert grid_3_3_incomplete.cell_sees_max_possible(0,0,0)
    assert not grid_3_3_incomplete.cell_sees_max_possible(1,2,0)

def test_get_coords_of_cells_in_direction():
    assert grid_5_5_incomplete.coords_of_visible_cells_in_direction(1,2,'north',0) == [(0,2)]
    assert grid_5_5_incomplete.coords_of_visible_cells_in_direction(1,2,'south',0) == [(2,2), (3,2)]
    assert grid_5_5_incomplete.coords_of_visible_cells_in_direction(1,2,'east',0) == []
    assert grid_5_5_incomplete.coords_of_visible_cells_in_direction(1,2,'west',0) == [(1,1)]
    assert set(grid_5_5_incomplete.coords_of_visible_cells_from(1,2,0)) == set([
        (0,2), (2,2), (3,2), (1,1)
    ])

def test_deduce_cell_maxes_visible_space():
    grid = Kurodoko((3,3))
    grid.set_numbers([(0,0,5), (1,2,2)])
    assert grid.shades[1,0] == grid.shades[0,2] == 0
    grid.deduce_cell_maxes_visible_space(0,0)
    assert grid.shades[1,0] == grid.shades[0,2] == 1

def test_find_nearest_blank_cell_in_direction():
    assert grid_5_5_incomplete.nearest_blank_cell_in_direction(3,0,'east') == (3,3)
    assert grid_5_5_incomplete.nearest_blank_cell_in_direction(4,4,'north') == (3,4)
    assert grid_5_5_incomplete.nearest_blank_cell_in_direction(1,1,'east') == ()
    assert grid_5_5_incomplete.nearest_blank_cells_from(4,4) == [(3,4), (4,3)]
    assert grid_5_5_incomplete.nearest_blank_cells_from(3,1) == [(3,3)]
    assert grid_5_5_incomplete.nearest_blank_cells_from(0,1) == []

def test_deduce_number_already_satisfied():
    grid = Kurodoko((3,3), set_numbers=[(0,0,5), (1,2,2)])
    grid.deduce_cell_maxes_visible_space(0,0)
    assert grid.shades[2,2] == 0
    # Cell (1,2) now has one black neighbour (1,1), one white neighbour (2,0),
    # and one blank neighbour (2,2). Since its number is 2 and it can see
    # a cell already, it should deduce that it must place a black cell in (2,2).
    grid.deduce_number_already_satisfied(1,2)
    assert grid.shades[2,2] == -1

def test_get_cells_by_type():
    grid = Kurodoko((3,3), set_numbers=[(0,0,5), (1,2,2)])
    grid.deduce_cell_maxes_visible_space(0,0)
    assert grid.numbered_cells() == [(0,0), (1,2)]
    assert grid.white_cells() == [(0,0), (0,1), (0,2), (1,0), (1,2), (2,0)]
    assert grid.black_cells() == []
    assert grid.blank_cells() == [(1,1), (2,1), (2,2)]

def test_deduce_dont_split_grid():
    grid = Kurodoko((4,4), set_shades=[(3,0), (2,1), (0,3)])
    assert grid.shades[1,2]==0
    assert grid.cell_cannot_be_black(1,2)
    grid.deduce_dont_split_grid(1,2)
    assert grid.shades[1,2]==1

def test_solve_a_solvable_grid():
    grid = Kurodoko((5,5), set_numbers=[(0,0,4), (0,4,6), (2,1,9), (2,3,5), (4,0,2)])
    for i in range(5):
        for coord in grid.valid_coords:
            grid.deduce_dont_split_grid(*coord)
            if grid.numbers[coord] > 0:
                grid.deduce_cell_maxes_visible_space(*coord)
                grid.deduce_number_already_satisfied(*coord)
    assert grid._grid_filled_out()

def test_get_exhausted_numbered_cells():
    grid = Kurodoko((3,3), set_numbers=[(0,0,5), (2,2,3)])
    assert grid.limited_numbered_cells() == []
    grid.deduce_cell_maxes_visible_space(0,0)
    assert grid.limited_numbered_cells() == [(0,0)]

def test_get_unsolved_cells():
    grid = Kurodoko((4,4), set_numbers=[(1,1,7), (0,3,2)])
    """
    Initial:     After         After         After
                 maxes_space:  sees_max:     dont_split:
    ? ? ? 2      ? . ? 2       ? . X 2       ? . X 2
    ? 7 ? ?      . 7 . .       . 7 . .       . 7 . .
    ? ? ? ?      ? . ? ?       ? . . X       ? . . X
    ? ? ? ?      ? . ? ?       ? . ? .       ? . . .
    """
    assert set(grid.unsolved_cells()) == set(grid.valid_coords)
    grid.deduce_cell_maxes_visible_space(1,1)
    assert set(grid.unsolved_cells()) == set([(0,0), (0,2), (0,3), (2,0), (2,2), (2,3), (3,0), (3,2), (3,3)])
    grid.deduce_number_already_satisfied(0,3)
    assert set(grid.unsolved_cells()) == set([(0,0), (2,0), (3,0), (3,2)])
    grid.deduce_dont_split_grid(3,2)
    assert set(grid.unsolved_cells()) == set([(0,0), (2,0), (3,0)])

def test_solve_grid():
    grid = Kurodoko((4,4), set_numbers=[(1,1,7), (0,3,2), (2,0,4)])
    grid.solve_grid()
    assert grid._is_solved_and_valid()
    assert grid.solving_iterations == 3
