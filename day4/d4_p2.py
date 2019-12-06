# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 14:11:34 2019

@author: Mike
"""

## https://adventofcode.com/2019/day/4#part2

#An Elf just remembered one more important detail: the two adjacent matching digits are not part of a larger group of matching digits.
#
#Given this additional criterion, but still ignoring the range rule, the following are now true:
#
#112233 meets these criteria because the digits never decrease and all repeated digits are exactly two digits long.
#123444 no longer meets the criteria (the repeated 44 is part of a larger group of 444).
#111122 meets the criteria (even though 1 is repeated more than twice, it still contains a double 22).

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
    
    ## changed relative to d4_p1
    def has_pair(list_of_digits):
        iter_group_lengths = len(list(groupby(list_of_digits))), [len(list(g)) for k,g in groupby(list_of_digits)]
        #print (iter_group_lengths)
        if iter_group_lengths[0] == len(list_of_digits) or 2 not in iter_group_lengths[1]:
            return False
        return True    
    
    for number in lst:
        breakdown = [x for x in str(number)]
        passes.append(has_pair(breakdown) & check_increasing(breakdown))
    
    return sum(passes)

if __name__ == '__main__':
    solution = check_pattern(possible_values)
    print (solution)



