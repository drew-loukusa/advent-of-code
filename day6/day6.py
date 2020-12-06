from aocd.models import Puzzle
from collections import defaultdict
def save_input_to_file(puzzle, day):
    filename = "day" + str(day) + ".txt"
    with open(filename, mode='w+') as f:
        data = puzzle.input_data
        f.write(data)

Year=2020
Day=6

puzzle = Puzzle(year=Year, day=Day)
#save_input_to_file(puzzle, day=Day)

infile = "day6ex.txt"
infile = "day6.txt"
lines = [line.rstrip() for line in open(infile)]

# Part 1
if False:
    sum_count = 0
    cur_set = set()
    for line in lines: 
        for c in line: 
            #print(f"Adding {c} to cur set")
            cur_set.add(c)
        
        if len(line) == 0:
            #print(f"Found {len(cur_set)} in set ")
            sum_count += len(cur_set)
            cur_set = set()
            
  
   # print(f"Found {len(cur_set)} in set ")
    sum_count += len(cur_set)
    cur_set = set()
            
    #puzzle.answer_a = sum_count
    print(sum_count)
# Part 2

if True:
    sum_count = 0
    personID = 0
    cur_group = defaultdict(set)
    for line in lines: 
        for c in line: 
            #print(f"Adding {c} to cur set")
            cur_group[personID].add(c)
        personID += 1

        if len(line) == 0:
            common_qs = set("abcdefghijklmnopqrstuvwxqyz")
            for k,v in cur_group.items():
                common_qs = common_qs & v
            sum_count += len(common_qs)
            cur_group = defaultdict(set)
            personID = 0

   # print(f"Found {len(cur_set)} in set ")
    common_qs = set("abcdefghijklmnopqrstuvwxqyz")
    for k,v in cur_group.items():
        common_qs = common_qs & v
    sum_count += len(common_qs)
    cur_group = defaultdict(set)
    personID = 0
    
    print(sum_count)

    #puzzle.answer_b = sum_count
