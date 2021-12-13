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
    
    for instr in instructions[0:1]:

        axis,fold_line = instr.split('=')
        fold_line = int(fold_line)

        # Get the row or column indices of the rows or cols to be flipped
        rows_or_cols = set([ n for n in dots[axis] if n > fold_line ])

        # get indicies and rows or cols into lists
        kstack = []
        vstack = []
        end = MAX_X if axis == 'x' else MAX_Y
        for i in range(fold_line, end + 1):
            kstack.append(i)
            if i in rows_or_cols:
                vstack.append(dots[axis][i])
            else:
                vstack.append({})

        # if MAX_X  < 80 and MAX_Y < 80: 
        #     dump_dots(dots, axis, fold_line, MAX_X, MAX_Y)
        # print(end='')

        mi, mj = fold_line, fold_line
        while mj < end:
            mj += 1
            mi -= 1
            for dot in dots[axis][mj]:
                if axis == 'y': dot.y = mi
                if axis == 'x': dot.x = mi
                dots[axis][mi].add(dot)

        for k in range(fold_line, end + 1):
            if k in dots[axis]:
                del dots[axis][k]
        
        if axis == 'y': MAX_Y = fold_line - 1
        if axis == 'x': MAX_X = fold_line - 1

        # if MAX_X  < 80 and MAX_Y < 80: 
        #     dump_dots(dots, axis, fold_line, MAX_X, MAX_Y)
        # print(end='')


    all_dots = set()
    dots_sum = 0
    for row in dots['y'].values():
        for dot in row:
            all_dots.add(dot)
    if MAX_X  < 80 and MAX_Y < 80: 
        dump_dots(dots, axis, fold_line, MAX_X, MAX_Y)
        print(end='')
    return len(all_dots)

def main(infile):
    return solve(*process(infile))
    
if __name__ == "__main__":
    year, day = 2021, 13
    save_puzzle(year, day, __file__)
    aoc = AOC_Test(main, __file__)

    # TESTS, test against example input, other test input here
    aoc.test("day13ex.txt", ans=17)
    aoc.test("day13ex1.txt", ans=40)
    aoc.test("day13ex2.txt", ans=20)

    # Run question 
    aoc.test("day13.txt", ans=-1, save_answer=True)

    # Submit if user passed in 'submit' on command line
    if len(sys.argv) > 1 and sys.argv[1] == "submit":
        puzzle = Puzzle(year=year, day=day)
        puzzle.answer_a = aoc.answer