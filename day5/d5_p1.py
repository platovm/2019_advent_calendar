# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 20:11:53 2019

@author: Mike
"""

## https://adventofcode.com/2019/day/5

import re

with open('input.txt', 'r') as f:
    input_ = list(map(int,f.read().split(',')))

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
        self.my_number = int(input("Please enter a number (1 for TEST, which is default):").strip() or '1')
        self.mode_regex = re.compile("^1[0-1]?0[1,2]$")
        self.pointer = 0
    
    def basic_add(self, z, seq):
        # print ("Successfully reached the adder")
        temp = seq[seq[z+1]] + seq[seq[z+2]]
        seq[seq[z+3]] = temp
        self.pointer+=3
        
    def basic_mult(self, z, seq):
        # print ("Successfully reached the multiplier")
        temp = seq[seq[z+1]] * seq[seq[z+2]]
        seq[seq[z+3]] = temp
        self.pointer+=3
    
    def from_input(self, z, seq):
        # print ("Successfully reached the inputter")
        seq[seq[z+1]] = self.my_number
        self.pointer+=1
        
    def to_output(self, z, seq):
        #print ("absolutely nothing should be here...")
        print("**IMPORTANT** {}".format(seq[seq[z+1]]))
        self.pointer+=1
        
    def complex_add(self, z, seq, args):
        # print("Successfully reached the level 2 adder")
        #print('We are on complex add, with pointer:{}, args:{}'.format(z, args))
        temp = 0
        if args[1] == 0: #argument 2 -> immediate, argument 3 -> positional 
            temp = seq[z+1] + seq[seq[z+2]]
        else:
            if args[0] == 0:
                temp = seq[seq[z+1]] + seq[z+2]
            else:
                temp = seq[z+1] + seq[z+2]
        print("Temp right now is {}, which will go into position {}".format(temp, seq[z+3]))
        seq[seq[z+3]] = temp
        self.pointer+=3
        
    def complex_mult(self, z, seq, args):
        # print("Successfully reached the level 2 multiplier")
        temp = 0
        if args[1] == 0: #argument 2 -> immediate, argument 3 -> positional 
            temp = seq[z+1] * seq[seq[z+2]]
        else:
            if args[0] == 0:
                temp = seq[seq[z+1]] * seq[z+2]
            else:
                temp = seq[z+1] * seq[z+2]
        print("Temp right now is {}, which will go into position {}".format(temp, seq[z+3]))
        seq[seq[z+3]] = temp
        self.pointer+=3
        
    def single_intcode(self, digit, current, seq):
        print ("Doing single int mode with intcode={}, pointer={}. Intcode changed: {}".format(digit, current, seq!=self.intcode))
        cases = {
                1: self.basic_add,
                2: self.basic_mult,
                3: self.from_input,
                4: self.to_output
                }
        func = cases.get(digit, "Improper intcode identifier")
        try:
            func(current, seq)
        except Exception as e:
            raise(e)
        
    def multi_intcode(self, digit, current, seq, args):
        print ("Doing multi int mode with intcode={}, pointer={}. Args: {}.".format(digit, current, args))
        cases = {
                1: self.complex_add,
                2: self.complex_mult
                }
        func = cases.get(digit, "Improper intcode identifier")
        try:
            func(current, seq, args)
        except Exception as e:
            raise(e)
        
    def compute(self):
        intcode = self.intcode.copy()
        while self.pointer < len(intcode):
            
            # print("Current value at position 0 is {}".format(intcode[0]))
            #print("Welcome to pointer {}, current weather is {}".format(self.pointer, intcode[self.pointer]))

            if len(str(intcode[self.pointer])) == 1 and intcode[self.pointer] in list(range(1,5)):
                
                #print("{} meets single digit criteria".format(intcode[self.pointer]))
                print("Current pointer is {}, running single intcode".format(self.pointer))
                self.single_intcode(intcode[self.pointer], self.pointer, intcode)

            elif len(str(intcode[self.pointer])) > 1 and bool(self.mode_regex.match(str(intcode[self.pointer]))):
                
                #print("{} meets multi digit criteria".format(intcode[self.pointer]))
                #print ("{} is being ruled-checked".format(intcode[self.pointer]))
                code = int(str(intcode[self.pointer])[-2:])
                modes = []
                
                if len(str(intcode[self.pointer])) == 4:
                    modes = list(map(int,','.join(str(intcode[self.pointer])[1::-1]).split(',')))
                
                elif len(str(intcode[self.pointer])) == 3:
                    modes = list((int(str(intcode[self.pointer])[:1]), 0))                 
                
                print("Current pointer is {}, running multi intcode".format(self.pointer))
                self.multi_intcode(code, self.pointer, intcode, modes)
            
            elif intcode[self.pointer] == (99999 or 99): # the 99 is just for backwards compatibility for day 2 challenges
                return intcode
                break
            
            else:
                print("{} is being skipped".format(intcode[self.pointer]))
                pass
            
            self.pointer+=1
            #print("Now we are on pointer {}".format(self.pointer))
        
        return intcode
    
if __name__ == '__main__':
    what = input("Test or Main? ").strip() or 'Main'
    if what == 'Test':
        old_computer = Computer(botched_input)
        print ("The input param of this computer is {}".format(old_computer.my_number))
        old_numbers = old_computer.compute()
        print (old_numbers[0])    
    elif what == 'Main':
        new_computer = Computer(input_)
        print ("The input param of this computer is {}".format(new_computer.my_number))
        new_numbers = new_computer.compute()
    
    

