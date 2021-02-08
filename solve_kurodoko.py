from copy import deepcopy
import numpy as np

def unfold_list_of_lists(list_of_lists):
    return [item for sublist in list_of_lists for item in sublist]

class Kurodoko(object):
    
    def __init__(self, grid_size, set_numbers=None, set_shades=None):
        
        assert len(grid_size)==2
        self.grid_size = grid_size
        self.height = grid_size[0]
        self.width = grid_size[1]
        self.numbers = np.zeros(grid_size, dtype=int)
        # Shades are 0 if blank, 1 for white and -1 for black
        self.shades = np.zeros(grid_size, dtype=int)
        self.valid_coords = [(i,j) for i in range(self.height) for j in range(self.width)]
        if set_numbers is not None:
            self.set_numbers(set_numbers)
        # Numbers are 0 if unset, else >= 1
        if set_shades is not None:
            for coord in set_shades:
                self.set_shade_black(*coord)
    
    def numbered_cells(self):
        return [coord for coord in self.valid_coords if self.numbers[coord]>0]
    
    def limited_numbered_cells(self):
        """
        We want this to return fully solved cells only. A cell numbered N is solved if:
        - it sees N white cells [i.e., sees the number it is supposed to]
        - it sees N blank cells [i.e., it could not possibly see more white cells]
        """
        return [coord for coord in self.numbered_cells() if 
            self.count_visible_cells_from(*coord, 0) == self.count_visible_cells_from(*coord, 1)
        ]
    
    def blank_cells(self):
        return [coord for coord in self.valid_coords if self.shades[coord]==0]

    def white_cells(self):
        return [coord for coord in self.valid_coords if self.shades[coord]==1]

    def black_cells(self):
        return [coord for coord in self.valid_coords if self.shades[coord]==-1]
    
    def unsolved_cells(self):
        numbered_cells = self.numbered_cells()
        blank_cells = self.blank_cells()
        limited_cells = self.limited_numbered_cells()
        return list(set(blank_cells + numbered_cells).difference(limited_cells))
    
    def set_number(self, row, col, number):
        assert self.numbers[row, col] == 0  # Only can set numbers in blank cells
        assert self.shades[row, col] == 0   # ... and if cell is blank.
        assert type(number) is int
        self.numbers[row, col] = number
        self.shades[row, col] = 1
    
    def set_numbers(self, assignment_list):
        for row,col,number in assignment_list:
            self.set_number(row, col, number)
    
    def set_shade_black(self, row, col):
        """
        Safe way to set a cell black:
         - asserts cell isn't white already
         - asserts all neighbours are blank or white
         - makes the cell black
         - makes all neighbours white
        """
        neighbours = self.get_neighbours(row, col)
        assert self.shades[row, col] <= 0
        for coord in neighbours:
            assert self.shades[coord] >= 0
        self.shades[row, col] = -1
        for coord in neighbours:
            self.shades[coord] = 1
    
    def _is_filled_out(self):
        """
        Returns whether the grid is completed or not
        """
        return np.all(self.shades!=0)

    def _is_solved_and_valid(self):
        return self._is_filled_out() and not self._any_regions_cut_off(1)
    
    def _any_regions_cut_off(self, thresh):
        white_cells = self.get_all_white_cells(thresh=thresh)
        if len(white_cells) == 0:
            # There cannot be any cut-off regions if there are no white regions.
            return False
        else:
            one_cell = list(white_cells)[0]
            connected_cells = self.collect_contiguous_cells_from(one_cell[0], one_cell[1], thresh)
            return set(connected_cells) != set(white_cells)
    
    def _any_black_cells_adjoin_each_other(self):
        """
        This should return False if the set B of all black cells
        and the set of all neighbours of members of B are disjoint.
        """
        black_cells = self.black_cells()
        neighbours_of_black_cells = []
        for coord in black_cells:
            neighbours_of_black_cells += self.get_neighbours(*coord)
        return set.intersection(set(black_cells), set(neighbours_of_black_cells)) != set()
    
    def _cell_sees_too_much(self, row, col):
        """
        A cell sees too much if the visible white cells are greater than the number.
        """
        if self.numbers[row,col] > 0:
            return self.count_visible_cells_from(row,col,1) + 1 > self.numbers[row,col]
        else:
            return False
    
    def _cell_sees_too_little(self, row, col):
        """
        A cell sees to little if the visible blank cells are less than the number.
        """
        if self.numbers[row,col] > 0:
            return self.count_visible_cells_from(row,col,0) + 1 < self.numbers[row,col]
        else:
            return False
    
    def _any_cell_sees_wrong_number(self):
        coords = self.numbered_cells()
        any_too_much = any([self._cell_sees_too_much(*coord) for coord in coords])
        any_too_little = any([self._cell_sees_too_little(*coord) for coord in coords])
        return any_too_much or any_too_little
    
    def _any_numbered_cell_black(self):
        coords = self.numbered_cells()
        return any([self.shades[coord]==-1 for coord in coords])
    
    def _contains_contradiction(self):
        """
        Grid contains contradictions if ANY of these conditions are true:
        - any_regions_cut_off
        - black square has any numbers
        - cells_seen(1) > number  (number sees too many white cells)
        - cells_seen(0) < number  (number sees too few blank cells)
        """
        if self._any_regions_cut_off(0):
            return True
        elif self._any_black_cells_adjoin_each_other():
            return True
        elif self._any_cell_sees_wrong_number():
            return True
        elif self._any_numbered_cell_black():
            return True
        else:
            return False
    
    def count_cells_in_each_direction(self, row, col):
        center = (row,col)
        n_north = row 
        n_south = self.grid_size[0] - row - 1
        n_west = col
        n_east = self.grid_size[1] - col - 1
        n_visible = n_north + n_south + n_west + n_east
        assert n_visible == np.sum(self.grid_size) - 2
        return {
            'north':n_north,
            'south':n_south,
            'west':n_west,
            'east':n_east
        }
    
    def count_visible_cells_in_direction(self, row, col, direction, thresh):
        """
        Counts cells visible from (row,col) in direction.
        
        If thresh is 1:
            - white (1) cells visible
            - blank (0) or black (-1) cells block vision
        If thresh is 0:
            - white (1) and blank (0) cells visible
            - black (-1) cells block vision
        Self is never visible!
        """
        assert thresh in [0, 1]
        assert direction in ['north','south','east','west']
        if self.shades[row,col] < thresh:
            return 0
        n_visible = 0
        if direction == 'north':
            for i in range(row):
                shade = self.shades[row-i-1, col]
                if shade >= thresh:
                    n_visible += 1
                else:
                    return n_visible
        elif direction == 'south':
            for i in range(self.height-row-1):
                shade = self.shades[row+i+1, col]
                if shade >= thresh:
                    n_visible += 1
                else:
                    return n_visible
        elif direction == 'west':
            for i in range(col):
                shade = self.shades[row, col-i-1]
                if shade >= thresh:
                    n_visible += 1
                else:
                    return n_visible
        elif direction == 'east':
            for i in range(self.width-col-1):
                shade = self.shades[row, col+i+1]
                if shade >= thresh:
                    n_visible += 1
                else:
                    return n_visible
        return n_visible
    
    def count_visible_cells_from(self, row, col, thresh):
        assert thresh in [0,1]
        n_in_dir = sum([self.count_visible_cells_in_direction(
            row, col, direction, thresh=thresh
            ) for direction in ['south','north','east','west']
        ])
        return n_in_dir
    
    def coords_of_visible_cells_in_direction(self, row, col, direction, thresh):
        assert direction in ['north','south','east','west']
        n_cells_in_dir = self.count_visible_cells_in_direction(row, col, direction, thresh)
        if direction == 'north':
            coords = [(row-i-1,col) for i in range(n_cells_in_dir)]
        elif direction == 'south':
            coords = [(row+i+1,col) for i in range(n_cells_in_dir)]
        elif direction == 'east':
            coords = [(row,col+i+1) for i in range(n_cells_in_dir)]
        elif direction == 'west':
            coords = [(row,col-i-1) for i in range(n_cells_in_dir)]
        return coords
    
    def coords_of_visible_cells_from(self, row, col, thresh):
        coords = []
        for direction in ['north','south','east','west']:
            coords += self.coords_of_visible_cells_in_direction(row, col, direction, thresh)
        return coords
    
    def nearest_blank_cell_in_direction(self, row, col, direction):
        n_white_cells_visible = self.count_visible_cells_in_direction(row, col, direction, 1)
        n_blank_cells_visible = self.count_visible_cells_in_direction(row, col, direction, 0)
        assert n_blank_cells_visible >= n_white_cells_visible
        n_extra = n_blank_cells_visible - n_white_cells_visible
        if n_extra == 0:
            return ()
        else:
            if direction == 'north':
                return (row - n_white_cells_visible - 1, col)
            elif direction == 'south':
                return (row + n_white_cells_visible + 1, col)
            elif direction == 'east':
                return (row, col + n_white_cells_visible + 1)
            elif direction == 'west':
                return (row, col - n_white_cells_visible - 1)
    
    def nearest_blank_cells_from(self, row, col):
        coords = [self.nearest_blank_cell_in_direction(row, col, direction) for direction in ['north', 'south', 'east', 'west']]
        return [coord for coord in coords if coord]
    
    def all_nearest_blank_cells(self):
        coords = [self.nearest_blank_cells_from(*numbered_cell) for numbered_cell in self.numbered_cells()]
        return list(set(unfold_list_of_lists(coords)))
    
    def all_cells_diagonal_to_cells(self, coords):
        diagonal_coords = [self.get_diagonal_neighbours(*coord) for coord in coords]
        return list(set(unfold_list_of_lists(diagonal_coords)))
    
    def all_cells_diagonal_to_black_cells(self):
        coords = [self.get_diagonal_neighbours(*black_cell) for black_cell in self.black_cells()]
        return list(set(unfold_list_of_lists(coords)))
    
    def all_blank_cells_diagonal_to_black_cells(self):
        return list(set.intersection(set(self.all_cells_diagonal_to_black_cells()), set(self.blank_cells())))
    
    def collect_contiguous_cells_from(self, row, col, thresh):
        """
        Starting in the cell at (row,col), collect all cells that are
        contiguous with it.
        
        Contiguity requires connectedness by white cells if thresh==1,
        or by white or blank cells if thresh==0.
        """
        assert thresh in [0,1]
        cells_visited = set([(row,col)])
        cells_exhausted = set()
        while set(cells_exhausted) != set(cells_visited):
            # Pick a cell from the visited set that is not exhausted
            next_options = list(cells_visited.difference(cells_exhausted))
            assert len(next_options) > 0
            current_cell = next_options[0]
            current_row, current_col = current_cell
            # Get all neighbours
            current_neighbours = self.get_open_neighbours(current_row, current_col, thresh)
            # Add these to the visited set, and add current_cell to exhausted set.
            cells_visited = cells_visited.union(current_neighbours)
            cells_exhausted.add(current_cell)
        return cells_visited
        # cell_set =
        # for coord in cell_
        # Perform depth first search on cells
    
    def get_neighbours(self, row, col):
        neighbours = [(row-1,col), (row+1,col), (row,col-1), (row,col+1)]
        return list(set.intersection(set(neighbours), set(self.valid_coords)))
    
    def get_diagonal_neighbours(self, row, col):
        neighbours = [(row-1,col-1), (row+1,col-1), (row-1,col+1), (row+1,col+1)]
        return list(set.intersection(set(neighbours), set(self.valid_coords)))
    
    def get_open_neighbours(self, row, col, thresh):
        viable_neighbours = self.get_neighbours(row, col)
        open_neighbours = [coord for coord in viable_neighbours if self.shades[coord] >= thresh]
        return open_neighbours
    
    def get_all_white_cells(self, thresh):
        all_white_cells = set([coord for coord in self.valid_coords if self.shades[coord]>=thresh])
        return all_white_cells
        
    def number_is_valid_at(self, row, col):
        number = self.numbers[row,col]
        checks = [number > 0]
        if number > 0:
            seen = self.count_visible_cells_from(row, col, thresh=1)
            checks += [seen == number-1]
        return all(checks)
    
    
    def black_cell_is_valid_at(self, row, col):
        shade = self.shades[row,col]
        neighbours = self.get_neighbours(row, col)
        checks = [self.shades[neighbour]==1 for neighbour in neighbours]
        checks += [shade==-1]
        return all(checks)

        
    def cell_is_valid(self, row, col):
        checks = []
        if self.numbers[row,col] > 0:
            checks += [self.shades[row,col] >= 0]
            return all(checks + [self.number_is_valid_at(row,col)])
        elif self.shades[row,col] == -1:
            checks += [self.numbers[row,col] == 0]
            return all(checks + [self.black_cell_is_valid_at(row,col)])
        else:
            return True
    
    def grid_contains_no_errors(self):
        checks = [self.cell_is_valid(*coord) for coord in self.valid_coords]
        checks += [not self._any_regions_cut_off(thresh=0)]
        return all(checks)
    
    def cell_sees_max_possible(self, row, col, thresh):
        """
        Returns TRUE if the cell at (row, col) can currently see a number
        of cells equal to its number.
        """
        assert self.numbers[row,col] > 0
        return self.count_visible_cells_from(row,col,thresh)+1 == self.numbers[row,col]
    
    def deduce_cell_maxes_visible_space(self, row, col):
        if self.cell_sees_max_possible(row, col, 0):
            ensure_white_coords = self.coords_of_visible_cells_from(row, col, 0)
            for coord in ensure_white_coords:
                self.shades[coord] = 1
    
    def deduce_number_already_satisfied(self, row, col):
        if self.count_visible_cells_from(row, col, 1) + 1 == self.numbers[row, col]:
            # Visible WHITE cells satisfy number.
            # So, now get nearest visible BLANK cells and make them BLACK.
            coords = self.nearest_blank_cells_from(row, col)
            for coord in coords:
                self.set_shade_black(*coord)
    
    def cell_cannot_be_black(self, row, col):
        fake_grid = Kurodoko(self.grid_size, set_shades=self.black_cells())
        fake_grid.set_shade_black(row, col)
        # If any regions are now cut off, then cell cannot be black; return True.
        return fake_grid._any_regions_cut_off(0)
    
    def deduce_dont_split_grid(self, row, col):
        if self.shades[row,col] == 0 and self.cell_cannot_be_black(row, col):
            self.shades[row, col] = 1

    def solve_grid_with_deductions(self):
        prev_grid_state = self.shades[:].copy()
        state_changed = True
        self.solving_iterations = 0
        while state_changed and (self.solving_iterations < 1000):
            for coord in self.valid_coords:
                if self.numbers[coord] > 0:
                    self.deduce_cell_maxes_visible_space(*coord)
                    self.deduce_number_already_satisfied(*coord)
                if self.shades[coord] == 0:
                    self.deduce_dont_split_grid(*coord)
            next_grid_state = self.shades[:]
            if np.all(prev_grid_state == next_grid_state):
                state_changed = False
            else:
                prev_grid_state = next_grid_state.copy()
            self.solving_iterations += 1
    
    def clone(self):
        return deepcopy(self)
    
    def get_cant_be_black_candidates(self):
        return self.all_nearest_blank_cells() + self.all_cells_diagonal_to_black_cells() + self.all_cells_diagonal_to_cells(self.numbered_cells())
    
    def get_cant_be_white_candidates(self):
        return self.all_nearest_blank_cells()
    
    def check_must_not_be_black(self, row, col):
        fake_grid = self.clone()
        fake_grid.shades[(row, col)] = -1
        return fake_grid._contains_contradiction()
    
    def check_must_not_be_white(self, row, col):
        fake_grid = self.clone()
        fake_grid.shades[(row, col)] = 1
        return fake_grid._contains_contradiction()
    
    def solve_grid_with_deductions_and_single_conjectures(self):
        prev_grid_state = self.shades[:].copy()
        state_changed = True
        self.solving_iterations = 0
        while state_changed and (self.solving_iterations < 1000):
            for coord in self.blank_cells():
                if self.numbers[coord] > 0:
                    self.deduce_cell_maxes_visible_space(*coord)
                    self.deduce_number_already_satisfied(*coord)
                if self.shades[coord] == 0:
                    self.deduce_dont_split_grid(*coord)
            for coord in self.get_cant_be_black_candidates():
                if self.check_must_not_be_black(*coord):
                    self.shades[coord] = 1
            for coord in self.get_cant_be_white_candidates():
                if self.check_must_not_be_white(*coord):
                    self.set_shade_black(*coord)
            next_grid_state = self.shades[:]
            if np.all(prev_grid_state == next_grid_state):
                state_changed = False
            else:
                prev_grid_state = next_grid_state.copy()
            self.solving_iterations += 1
