# https://adventofcode.com/2021/day/14

import sys
from collections import defaultdict as dd
from aocd.models import Puzzle
from my_aoc_utils.utils import save_puzzle, AOC_Test

def process(infile):
    """Process the input file into a data structure for solve()"""
    
    template = None 
    insertion_rules = dict()
    for line in open(infile):
        line = line.rstrip()
        if len(line) <= 0: 
            continue
        if template is None:
            template = line
        else:
            rule, _, element = line.split(' ')
            insertion_rules[rule] = element
    return template, insertion_rules

def solve(template, insertion_rules, steps_to_run):
    counts = None 
    cur_step_str = list(template)
    lce, mce = cur_step_str[0:2]
    # Problem soving go HERE
    for _ in range(steps_to_run):
        element_counts = dd(int)
        a, b = None, cur_step_str[0]
        i = 1
        tlen = len(cur_step_str)
        next_step_str = b
        element_counts[b] += 1
        while i < len(cur_step_str):
            # Move window 
            a = b
            b = cur_step_str[i]

            # Find which element should be inserted given current window
            rule_str = ''.join([a,b])
            element_to_insert = insertion_rules[rule_str]
            
            # Increment element counts
            element_counts[element_to_insert] += 1
            element_counts[b] += 1
            
            # Add window and new element to string for the next step 
            next_step_str += (element_to_insert + b)
            # increment i
            i += 1
        cur_step_str = next_step_str
        counts = element_counts

    mcc, lcc = None, None 
    for k,v in counts.items():
        if lcc is None: lcc, lce = v, k
        if v < lcc: lcc, lce = v, k
        if mcc is None: mcc, mce, = v, k
        if v > mcc: mcc, mce, = v, k
            
    return counts[mce] - counts[lce]

def main(infile):
    return solve(*process(infile), steps_to_run=10)
    
if __name__ == "__main__":
    year, day = 2021, 14
    save_puzzle(year, day, __file__)
    aoc = AOC_Test(main, __file__)

    # TESTS, test against example input, other test input here
    aoc.test("day14ex.txt", ans=1588)

    # Run question 
    aoc.test("day14.txt", ans=3555, save_answer=True)

    # Submit if user passed in 'submit' on command line
    if len(sys.argv) > 1 and sys.argv[1] == "submit":
        puzzle = Puzzle(year=year, day=day)
        puzzle.answer_a = aoc.answer
