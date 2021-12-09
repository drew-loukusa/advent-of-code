# https://adventofcode.com/2021/day/7

import sys
from collections import defaultdict as dd
from aocd.models import Puzzle
from my_aoc_utils.utils import save_puzzle, AOC_Test

def process(infile):
    """Process the input file into a data structure for solve()"""
    return [int(n) for n in open(infile).readline().split(',')]

def cost_of(distance):
    return int((distance**2 + distance)/2)
    # return distance

def solve(data):

    # First make a count of how many crabs are in each position
    pos_counts = dd(int)
    for num in data:
        pos_counts[num] += 1

    cur_align_pos = None
    r_count, l_count, total_fuel_cost = 0,0,0
    l_pos, r_pos = [], []

    # Sort by position, and walk through the positions
    # for cur_pos in sorted(position_counts.keys()):
    spc = sorted(pos_counts.keys())
    all_pos = range(spc[0], spc[-1]+1)
    for cur_pos in all_pos:
        count = pos_counts[cur_pos]
        
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
            cost = cost_of(cur_pos - cur_align_pos) * count

            # Add that cost to the right cost, and total cost
            if cost > 0:
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
        i = 0
        while move_alignment:
            if len(r_pos) == 0: 
                break
            new_align_pos = r_pos[i]
            old_align_count = pos_counts[cur_align_pos]
            new_align_count = pos_counts[new_align_pos]

            # Calc l cost
            new_l_cost = 0      
            for pos in l_pos:
                if pos_counts[pos] > 0:
                    new_l_cost += cost_of(abs(new_align_pos - pos))*pos_counts[pos]

            # If left gains new elements, calc cost for them
            new_l_cost += cost_of(abs(new_align_pos - cur_align_pos))*old_align_count

            # Calc r cost
            new_r_cost = 0
            for pos in r_pos:
                if pos_counts[pos] > 0:
                    new_r_cost += cost_of(abs(pos - new_align_pos))*pos_counts[pos]

            # If the right loses elements, calc how much cost is removed
            # new_r_cost -= cost_of(abs(new_align_pos - cur_align_pos))*new_align_count

            new_t_cost = new_l_cost + new_r_cost

            if new_t_cost <= total_fuel_cost:
                l_pos.append(cur_align_pos)
                cur_align_pos = r_pos.pop(0)
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
    aoc.test("day7ex.txt", ans=168)

    # Run question
    aoc.test("day7.txt", ans=105461913, save_answer=True)

    # Submit if user passed in 'submit' on command line
    if len(sys.argv) > 1 and sys.argv[1] == "submit":
        puzzle = Puzzle(year=year, day=day)
        puzzle.answer_b = aoc.answer
