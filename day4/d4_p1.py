# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 22:06:48 2019

@author: Mike
"""

## https://adventofcode.com/2019/day/4

#However, they do remember a few key facts about the password:
#
#It is a six-digit number.
#The value is within the range given in your puzzle input.
#Two adjacent digits are the same (like 22 in 122345).
#Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679).
#Other than the range rule, the following are true:
#
#111111 meets these criteria (double 11, never decreases).
#223450 does not meet these criteria (decreasing pair of digits 50).
#123789 does not meet these criteria (no double).
#How many different passwords within the range given in your puzzle input meet these criteria?

from itertools import groupby

input_ = '197487-673251'
input_range = list(map(int,input_.split('-')))
possible_values = list(range(input_range[0],input_range[1]+1))

def check_pattern(lst):
    
    passes = []
    
    def check_increasing(list_of_digits):
        i = 1
        while i < len(list_of_digits):
            check = int(list_of_digits[i-1]) <= int(list_of_digits[i])
            if not check:
                return False
            i+=1
        return True
    
    def has_pair(list_of_digits):
        if len(list(groupby(list_of_digits))) == len(list_of_digits):
            return False
        return True    
    
    for number in lst:
        breakdown = [x for x in str(number)]
        passes.append(has_pair(breakdown) & check_increasing(breakdown))
    
    return sum(passes)

if __name__ == '__main__':
    solution = check_pattern(possible_values)
    print (solution)