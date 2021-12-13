# https://adventofcode.com/2021/day/13

import sys
from copy import deepcopy
from collections import defaultdict as dd
from aocd.models import Puzzle
from my_aoc_utils.utils import save_puzzle, AOC_Test

class Dot:
    def __init__(self, x,y):
        self.x = x 
        self.y = y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self) -> str:
        return f"d({self.x}, {self.y})"

    def __eq__(self, __o: object) -> bool:
        return (self.x == __o.x and self.y == __o.y)

    def coords(self):
        return self.x, self.y

def process(infile):
    """Process the input file into a data structure for solve()"""
    MAX_X, MAX_Y = 0,0
    dots = {'y':dd(set), 'x':dd(set)} 
    instructions = [] 
    for line in open(infile):
        line = line.rstrip()
        if len(line) == 0:
            break
        x,y = line.split(',')
        x,y = int(x), int(y)
        dot = Dot(x,y)
        dots['y'][y].add(dot)
        dots['x'][x].add(dot)
        MAX_X = max(x, MAX_X)
        MAX_Y = max(y, MAX_Y)

    for line in open(infile):
        line = line.rstrip()
        tokens = line.split(' ')
        if len(tokens) == 3:
            instructions.append(tokens[2])
    
    return dots, instructions, MAX_X, MAX_Y

def dump_dots(dots, axis, fold_line, MAX_X, MAX_Y):
    print("="*80)
    dots = deepcopy(dots)
    for y in range(MAX_Y + 1):
        if axis == 'y' and fold_line == y:
            print('-'*MAX_X)
            continue
        for x in range(MAX_X + 1):
            if axis == 'x' and fold_line == x:
                print('|', end='')
                continue
            if len(dots['y'][y]) > 0:
                row_set: set = dots['y'][y]
                pdot = Dot(x,y)
                if pdot in row_set:
                    print('#', end='')
                    dots['y'][y].remove(Dot(x,y))
                else:
                    print('.', end='')
            else:
                print('.', end='')
        print()

def solve(dots, instructions, MAX_X, MAX_Y):   
    
    for instr in instructions:

        axis,fold_line = instr.split('=')
        fold_line = int(fold_line)

        end = MAX_X if axis == 'x' else MAX_Y

        # Walk UP and DOWN from the fold line at the same time
        # OR RIGHT and LEFT (depends on what the fold axis is)

        # As we encounter dots below or to the right of the fold
        # We push them into the corresponding mirrored row or col

        k, f = fold_line, fold_line
        while f < end:
            f += 1 
            k -= 1
            # "Move" the dot and update the dot itself 
            for dot in dots[axis][f]:
                if axis == 'y': dot.y = k
                if axis == 'x': dot.x = k
                dots[axis][k].add(dot)

        # Remove lines that have been "folded"
        for k in range(fold_line, end + 1):
            if k in dots[axis]:
                del dots[axis][k]
        
        # Update the bounds (used for dumping)
        if axis == 'y': MAX_Y = fold_line - 1
        if axis == 'x': MAX_X = fold_line - 1       
    
    # Put all the dots into a new set 
    all_dots = set()
    for row in dots['y'].values():
        for dot in row:
            all_dots.add(dot)

    # Why put all dots into a new set?
    # Because I was hashing 'dots' with values which I then changed later.
    # This means the hash values don't match what the were originally
    # SO, when you are adding points to a row or column, you might add a 
    # duplicate value since set.add() won't detect dupes (dupes will have diff 
    # hashes) 

    # THIS IS BECAUSE I USED A HACK. I made a mutable type that I can hash. BAD!
    # But, it does work in this case. You just have to make sure to get rid of
    # dupes at the end before counting

    # By trying to push all the dots that still "exist" into a new set, we force 
    # python to re-evaluate the hash, and now dupes will be rejected. 
    # This will give us the true count of how many dots are visible after folding
  
    return len(all_dots)

def main(infile):
    dots, instructions, MAX_X, MAX_Y = process(infile)
    return solve(dots, [instructions[0]], MAX_X, MAX_Y)
    
if __name__ == "__main__":
    year, day = 2021, 13
    save_puzzle(year, day, __file__)
    aoc = AOC_Test(main, __file__)

    # TESTS, test against example input, other test input here
    aoc.test("day13ex.txt", ans=17)
    aoc.test("day13ex1.txt", ans=40)
    aoc.test("day13ex2.txt", ans=20)

    # Run question 
    aoc.test("day13.txt", ans=610, save_answer=True)

    # Submit if user passed in 'submit' on command line
    if len(sys.argv) > 1 and sys.argv[1] == "submit":
        puzzle = Puzzle(year=year, day=day)
        puzzle.answer_a = aoc.answer 