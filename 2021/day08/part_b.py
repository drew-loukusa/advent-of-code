# https://adventofcode.com/2021/day/8

import sys
from collections import defaultdict as dd
from aocd.models import Puzzle
from my_aoc_utils.utils import save_puzzle, AOC_Test

def process(infile):
    """Process the input file into a data structure for solve()"""
    data = []
    for line in open(infile):
        signal_patterns = []
        tokens = line.rstrip().split(' ')
        while len(tokens) > 0:
            tk = tokens.pop(0)
            if tk == '|':
                break
            signal_patterns.append(tk)
        output_value = tokens
        data.append((signal_patterns, output_value))
    return data

def solve(data):
    # The general idea of this algorithm is as follows:
    # 1. Identify what number a pattern maps to
    # 2. Use that number -> pattern mapping to deduce some of the wire -> segment mappings 
    #       The wire -> segment mappings can be a COMPLETE mapping e.g. wire A -> segment B
    #       or a partial mappping e.g. wire A -> seg C or seg F 
    # 3. Use your inital mappings from being able to easily ident 1,4,7 and ad hoc rules
    #    to further refine the mapping and ident new number -> pattern segment mappings
    # 4. Keep id'ing numbers, keep refining map
    # 5. Repeat until map is done (e.g. every wire maps to one and only one segment)
    segms = {
        0: set("abcefg"), 1: set("cf"), 2: set("acdeg"), 3: set("acdfg"), 4: set("bcdf"),
        5: set("abdfg"), 6: set("abdefg"), 7: set("acf"), 8: set("abcdefg"), 9: set("abcdfg")
    }
    output_value_sum = 0
    for entry in data:
        seg_pool = set("abcdefg")
        wire_to_seg = {k:set() for k in "abcdefg"}
        ntp = {} # num to wire pattern 

        def update_mapping(num, pattern, num_to_pattern, segm_pool: set, wire_to_segm):
            num_to_pattern[num] = pattern
            mapping: set = segm_pool.intersection(segms[num])
            segm_pool.difference_update(segms[num])
            for wire in pattern:
                if len(wire_to_segm[wire]) == 0:
                    wire_to_segm[wire] = set(mapping)

        def update_mapping_but_different(num: int, ntp: dict, segms: dict, wire_to_seg: dict):
            # Gather the possible segments for number, according to our current, incomplete map
            p_segms = set()
            for wire in ntp[num]:
                p_segms.update(wire_to_seg[wire])

            # The segment 
            seg_to_rem = p_segms.difference(segms[num]).pop()
        
            rem_other = None
            for wire in ntp[num]:
                mapping = wire_to_seg[wire]
                if seg_to_rem in mapping:
                    wire_to_seg[wire].remove(seg_to_rem)
                    rem_other = set(wire_to_seg[wire])
                    rem_other = rem_other.pop()

            for wire in wire_to_seg:
                mapping = wire_to_seg[wire]
                if rem_other in mapping and len(mapping) > 1:
                    wire_to_seg[wire].remove(rem_other)

        segm_patterns = entry[0]
        output_values = entry[1]

        # Map (length of pattern) -> (list of patters with that length)
        patterns = dd(list)
        for pattern in segm_patterns:
            patterns[len(pattern)].append(pattern)
           
        # We can assign a number to patterns with unique lengths quite easily
        for num in (1,7,4):
            length = len(segms[num])
            pattern = patterns[length][0]
            update_mapping(num, pattern, ntp, seg_pool, wire_to_seg)

        # Next let's figure out the numbers that use 5 segments
        # Get the wires used for 1
        wires_for_1 = set(ntp[1])
        for pattern in patterns[5]:
            # 3 is the only number (of 2,5,3) that uses BOTH of the wires that 1 uses
            if len(wires_for_1.intersection(set(pattern))) == 2:
                update_mapping(3, pattern, ntp, seg_pool, wire_to_seg)

        # We should have 1 letter left in the segm pool. Assign it to the last remaining wire 
        last_segm = seg_pool.pop()
        for wire, mapping in wire_to_seg.items():
            if len(mapping) == 0:
                wire_to_seg[wire].add(last_segm)

        # Now let's refine the mapping. As it stands we will have some 1 to 1 mappings
        # between wires, but also some 1 -> 2 mappings. Let's get rid of those 1->2 mappings
        update_mapping_but_different(3, ntp, segms, wire_to_seg)

        # Now we can grab the wire that maps to the 'e' segment
        # Of 2,5, and 3, The 'e' segment is only used by 2; so we can use it
        # to identify the segment pattern that maps to the number 2
        ewire = None 
        for k,v in wire_to_seg.items():
            if v == set('e'):
                ewire = k 

        # Now we can pick 2 from the remaning segment patterns
        for pattern in patterns[5]:
            if ewire in pattern:
                ntp[2] = pattern 
       
        # Now we can finish refining our mapping
        update_mapping_but_different(2, ntp, segms, wire_to_seg)

        # AND WE HAVE A MAPPING of WIRE -> SEGMENT
        # It was messy, but it's done. Now we can decode the numbers. Yay!

        for k,v in wire_to_seg.items():
            wire_to_seg[k] = v.pop()
        
        # Decode the encoded output value strings from being wire descriptive, 
        # to being segment descriptive 
        decoded_output_patterns = []
        for pattern in output_values:
            decoded_pattern = ""
            for wire in pattern:
                decoded_pattern += wire_to_seg[wire]
            decoded_output_patterns.append(decoded_pattern)
        
        # Convert the now segment descriptive strings into a 4 digit number string
        num_str = ""
        for value_pattern in decoded_output_patterns:
            pset = set(value_pattern)
            for num,seg_pattern in segms.items():
                if pset == seg_pattern:
                    num_str += str(num)
        output_value_sum += int(num_str)
    return output_value_sum

def main(infile):
    return solve(process(infile))
    
if __name__ == "__main__":
    year, day = 2021, 8
    save_puzzle(year, day, __file__)
    aoc = AOC_Test(main, __file__)

    # TESTS, test against example input, other test input here
    aoc.test("day8ex.txt", ans=61229)

    # Run question 
    aoc.test("day8.txt", ans=998900, save_answer=True)

    # Submit if user passed in 'submit' on command line
    if len(sys.argv) > 1 and sys.argv[1] == "submit":
        puzzle = Puzzle(year=year, day=day)
        puzzle.answer_b = aoc.answer
