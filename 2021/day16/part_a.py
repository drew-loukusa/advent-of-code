# https://adventofcode.com/2021/day/16

import sys
from typing import List
from aocd.models import Puzzle
from my_aoc_utils.utils import save_puzzle, AOC_Test

CHAR_TO_BITS = {'0':'0000', '1':'0001', '2':'0010', '3':'0011', '4':'0100', '5':'0101', '6':'0110',
    '7':'0111', '8':'1000', '9':'1001', 'A':'1010', 'B': '1011', 'C': '1100', 'D':'1101', 
    'E':'1110', 'F':'1111'}

def process(infile):
    """Process the input file into a data structure for solve()"""
    hex_str = open(infile).readline().rstrip()

    bin_str = ""
    # Convert string from hex to binary (as as string)
    for char in hex_str:
        bin_str += CHAR_TO_BITS[char]
    
    return bin_str

class Packet:
    def __init__(self, version, typeID, value=None) -> None:
        self.version: int = version
        self.typeID: int = typeID 
        self.value: int = value 
        self.packets: List[Packet] = []
    
    def __repr__(self) -> str:
        return f"pkt< v:{self.version}, t:{self.typeID}, n:{self.value}, sub:{len(self.packets)} >"

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
        packet.value = int(num_str, base=2)
        return i, packet
    
    # Packet is operation packet
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

            # Process the sub packets
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

            # Process the sub packets
            for _ in range(num_packets):
                i,res = process_packet(bin_str, i = i)
                if res != None:
                    packet.packets.append(res)

        # Sub packets are processed, execute the operation

        if packet.typeID == 0:
            if packet.value is None:
                packet.value = 0
            for sub in packet.packets:
                packet.value += sub.value 
                
        if packet.typeID == 1:
            prod = 1
            for sub in packet.packets:
                prod *= sub.value
            packet.value = prod

        if packet.typeID == 2:
            min_val = None
            for sub in packet.packets:
                if min_val is None:
                    min_val = sub.value
                else:
                    min_val = min(min_val, sub.value)
            packet.value = min_val

        if packet.typeID == 3:
            max_val = None
            for sub in packet.packets:
                if max_val is None:
                    max_val = sub.value
                else:
                    max_val = max(max_val, sub.value)
            packet.value = max_val

        if packet.typeID == 5:
            a,b = packet.packets
            packet.value = 1 if a.value > b.value else 0

        if packet.typeID == 6:
            a,b = packet.packets
            packet.value = 1 if a.value < b.value else 0

        if packet.typeID == 7:
            a,b = packet.packets
            packet.value = 1 if a.value == b.value else 0
    
        return i, packet

def solve(bin_str):
    # Process the 'packet' (and any sub packets)
    top_level_packet: Packet = process_packet(bin_str)[1]
    
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
    aoc.test("puzzle_input.txt", ans=969, save_answer=True)

    # Submit if user passed in 'submit' on command line
    if len(sys.argv) > 1 and sys.argv[1] == "submit":
        puzzle = Puzzle(year=year, day=day)
        puzzle.answer_a = aoc.answer
