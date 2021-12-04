# https://adventofcode.com/2021/day/4

from os import unlink
import sys
from collections import defaultdict as dd
from typing import List
from aocd.models import Puzzle
from my_aoc_utils.utils import save_puzzle, AOC_Test

BINGO_SIZE = 5
class BingoBoard:
    def __init__(self, lines, val_to_board: dict = None):
        self.vals = {}
        for y, row in enumerate(lines):
            row_vals = [int(n) for n in row.split(' ') if n != '']
            for x, n, in enumerate(row_vals):
                self.vals[n] = (y,x)

                # Map value to list of boards that have said value in them
                if val_to_board != None:
                    val_to_board[n].append(self)

        self.rows = {n:set() for n in range(BINGO_SIZE)}
        self.cols = {n:set() for n in range(BINGO_SIZE)}
    
def process(infile):
    """Process the input file into a data structure for solve()"""
    return [line.rstrip() for line in open(infile)]

def make_boards(data):
    value_to_board = dd(list)
    boards = []
    i = 0
    while i < len(data):
        rows = []
        for _ in range(5):
            rows.append(data[i])
            i += 1
        boards.append(BingoBoard(rows, value_to_board))
        i += 1
    return boards, value_to_board
  
def next_winning_board(nums, vals_to_board, boards: List[BingoBoard]):
    """
    Given a list of numbers and a list of boards, find the next winning board.
    This function returns the remaining nums that were left after locating the next winning board, 
    the last number drawn, and the winning board in a tuple: (winning_board, last_number_drawn, remaning nums)

    If there are no nums left, then remaining_nums will be None
    """
    winning_board = None
    last_num_drawn = 0
    remaning_nums = None 
    for num_i, num in enumerate(nums):

        if last_num_drawn != 0 and winning_board is not None:
            break

        for board in vals_to_board[num]:
            board: BingoBoard
            coords = board.vals.get(num)

            if coords is None:
                continue
            y,x = coords

            board.rows[y].add(num)
            board.cols[x].add(num)

            if len(board.rows[y]) == BINGO_SIZE or \
                len(board.cols[x]) == BINGO_SIZE:
                winning_board = board
                last_num_drawn = num
                if num_i + 1 < len(nums):
                    remaning_nums = nums[num_i+1:]
                break

    return winning_board, last_num_drawn, remaning_nums

def sum_unmarked_values(board: BingoBoard):
    unmarked_sum = 0
    for k in board.vals:
        y,x = board.vals[k]
        if k not in board.rows[y] and \
            k not in board.cols[x]:
            unmarked_sum += k
    return unmarked_sum

def solve(data):
    nums = [ int(n) for n in data[0].split(',')]
    boards, vals_to_board = make_boards(data[2:])
    win_board, last_num_drawn, _ = next_winning_board(nums, vals_to_board, boards)
    unmarked_sum = sum_unmarked_values(win_board)
    return last_num_drawn * unmarked_sum

def main(infile):
    return solve(process(infile))

if __name__ == "__main__":
    year, day = 2021, 4
    save_puzzle(year, day, __file__)
    aoc = AOC_Test(main, __file__)

    # TESTS, test against example input, other test input here
    aoc.test("day4ex.txt", ans=4512)

    # Run question
    aoc.test("day4.txt", ans=51034, save_answer=True)

    # Submit if user passed in 'submit' on command line
    if len(sys.argv) > 1 and sys.argv[1] == "submit":
        puzzle = Puzzle(year=year, day=day)
        puzzle.answer_a = aoc.answer
