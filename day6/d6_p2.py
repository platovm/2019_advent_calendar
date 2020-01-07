# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 10:31:21 2020

@author: Mike
"""

from treelib import Tree
#import pysnooper

with open('orbit_input.txt', 'r') as f:
    input_ = f.read().split('\n')
    
with open('test_input.txt', 'r') as f:
    test_input = f.read().split('\n')

with open('test_input_SAN.txt', 'r') as f:
    test_input_SAN = f.read().split('\n')

def main(lst):
    parents = [x.split(')')[0] for x in lst]
    children = [x.split(')')[1] for x in lst]
    
    #initialize tree and root
    galaxy = Tree()
    galaxy.create_node("COM", "COM")
        
    for c_node in children:
        galaxy.create_node(c_node, c_node, parent='COM')
    
    for pair in list(zip(parents, children)):
        galaxy.move_node(pair[1], pair[0])
    
    indices = {}
    for line in galaxy.paths_to_leaves():
        for ele in line:
            indices[ele] = line.index(ele)
    
    leaves = galaxy.paths_to_leaves()
    main.total = 0
    
    def aggregate(leaves):
        main_leaf = sorted(leaves, key=len, reverse=True)[0]
        main.total += sum([indices[q] for q in main_leaf])
        #print("Len of current leaves: {}, total at this point is {}".format(len(leaves), main.total))
        
        leaves.remove(main_leaf)
        
        for i in range(len(leaves)):
            leaves[i] = list(set(leaves[i]) - set(main_leaf))
         
        flat_leaves = [x for lst in leaves for x in lst]
        if len(flat_leaves) == len(set(flat_leaves)):
            for planet in flat_leaves:
                main.total += indices[planet]
            return False
        
        else:
            return aggregate(leaves)
    
    aggregate(leaves)
    print(main.total)    
    return galaxy

if __name__ == '__main__':
    temp = input("Test, Santest, or Main (default)? ").strip() or "Main"
    if temp == "Test":
        tree = main(test_input)
    elif temp == 'Santest':
        tree = main(test_input_SAN)
    elif temp == "Main":
        tree = main(input_)
    you_branch = list(tree.rsearch('YOU'))
    san_branch = list(tree.rsearch('SAN'))
    shared = set(you_branch).intersection(set(san_branch))
    you_branchpoint = min([you_branch.index(x) for x in shared])
    san_branchpoint = min([san_branch.index(x) for x in shared])
    print (you_branchpoint + san_branchpoint - 2)
        
        