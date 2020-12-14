from aocd.models import Puzzle
from collections import defaultdict
from copy import deepcopy

def save_input_to_file(puzzle, day):
    filename = "day" + str(day) + ".txt"
    with open(filename, mode='w+') as f:
        data = puzzle.input_data
        f.write(data)

Year=2020
Day=11

# puzzle = Puzzle(year=Year, day=Day)
# save_input_to_file(puzzle, day=Day)

#infile = "day11ex.txt"
infile = "C:\\source\\advent-of-code\\2020\\day11\\day11.txt"
infile = "C:\\source\\advent-of-code\\2020\\day11\\day11ex.txt"
infile = "day11.txt"
seats = [list(line.rstrip()) for line in open(infile)]

seats_dict = defaultdict(dict)
for row, y in zip(seats, range(len(seats))): 
    for seat, x in zip(row, range(len(row))):
        seats_dict[y][x] = seat
seats = seats_dict

MAX_X = len(seats[0]) - 1
MAX_Y = len(seats) - 1

print(f"MAX_X: {MAX_X}")
print(f"MAX_Y: {MAX_Y}")

def is_empty(seats, x,y):
    return seats[y][x] in ['L', '.']

def is_occupied(seats, x,y):
    return not is_empty(seats, x, y)

def adjacent_occupied(seats, x, y):
    occupied_seats = 0
    # Count seats above: From (x-1, y-1) -> (x+1, y-1)
    if y > 0:
        if x > 0     and is_occupied(seats, x-1, y-1): occupied_seats += 1
        if is_occupied(seats, x, y-1): occupied_seats += 1
        if x < MAX_X and is_occupied(seats, x+1, y-1): occupied_seats += 1


    # Count seats left and right: (x-1, y), (x+1, y)
    if x > 0     and is_occupied(seats, x-1, y): occupied_seats += 1
    if x < MAX_X and is_occupied(seats, x+1, y): occupied_seats += 1

    # Count seats below: From (x-1, y+1) -> (x+1 y+1)
    if y < MAX_Y:
        if x > 0     and is_occupied(seats, x-1, y+1): occupied_seats += 1
        if is_occupied(seats, x, y+1): occupied_seats += 1
        if x < MAX_X and is_occupied(seats, x+1, y+1): occupied_seats += 1

    return occupied_seats

def update_seat(seats, seats_copy, x, y):

    # Return 1 or -1 based on if seat was updated to "occupied" or "empty"
    
    # DEF: Adjacent: one of the eight positions immediately up, down, left, right, or diagonal from a seat
    
    # The seat becomes occupied:
    # > If a seat is empty (L) AND
    # > There are no occupied seats adjacent to it
    if is_empty(seats, x, y) and adjacent_occupied(seats, x, y) == 0:
        seats_copy[y][x] = '#'
        return 1

    # The seat becomes empty:
    # > If a seat is occupied (#) AND 
    # > Four or more seats adjacent to it are also occupied
    if not is_empty(seats, x, y) and adjacent_occupied(seats, x ,y) >= 4:
        seats_copy[y][x] = 'L'
        return -1

    # Seat state did not change
    return 0 

def simulate_round(seats, seats_copy, occupied_seats):
    for y, row in seats.items():
        for x, seat in row.items():
            if seat == '.': continue 
            occupied_seats += update_seat(seats, seats_copy, x, y)
    
    return occupied_seats

# Part 1
if False:
    last_count = 0
    seats_copy = deepcopy(seats)
    occupied_count = simulate_round(seats, seats_copy, last_count)
    while last_count != occupied_count:
        last_count = occupied_count
        seats = seats_copy 
        seats_copy = deepcopy(seats)
        occupied_count = simulate_round(seats, seats_copy, occupied_count)      
    
    print(occupied_count)
    #puzzle.answer_a = result

def in_bounds(loc):
    x,y = loc
    return (x >= 0 and x <= MAX_X) and (y >= 0 and y <= MAX_Y)

def line_of_sight_occupied(seats, x, y):
    occupied_seats = 0
    # Check each 8 directions
    dirs = [('+','+'), ('', '+'), ('-','+'), ('-', ''), ('-','-'), ('', '-'), ('+', '-'), ('+', '')]
    for x_dir, y_dir in dirs:
        # Look in direction until occupied seat or wall is found 
        cx, cy = x, y
        while in_bounds((cx, cy)):
            if   x_dir == '+': cx += 1
            elif x_dir == '-': cx -= 1
            if   y_dir == '+': cy += 1
            elif y_dir == '-': cy -= 1
            if in_bounds((cx,cy)):
                if is_occupied(seats, cx, cy):
                    occupied_seats += 1
                    break 
                elif seats[cy][cx] == 'L':
                    break 
    return occupied_seats

def update_seat_vis(seats, seats_copy, x, y):

    # Return 1 or -1 based on if seat was updated to "occupied" or "empty"
    
    # DEF: Adjacent: one of the eight positions immediately up, down, left, right, or diagonal from a seat
    
    # The seat becomes occupied:
    # > If a seat is empty (L) AND
    # > There are no occupied seats adjacent to it
    if is_empty(seats, x, y) and line_of_sight_occupied(seats, x, y) == 0:
        seats_copy[y][x] = '#'
        return 1

    # The seat becomes empty:
    # > If a seat is occupied (#) AND 
    # > Four or more seats adjacent to it are also occupied
    if not is_empty(seats, x, y) and line_of_sight_occupied(seats, x ,y) >= 5:
        seats_copy[y][x] = 'L'
        return -1

    # Seat state did not change
    return 0 

def simulate_round_vis(seats, seats_copy, occupied_seats):
    for y, row in seats.items():
        for x, seat in row.items():
            if seat == '.': continue 
            occupied_seats += update_seat_vis(seats, seats_copy, x, y)
    
    return occupied_seats


# Part 2
if True:
    last_count = 0
    seats_copy = deepcopy(seats)
    occupied_count = simulate_round_vis(seats, seats_copy, last_count)
    while last_count != occupied_count:
        last_count = occupied_count
        seats = seats_copy 
        seats_copy = deepcopy(seats)
        occupied_count = simulate_round_vis(seats, seats_copy, occupied_count)  
        # print(occupied_count)    
    
    print(occupied_count)

    #puzzle.answer_b = result
