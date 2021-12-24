# https://adventofcode.com/2021/day/16

import sys
from typing import List
from aocd.models import Puzzle
from my_aoc_utils.utils import save_puzzle, AOC_Test

def process(infile):
    """Process the input file into a data structure for solve()"""
    return open(infile).readline().rstrip()

char_to_bits = {'0':'0000', '1':'0001', '2':'0010', '3':'0011', '4':'0100', '5':'0101', '6':'0110',
    '7':'0111', '8':'1000', '9':'1001', 'A':'1010', 'B': '1011', 'C': '1100', 'D':'1101', 
    'E':'1110', 'F':'1111'}

bits_to_char = {v:k for k,v in char_to_bits.items()}

pad = lambda bits: ('0'*(4-len(bits))) + bits if len(bits) < 4 else bits
to_char = lambda bits: bits_to_char[pad(bits)]
to_bits = lambda char: char_to_bits[char]

class Packet:
    def __init__(self, version, typeID, number=None) -> None:
        self.version: int = version
        self.typeID: int = typeID 
        self.number: int = number 
        self.packets: List[Packet] = []
    
    def __repr__(self) -> str:
        return f"pkt< v:{self.version}, t:{self.typeID}, n:{self.number}, sub:{len(self.packets)} >"

def process_packet(bin_str, i = 0):
    # i : start reading bits here
    # wlen : read this many bits 
    wlen = 3

    # Extract the header 
    # First three bits are the packet version 
    version = int(bin_str[i:i + wlen], base=2)
    i += 3
    
    # Packet type 
    typeID = int(bin_str[i:i + wlen], base=2)
    i += 3

    packet = Packet(version=version, typeID=typeID)

    # Packet represents literal value
    if typeID == 4:
        # Adjust window length to read chunks of 5 bits
        num_str = ""
        wlen += 2
        last_group = False 
        while not last_group:
            if wlen >= len(bin_str): break
            chunk = bin_str[i:i + wlen]
            last_group = False if chunk[0] == '1' else True
            num_str += chunk[1:]
            i += 5
        #return i, int(num_str, base=2)
        packet.number = int(num_str, base=2)
        return i, packet
    
    # Packet is operator
    else:
        # Get the length type ID 
        length_typeID = int(bin_str[i])
        i += 1

        # length type id is 0
        # The next 15 bits are number containing total length in bits 
        # of the sub packets contained by this packet
        if length_typeID == 0:
            length_in_bits = int(bin_str[i:i + 15], base=2)
            i += 15
            max_i = i + length_in_bits

            while i < max_i:
                i,res = process_packet(bin_str, i = i) 
                if res != None:
                    packet.packets.append(res)

        # length type id is 1
        # The next 11 bits are number describing NUM of sub-packets contained
        # in this packet 
        if length_typeID == 1:
            num_packets = int(bin_str[i:i + 11], base=2)
            i += 11
            for _ in range(num_packets):
                i,res = process_packet(bin_str, i = i)
                if res != None:
                    packet.packets.append(res)
    
        return i, packet

def solve(data):
    result = None 
    bin_str = ""

    # Convert string from hex to binary (as as string)
    for char in data:
        bin_str += to_bits(char)

    _, top_level_packet = process_packet(bin_str)

    # Run a bfs on the recursive packet structure and count the version numbers 
    version_num_sum = 0
    q = [top_level_packet]
    while len(q) > 0:
        packet = q.pop(0)
        version_num_sum += packet.version
        q.extend(packet.packets)
    
    return version_num_sum

def main(infile):
    return solve(process(infile))
    
if __name__ == "__main__":
    year, day = 2021, 16
    save_puzzle(year, day, __file__)
    aoc = AOC_Test(main, __file__)

    # TESTS, test against example input, other test input here
    aoc.test("ex0.txt", ans=16)
    aoc.test("ex1.txt", ans=12)
    aoc.test("ex2.txt", ans=23)
    aoc.test("ex3.txt", ans=31)

    # Run question 
    aoc.test("puzzle_input.txt", ans=-1, save_answer=True)

    # Submit if user passed in 'submit' on command line
    if len(sys.argv) > 1 and sys.argv[1] == "submit":
        puzzle = Puzzle(year=year, day=day)
        puzzle.answer_a = aoc.answer
