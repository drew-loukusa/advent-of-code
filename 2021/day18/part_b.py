# https://adventofcode.com/2021/day/18

import sys
from typing import List
from aocd.models import Puzzle
from my_aoc_utils.utils import save_puzzle, AOC_Test
from part_a import BTreeNode, TreeParser, process, set_depth, reduce, calculate_magnitude, flatten_tree

def process(infile):
    return [line.rstrip() for line in open(infile)]

def add_trees(left, right):
    """
    Add left and right together and reduce.
    Return the magnitude of the result tree.
    """
    root = BTreeNode(value=None, left=left, right=right)
    set_depth(root)
    reduce(root)
    return calculate_magnitude(root) 

def solve(trees: List[str]):    
    max_mag = 0
    
    # Input isn't that large, so we can afford to use nested for loops
    for ltree in trees:
        for rtree in trees:
            if ltree == rtree: 
                continue 
            left = TreeParser(ltree).parse_tree()
            right = TreeParser(rtree).parse_tree()
            mag = add_trees(left, right)
            max_mag = max(mag, max_mag)
    return max_mag

def main(infile):
    return solve(process(infile))
    
if __name__ == "__main__":
    year, day = 2021, 18
    save_puzzle(year, day, __file__)
    aoc = AOC_Test(main, __file__)

    # TESTS, test against example input, other test input here
    aoc.test("ex0.txt", ans=3993)

    # Run question 
    aoc.test("puzzle_input.txt", ans=None, save_answer=True)

    # Submit if user passed in 'submit' on command line
    if len(sys.argv) > 1 and sys.argv[1] == "submit":
        puzzle = Puzzle(year=year, day=day)
        puzzle.answer_b = aoc.answer
