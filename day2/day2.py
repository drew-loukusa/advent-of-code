
from aocd.models import Puzzle

infile = "day2ex.txt"
infile = "day2in.txt"

# Part 1
if False:
    valid_passswords = 0
    for line in open(infile):
        # Parse line 
        t = line.replace('-', ' ') \
            .replace(':', '') \
            .split(' ')
        
        mn,mx = int(t[0]), int(t[1])
        c,psw = t[2], t[3]

        count = psw.count(c)
        if count >= mn and count <= mx:
            valid_passswords += 1

    print(valid_passswords)

# Part 2
if False:
    valid_passswords = 0
    for line in open(infile):        
        t = line.replace('-', ' ') \
            .replace(':', '') \
            .split(' ')
        
        s,e = int(t[0])-1, int(t[1])-1
        c,psw = t[2], t[3]

        # XOR 
        if  (psw[s] == c and psw[e] != c) != (psw[s] != c and psw[e] == c):
           valid_passswords += 1

        # a a, (True and False) False != (False and True) False } False 
        # a b, (True and True) True != (False and False) False } True
        # b a, (False and False) False != (True and True) True } True

    print(valid_passswords)

import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from aoc import *
from aocd.models import Puzzle

Year=2020
Day=2
puzzle = Puzzle(year=Year, day=Day)
save_input_to_file(puzzle, Day)



