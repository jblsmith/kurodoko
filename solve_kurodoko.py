import numpy as np

class Kurodoko(object):
    
    def __init__(self, grid_size):
        
        assert len(grid_size)==2
        self.grid_size = grid_size
        self.height = grid_size[0]
        self.width = grid_size[1]
        self.numbers = np.zeros(grid_size)
        # Numbers are 0 if unset, else >= 1
        self.shades = np.zeros(grid_size)
        # Shades are 0 if blank, 1 for white and -1 for black
        self.visible_in_row = np.zeros(grid_size)
        self.visible_in_column = np.zeros(grid_size)
        self.valid_coords = [(i,j) for i in range(self.height) for j in range(self.width)]
    
    def set_number(self, row, col, number):
        assert self.numbers[row, col] == 0  # Only can set numbers in blank cells
        assert self.shades[row, col] == 0   # ... and if cell is blank.
        assert type(number) is int
        self.numbers[row, col] = number
        self.shades[row, col] = 1
    
    def set_numbers(self, assignment_list):
        for row,col,number in assignment_list:
            self.set_number(row, col, number)
    
    def grid_filled_out(self):
        """
        Returns whether the grid is completed or not
        """
        return np.all(self.shades!=0)

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
    
    def count_visible_cells_in_direction(self, row, col, direction, thresh=1):
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
    
    def count_visible_cells_from(self, row, col, thresh=1):
        assert thresh in [0,1]
        n_in_dir = sum([self.count_visible_cells_in_direction(
            row, col, direction, thresh=thresh
            ) for direction in ['south','north','east','west']
        ])
        return n_in_dir
    
    def collect_contiguous_cells_from(self, row, col, thresh=1):
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
    
    def get_open_neighbours(self, row, col, thresh=1):
        viable_neighbours = self.get_neighbours(row, col)
        open_neighbours = [coord for coord in viable_neighbours if self.shades[coord] >= thresh]
        return open_neighbours
    
    def get_all_white_cells(self, thresh=1):
        all_white_cells = set([coord for coord in self.valid_coords if self.shades[coord]>=thresh])
        return all_white_cells
    
    def _any_regions_cut_off(self, thresh=0):
        white_cells = self.get_all_white_cells(thresh=thresh)
        if len(white_cells) == 0:
            # There cannot be any cut-off regions if there are no white regions.
            return False
        else:
            one_cell = list(white_cells)[0]
            connected_cells = self.collect_contiguous_cells_from(one_cell[0], one_cell[1], thresh)
            return set(connected_cells) != set(white_cells)
    
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

        
    # def cell_is_valid(self, row, col):
    #     if self.numbers[row,col] > 0:
    #         n_visible = self.cell_horizontal_



# class Cell:
#     self.coordinates
#     self.shade
#     self.number
#     self.neighbours(coordinates)
#
#     def grid.cell.get_neighbours()
#         return coords of neighbouring cells
#
#     def cell.check
#
#     def cell.possible_views()
#
#     def grid.cell.get_visible_cells()
#
#     def
#
#
#
