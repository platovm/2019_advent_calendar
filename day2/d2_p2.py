# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 15:12:56 2019

@author: Mike
"""

## https://adventofcode.com/2019/day/2#part1

with open('input.txt', 'r') as f:
    input_ = list(map(int,f.read().split(',')))

target = 19690720

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

def bruteforce(lst:list):
    #temp_list = lst.copy()
    done = False
    for i in range(99+1):
        temp_list = lst.copy()
        temp_list[1] = i
        snapshot = temp_list.copy()
        print (snapshot[:1]+snapshot[2:] == lst[:1]+lst[2:])
        for j in range(99+1):
            temp_list[2] = j
            temp = computer(temp_list)[0]
            if temp == target:
                done = True
                break
            temp_list = snapshot
        if done:
            break
    return i,j

if __name__ == '__main__':
    noun, verb = bruteforce(input_)
    print (100 * noun + verb)