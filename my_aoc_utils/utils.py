import os
from aocd.models import Puzzle
from my_aoc_utils.test_func import FunctionTester

def save_puzzle(year, day, current_script_path):
    """Save puzzle to file, but only if it doesn't already exist"""
    file_name = f"puzzle_input.txt"
    abs_file_path = abs_path(current_script_path, file_name)
    if not os.path.exists(abs_file_path):
        puzzle = Puzzle(year=year, day=day)
        with open(abs_file_path, mode='w+') as f:
            data = puzzle.input_data
            f.write(data)

def abs_path(dunder_file, file_name):
    """Get absolute path to file with name 'file_name' that lives in the same directory as dayN.py """
    script = os.path.realpath(dunder_file)
    head, _ = os.path.split(script)
    return os.path.join(head, file_name)

class AOC_Test:
    def __init__(self, function, script_path: str) -> None:
        self.ft = FunctionTester(function)
        # What is the absolute path of the dayN.py script, so that the test function knows how to load 
        # the input file 
        self.script_path = script_path
        self.answer = None

    def test(self, input_file_name, ans, save_answer=False):
        input_abs_path = abs_path(self.script_path, input_file_name)
        answer = self.ft.test(file_name=input_abs_path, ans=ans)
        if save_answer:
            self.answer = answer
        return answer 
