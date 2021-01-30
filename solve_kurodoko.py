import numpy as np

class Kurodoko(object):
    
    def __init__(self, grid_size):
        
        assert len(grid_size)==2
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
    