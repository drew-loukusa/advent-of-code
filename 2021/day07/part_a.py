# https://adventofcode.com/2021/day/7

import sys
import pprint
from collections import defaultdict as dd
from aocd.models import Puzzle
from my_aoc_utils.utils import save_puzzle, AOC_Test

def process(infile):
    """Process the input file into a data structure for solve()"""
    return [int(n) for n in open(infile).readline().split(',')]

def solve(data):

    # First make a count of how many crabs are in each position
    position_counts = dd(int)
    for num in data:
        position_counts[num] += 1

    cur_align_pos = None 
    r_count, r_cost, l_count, l_cost, total_fuel_cost, = 0,0,0,0,0
    l_pos, r_pos = [], []

    # Sort by position, and walk through the positions
    for cur_pos in sorted(position_counts.keys()):
        count = position_counts[cur_pos]
        
        if cur_align_pos is None:
            cur_align_pos = cur_pos
            continue 
        
        # First add the to the right window and update the counts and weights 
        # Because we are walking through the positions in sorted order,
        # new positions will always go on the right 
        if cur_pos > cur_align_pos:
            r_pos.append(cur_pos)
            r_count += count 

            # Calculate what the fuel cost is for the crabs to the current alignment position
            cost = (cur_pos - cur_align_pos) * count

            # Add that cost to the right cost, and total cost
            r_cost += cost
            total_fuel_cost += cost

        # Now check if we need to move the alignment right
        # Check if the cost increase from moving the alignment right
        # is less then the cost decrese 

        # Of course, if you move the alignment right, the old alignment
        # becomes a cost of the left side. So, there has to be enough
        # items on the right so that by moving the alignment right, 
        # we save more than moving the alignment incurs in cost 

        # and maybe we can move the alignment multiple times if needed?
        # Maybe that part loops until condition fails

        # The condition is: If the total cost DECREASES by moving the alignment right...

        move_alignment = True
        while move_alignment:
            if len(r_pos) == 0: 
                break 
            new_align_pos = r_pos[0]
            old_align_count = position_counts[cur_align_pos]
            new_align_count = position_counts[new_align_pos]

            align_diff = new_align_pos - cur_align_pos
            new_l_cost = l_cost + ((align_diff * l_count) + (align_diff * old_align_count))
            new_r_cost = r_cost - (align_diff * r_count)
            new_t_cost = new_l_cost + new_r_cost

            if new_t_cost < total_fuel_cost:
                l_pos.append(cur_align_pos)
                cur_align_pos = r_pos.pop(0)
                l_cost = new_l_cost
                r_cost = new_r_cost 
                total_fuel_cost = new_t_cost
                l_count += old_align_count
                r_count -= new_align_count
            else:
                move_alignment = False

    return total_fuel_cost

def main(infile):
    return solve(process(infile))
    
if __name__ == "__main__":
    year, day = 2021, 7
    save_puzzle(year, day, __file__)
    aoc = AOC_Test(main, __file__)

    # TESTS, test against example input, other test input here
    aoc.test("day7ex.txt", ans=37)

    # Run question 
    aoc.test("day7.txt", ans=356958, save_answer=True)

    # Submit if user passed in 'submit' on command line
    if len(sys.argv) > 1 and sys.argv[1] == "submit":
        puzzle = Puzzle(year=year, day=day)
        puzzle.answer_a = aoc.answer
