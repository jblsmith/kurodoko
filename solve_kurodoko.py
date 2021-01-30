import numpy as np

class Kurodoko(object):
    
    def __init__(self, grid_size):
        
        assert len(grid_size)==2
        self.cells = np.zeros(grid_size)
