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
        # Sahdes are 0 if blank, 1 for white and -1 for black
        self.visible_in_row = np.zeros(grid_size)
        self.visible_in_column = np.zeros(grid_size)
    
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
    
    def count_cells_in_direction(self, row, col, direction):
        assert direction in ['north','east','south','west']
        
    
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
