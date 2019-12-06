# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 13:04:50 2019

@author: Mike
"""

import numpy as np
import pandas as pd
import openpyxl
import matplotlib.pyplot as plt
import matplotlib.cm as cm

with open('wires.txt', 'r') as f:
    temp = f.read().split('\n')
    wire1 = temp[0].split(',')
    wire2 = temp[1].split(',')

class WireGrid():
    def __init__(self, path1, path2):
#        self.wire1 = path1
#        self.wire2 = path2
        self.measurement1 = self.measure(path1)
        self.measurement2 = self.measure(path2)
        self.x_min = min(self.measurement1[0][0], self.measurement2[0][0])
        self.x_max = max(self.measurement1[0][1], self.measurement2[0][1])
        self.y_min = min(self.measurement1[1][0], self.measurement2[1][0])
        self.y_max = max(self.measurement1[1][1], self.measurement2[1][1])
        self.x_offset = -1 * self.x_min if self.x_min < 0 else 0 
        self.y_offset = -1 * self.y_min if self.y_min < 0 else 0
        self.origin = (self.x_offset, self.y_offset) 
        self.test_grid = np.zeros((self.x_max + self.x_offset + 1, self.y_max + self.y_offset + 1))
        #print ("Initialized matrix shape: {}".format(self.test_grid.shape))
        
    def __repr__(self):
        return "Wire grid with size {}, wires starting at {}".format(self.test_grid.shape, self.origin)
 
    def measure(self, path):
        """ 
        Does a dry run of the wire's path, for use in defining the matrix size in order to handle the issue of being unable to do negative indexing
        """
        position = (0,0)
        loci = []
        for direction, pace in ( (x[0], int(x[1:])) for x in path ):
            if direction == 'U':
                old_pos = position
                new_pos = (old_pos[0], old_pos[1] + pace) 
                position = new_pos
                loci.append(position)
            elif direction == 'D':
                old_pos = position
                new_pos = (old_pos[0], old_pos[1] - pace) 
                position = new_pos
                loci.append(position)
            elif direction == 'L':
                old_pos = position
                new_pos = (old_pos[0] - pace, old_pos[1]) 
                position = new_pos
                loci.append(position)
            else:
                old_pos = position
                new_pos = (old_pos[0] + pace, old_pos[1]) 
                position = new_pos
                loci.append(position)
        xcoors, ycoors = zip(*loci)
        return [(min(xcoors), max(xcoors)), (min(ycoors), max(ycoors))]


    def trace(self, path:list, marker, saveformat=None, save=False, colormap=None):
        #grid = self.test_grid
        position = self.origin
        track = []
        for direction, pace in ( (x[0], int(x[1:])) for x in path ):

            if direction == 'U':
                old_pos = position
                new_pos = (old_pos[0], old_pos[1] + pace) 
                self.test_grid[old_pos[0], old_pos[1]:new_pos[1]] += int(marker)
                track.append(
                        list(zip([old_pos[0]]*pace, list(range(old_pos[1], old_pos[1] + pace))))
                        )
                position = new_pos
            elif direction == 'D':
                old_pos = position
                new_pos = (old_pos[0], old_pos[1] - pace) 
                self.test_grid[old_pos[0], old_pos[1]:new_pos[1]:-1] += int(marker)
                track.append(
                        list(zip([old_pos[0]]*pace, list(range(old_pos[1], old_pos[1] - pace, -1))))
                        )
                position = new_pos
            elif direction == 'L':
                old_pos = position
                new_pos = (old_pos[0] - pace, old_pos[1]) 
                self.test_grid[old_pos[0]:new_pos[0]:-1, old_pos[1]] += int(marker)
                track.append(
                        list(zip(list(range(old_pos[0], old_pos[0] - pace, -1)), [old_pos[1]]*pace))
                        )
                position = new_pos
            else:
                old_pos = position
                new_pos = (old_pos[0] + pace, old_pos[1]) 
                self.test_grid[old_pos[0]:new_pos[0], old_pos[1]] += int(marker)
                track.append(
                        list(zip(list(range(old_pos[0], old_pos[0] + pace)), [old_pos[1]]*pace))
                        )
                position = new_pos
        #return test_grid
        if save:
            if saveformat == 'png':
                save_matrix_png(self.test_grid, colormap)
            elif saveformat == 'excel':
                save_matrix_excel(self.test_grid)
            elif saveformat == 'csv':
                save_matrix_csv(self.test_grid)
            return "If you're here, you fucked up the arguments for saveformat: either png or excel"
        return track

    def point_distance(self, A:tuple, B:tuple):
        return abs(A[0] - B[0]) + abs(A[1] - B[1])
    
    def save_matrix_png(self, mat:np.matrix, color=cm.gray):
        fig = plt.figure(figsize=(10,10))
    
        ax = fig.add_subplot()
        # 'nearest' interpolation - faithful but blocky
        ax.imshow(mat, interpolation='nearest', cmap=color)
        
        #plt.show()
        plt.savefig('grid_test.png', dpi=100, bbox_inches='tight')
    
    def save_matrix_excel(self, mat:np.matrix, fname='./grid_test.xlsx'):
        pd.DataFrame(mat).to_excel(fname, index=False)
    
    def save_matrix_csv(self, mat:np.matrix, fname='./grid_test.csv'):
        np.savetxt(fname, mat, delimiter=',')
        
if __name__ == '__main__':
    new_grid = WireGrid(wire1, wire2)
    print ("Using wire grid centered on {}, with shape {}".format(new_grid.origin, new_grid.test_grid.shape))
    #initialize_grid_size(wire1, wire2)
    #print (test_grid.shape)
    wire1_track = new_grid.trace(wire1, 5)
    wire2_track = new_grid.trace(wire2, 4)
    neat_coords = list(zip(*np.where(new_grid.test_grid>=9)))
    neat_markers = list(new_grid.test_grid[np.where(new_grid.test_grid>=9)])
    new_grid.collisions = dict(list(zip(neat_coords, neat_markers)))
    nearest_colision = min(filter(lambda y: y!=0, [new_grid.point_distance(x, new_grid.origin) for x in new_grid.collisions.keys() if new_grid.collisions[x] == 9])) # filtering for 9s because the
    # markers used for the two wires were 4 and 5
    print (nearest_colision)