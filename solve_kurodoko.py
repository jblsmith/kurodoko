import numpy as np

class Kurodoko(object):
    
    def __init__(self, grid_size):
        
        assert len(grid_size)==2
        self.numbers = np.zeros(grid_size)
        self.shades = np.zeros(grid_size)
        self.visible_in_row = np.zeros(grid_size)
        self.visible_in_column = np.zeros(grid_size)
    
    