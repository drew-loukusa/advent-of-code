# https://adventofcode.com/2021/day/4

import sys
from aocd.models import Puzzle
from my_aoc_utils.utils import save_puzzle, AOC_Test
from part_a import BingoBoard, make_boards, next_winning_board, sum_unmarked_values

def process(infile):
    """Process the input file into a data structure for solve()"""
    return [line.rstrip() for line in open(infile)]

def solve(data):
    nums = [ int(n) for n in data[0].split(',')]
    boards, vals_to_board = make_boards(data[2:])
    _, _, nums = next_winning_board(nums, boards)

        

def main(infile):
    return solve(process(infile))
    
if __name__ == "__main__":
    year, day = 2021, 4
    save_puzzle(year, day, __file__)
    aoc = AOC_Test(main, __file__)

    # TESTS, test against example input, other test input here
    aoc.test("day4ex.txt", ans=None)

    # Run question 
    aoc.test("day4.txt", ans=None, save_answer=True)

    # Submit if user passed in 'submit' on command line
    if len(sys.argv) > 1 and sys.argv[1] == "submit":
        puzzle = Puzzle(year=year, day=day)
        puzzle.answer_b = aoc.answer
