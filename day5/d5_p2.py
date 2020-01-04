# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 13:17:54 2019

@author: Mike
"""

## https://adventofcode.com/2019/day/5#part2

import re
import logging
import pysnooper

# FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
# logging.basicConfig(filename='d5p2.log', format=FORMAT, level=logging.DEBUG)

with open('input.txt', 'r') as f:
    input_ = list(map(int,f.read().split(',')))

with open('testing_input.txt', 'r') as f:
    test_input = list(map(int,f.read().split(',')))

with open('../day2/input.txt','r',) as f:
    old_input = list(map(int, f.read().split(',')))
    
botched_input = old_input.copy()
botched_input[1] = 12
botched_input[2] = 2

# with old data, the first element should be 6627023

# Possible opt codes: ending in 1, 2, 3, 4, or 99, regardless of form/number of digits

#def computer(list_):
class Computer:
    def __init__(self, lst):
        self.intcode = lst
        self.my_number = int(input("Please enter a number (1 for TEST, 5 for AC (default)): ").strip() or '5') #updated to default to 5, not 1
        self.mode_regex = re.compile("^1[0-1]?0[1,2,4-8]$") #updated to include 5-8
        self.pointer = 0
    
    def basic_add(self, z, seq):
        temp = seq[seq[z+1]] + seq[seq[z+2]]
        seq[seq[z+3]] = temp
        self.pointer+=3
        
    def basic_mult(self, z, seq):
        temp = seq[seq[z+1]] * seq[seq[z+2]]
        seq[seq[z+3]] = temp
        self.pointer+=3
    
    def from_input(self, z, seq):
        seq[seq[z+1]] = self.my_number
        self.pointer+=1
        
    def to_output(self, z, seq):
        print("**IMPORTANT** {}".format(seq[seq[z+1]]))
        self.pointer+=1
    
    def jump_if_true(self, z, seq):
        if seq[seq[z+1]] != 0:
            self.pointer = seq[seq[z+2]]
        else:
            self.pointer+=3
    
    def jump_if_false(self, z, seq):
        if seq[seq[z+1]] == 0:
            self.pointer = seq[seq[z+2]]
        else:
            self.pointer+=3     

    def less_than(self, z, seq):
        if seq[seq[z+1]] < seq[seq[z+2]]:
            seq[seq[z+3]] = 1
        else:
            seq[seq[z+3]] = 0
        self.pointer+=3
        
    def equals_to(self, z, seq):
        if seq[seq[z+1]] == seq[seq[z+2]]:
            seq[seq[z+3]] = 1
        else:
            seq[seq[z+3]] = 0
        self.pointer+=3
        
    def complex_add(self, z, seq, args):
        temp = 0
        if args[1] == 0: #argument 2 -> immediate, argument 3 -> positional 
            temp = seq[z+1] + seq[seq[z+2]]
        else:
            if args[0] == 0:
                temp = seq[seq[z+1]] + seq[z+2]
            else:
                temp = seq[z+1] + seq[z+2]
        seq[seq[z+3]] = temp
        self.pointer+=3
        
    def complex_mult(self, z, seq, args):
        temp = 0
        if args[1] == 0: #argument 2 -> immediate, argument 3 -> positional 
            temp = seq[z+1] * seq[seq[z+2]]
        else:
            if args[0] == 0:
                temp = seq[seq[z+1]] * seq[z+2]
            else:
                temp = seq[z+1] * seq[z+2]
        seq[seq[z+3]] = temp
        self.pointer+=3
    
    def complex_output(self, z, seq, args):
        print("**IMPORTANT** {}".format(seq[z+1]))
        self.pointer+=1
    
    def complex_jump_true(self, z, seq, args):
        good = False
        if args[1] == 0:
            if seq[z+1] != 0:
                self.pointer = seq[seq[z+2]]
                good = True
        elif args[1] == 1: 
            if args[0] == 0:
                if seq[seq[z+1]] != 0:
                    self.pointer = seq[z+2]
                    good = True
            elif args[0] == 1:
                if seq[z+1] != 0:
                    self.pointer = seq[z+2]
                    good = True

        if not good:
            self.pointer+=3
    
    def complex_jump_false(self, z, seq, args):        
#        print ("Starting with pointer @ {}".format(z))
        good = False
        if args[1] == 0:
            if seq[z+1] == 0:
                self.pointer = seq[seq[z+2]]
                good = True
        elif args[1] == 1: 
            if args[0] == 0:
                if seq[seq[z+1]] == 0:
                    self.pointer = seq[z+2]
                    good = True
            elif args[0] == 1:
                if seq[z+1] == 0:
                    self.pointer = seq[z+2]
                    good = True
        
        if not good:
            self.pointer+=3
    
    def complex_equality_less(self, z, seq, args):
        temp = 0
        if args[1] == 0: 
            temp = seq[z+1] < seq[seq[z+2]]
        else:
            if args[0] == 0:
                temp = seq[seq[z+1]] < seq[z+2]
            else:
                temp = seq[z+1] < seq[z+2]

        if temp:
            seq[seq[z+3]] = 1
        else:
            seq[seq[z+3]] = 0
        self.pointer+=3
    
    def complex_equality_equal(self, z, seq, args):                
        temp = 0
        if args[1] == 0:  
            temp = seq[z+1] == seq[seq[z+2]]
        else:
            if args[0] == 0:
                temp = seq[seq[z+1]] == seq[z+2]
            else:
                temp = seq[z+1] == seq[z+2]
                
        if temp:
            seq[seq[z+3]] = 1
        else:
            seq[seq[z+3]] = 0
        self.pointer+=3
    
    def single_intcode(self, digit, current, seq):
#        print ("Doing single int mode with pointer={}, instruction={}. Intcode changed: {}".format(current, seq[current], seq!=self.intcode))
        cases = {
                1: self.basic_add,
                2: self.basic_mult,
                3: self.from_input,
                4: self.to_output,
                5: self.jump_if_true,
                6: self.jump_if_false,
                7: self.less_than,
                8: self.equals_to
                }
        func = cases.get(digit, "Improper intcode identifier")
        try:
            func(current, seq)
        except Exception as e:
            raise(e)
        
    def multi_intcode(self, digit, current, seq, args):
#        print ("Doing multi int mode with intcode={}, pointer={}, instruction={}. Args: {}.".format(digit, current, seq[current], args))
        cases = {
                1: self.complex_add,
                2: self.complex_mult,
                4: self.complex_output,
                5: self.complex_jump_true,
                6: self.complex_jump_false,
                7: self.complex_equality_less,
                8: self.complex_equality_equal
                }
        func = cases.get(digit, "Improper intcode identifier")
        try:
            func(current, seq, args)
        except Exception as e:
            raise(e)
    
    #@pysnooper.snoop(depth=3)
    def compute(self):
        intcode = self.intcode.copy()
        while self.pointer < len(intcode):
            
            pointer_reset = self.pointer
            initial_code = intcode[pointer_reset]
            
            
            if intcode[self.pointer] in list(range(1,9)): # bit of hardcoding here in specifying the list of valid single-digit intcodes
                
                self.single_intcode(intcode[self.pointer], self.pointer, intcode)

            elif len(str(intcode[self.pointer])) > 1 and bool(self.mode_regex.match(str(intcode[self.pointer]))):
                
                code = int(str(intcode[self.pointer])[-2:])
                modes = []
                
                if len(str(intcode[self.pointer])) == 4:
                    modes = list(map(int,','.join(str(intcode[self.pointer])[1::-1]).split(',')))
                
                elif len(str(intcode[self.pointer])) == 3:
                    modes = list((int(str(intcode[self.pointer])[:1]), 0))                 
                
                self.multi_intcode(code, self.pointer, intcode, modes)
                

            elif intcode[self.pointer] in [99999,99]: # the 99 is just for backwards compatibility for day 2 challenges
                break
            
            else:
                pass                
            
            #basically, if the pointer was at a valid intcode, and the intcode was changed, start this loop over --> pointer should be changed by this point
            if intcode[pointer_reset] != initial_code or int(str(initial_code)[-1:]) in [5,6]: 
                continue
            
            self.pointer+=1             
        
        return intcode
    
if __name__ == '__main__':
    what = input("Old, Test, Main (default), or None? ").strip() or 'Main'
    if what == 'Old':
        old_computer = Computer(botched_input)
        print ("The input param of this computer is {}".format(old_computer.my_number))
        old_numbers = old_computer.compute()
        print (old_numbers[0])
    elif what == 'Test':
        new_computer = Computer(test_input)
        print ("The input param of this computer is {}".format(new_computer.my_number))
        new_numbers = new_computer.compute()
    elif what == 'Main':
        new_computer = Computer(input_)
        print ("The input param of this computer is {}".format(new_computer.my_number))
        new_numbers = new_computer.compute()
    elif what == 'None':
        pass
