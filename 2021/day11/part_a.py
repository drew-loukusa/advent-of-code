# https://adventofcode.com/2021/day/11

import os
import sys
from aocd.models import Puzzle
from my_aoc_utils.utils import save_puzzle, AOC_Test

def process(infile):
    """Process the input file into a data structure for solve()"""
    return [[int(n) for n in line.rstrip()] for line in open(infile)]

def dump_matrix(matrix, clear=True):
    if clear:
        os.system("cls")
    for y, row in enumerate(matrix):
        for x in range(len(row)):
            if matrix[y][x] > 9:
                print('▮', end='')
            else:
                print(matrix[y][x], end='')
        print()

def increment_all(matrix, ignore_zeros=False):
    for y, row in enumerate(matrix):
        for x in range(len(row)):
            if matrix[y][x] == 0 and ignore_zeros:
                continue 
            matrix[y][x] += 1
    
def bfs_flash(point, M, flashed):
    flash_count = 0
    MAX_Y = len(M) - 1
    MAX_X = len(M[0]) - 1
    q = [point]
    while len(q) > 0:
        y,x = q.pop(0)
        if (y,x) in flashed:
            continue
        
        M[y][x] = 0
        flashed.add((y,x))
        flash_count += 1

        row = M[y]
        num = row[x]
      
        # INCREMENT Neighbors
        # At the same time, check if "Flashing" caused any neighbors to be >= 9

        def inc_and_queue(point):
            y, x = point
            if point not in flashed:
                M[y][x] += 1
            if M[y][x] > 9:
                q.append(point)

        # Check up
        if y > 0: 
            inc_and_queue((y - 1,x))

        # Right and up
        if x < MAX_X and y > 0:
            inc_and_queue((y - 1,x + 1))

        # Check right        
        if x < MAX_X:
            inc_and_queue((y,x + 1))

        # Right and down 
        if x < MAX_X and y < MAX_Y:
            inc_and_queue((y + 1,x + 1))

        # Check down
        if y < MAX_Y:
            inc_and_queue((y + 1,x))

        # Left and down
        if x > 0 and y < MAX_Y: 
            inc_and_queue((y + 1,x - 1))

        # Check left
        if x > 0:
            inc_and_queue((y,x - 1))

        # Left and up 
        if x > 0 and y > 0:
            inc_and_queue((y - 1,x - 1))
    
    return flash_count
        

def solve(matrix):   
    flash_count = 0
    for _ in range(100):
        # dump_matrix(matrix)
        increment_all(matrix)
        # dump_matrix(matrix)
        flashed = set()
        for y, row in enumerate(matrix):
            for x in range(len(row)):
                if matrix[y][x] > 9:
                    flash_count += bfs_flash((y,x), matrix, flashed)
       
        #dump_matrix(matrix)
        print(end='')
    return flash_count
        
def main(infile):
    return solve(process(infile))
    
if __name__ == "__main__":
    year, day = 2021, 11
    save_puzzle(year, day, __file__)
    aoc = AOC_Test(main, __file__)

    # TESTS, test against example input, other test input here
    # aoc.test("smollex.txt", ans=None)
    aoc.test("day11ex.txt", ans=1656)

    # Run question 
    aoc.test("day11.txt", ans=1665, save_answer=True)

    # Submit if user passed in 'submit' on command line
    if len(sys.argv) > 1 and sys.argv[1] == "submit":
        puzzle = Puzzle(year=year, day=day)
        puzzle.answer_a = aoc.answer
