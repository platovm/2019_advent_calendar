# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 13:33:08 2019

@author: Mike
"""

import numpy as np
import pandas as pd
import openpyxl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import d3_p1_oop as part1

with open('wires.txt', 'r') as f, \
    open('fake_wire_1.txt', 'r') as a,\
    open('fake_wire_2.txt', 'r') as b:
    temp = f.read().split('\n')
    wire1 = temp[0].split(',')
    wire2 = temp[1].split(',')
    fake_wire1 = a.read().split(',')
    fake_wire2 = b.read().split(',')

def wire_distance(collisions, wire1_t, wire2_t):
    flat_wire1, flat_wire2 = [], []
    for x in wire1_t: flat_wire1.extend(x)
    for x in wire2_t: flat_wire2.extend(x)
    #print (len(flat_wire1), len(flat_wire2))
#    return flat_wire1, flat_wire2
    wire_distances = []
    for collision in (x for x in collisions.keys() if collisions[x] == 9):
        wire_distances.append(flat_wire1.index(collision) + flat_wire2.index(collision))
    return min(filter(lambda x: x!= 0 , wire_distances))

if __name__ == '__main__':
    new_grid = part1.WireGrid(wire1, wire2)
    print ("Using wire grid centered on {}, with shape {}".format(new_grid.origin, new_grid.test_grid.shape))
    #initialize_grid_size(wire1, wire2)
    #print (test_grid.shape)
    wire1_track = new_grid.trace(wire1, 5)
    wire2_track = new_grid.trace(wire2, 4)
    neat_coords = list(zip(*np.where(new_grid.test_grid>=9)))
    neat_markers = list(new_grid.test_grid[np.where(new_grid.test_grid>=9)])
    new_grid.collisions = dict(list(zip(neat_coords, neat_markers)))
    #f1, f2 = wire_distance(new_grid.collisions, wire1_track, wire2_track)
    solution = wire_distance(new_grid.collisions, wire1_track, wire2_track)
    print (solution)