# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 13:58:08 2019

@author: Mike
"""

## https://adventofcode.com/2019/day/2#part1

with open('input.txt', 'r') as f:
    input_ = list(map(int,f.read().split(',')))
 
botched_input = input_.copy()
botched_input[1] = 12
botched_input[2] = 2

## This part below was just for exploratory visualization of how 4-tuples look
#def chunks(lst:list, n):
#    """Yield successive n-sized chunks from list."""
#    for i in range(0, len(lst), n):
#        yield lst[i:i + n]
        
#for i in range(len(input_)):
#    if i%4 == 0:
#        print(input_[i])

def computer(lst:list):
    temp_list = lst.copy()      
    for i in range(len(temp_list)):
        if i%4 == 0 and temp_list[i] == 99:
            break
        elif i%4 == 0 and temp_list[i] == 1:
            temp = temp_list[temp_list[i+1]] + temp_list[temp_list[i+2]]
            temp_list[temp_list[i+3]] = temp
        elif i%4 == 0 and temp_list[i] == 2:
            temp = temp_list[temp_list[i+1]] * temp_list[temp_list[i+2]]
            temp_list[temp_list[i+3]] = temp
    return temp_list
    
if __name__ == '__main__':
    print (computer(botched_input)[0])