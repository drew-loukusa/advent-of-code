from aocd.models import Puzzle


def save_input_to_file(puzzle, day):
    filename = "day" + str(day) + ".txt"
    with open(filename, mode="w+") as f:
        data = puzzle.input_data
        f.write(data)


Year = 2020
Day = 9

# puzzle = Puzzle(year=Year, day=Day)
# save_input_to_file(puzzle, day=Day)

infile, window_len = "day9ex.txt", 5
infile, window_len = "day9.txt", 25
nums = [int(line) for line in open(infile)]

# Part 1
if False:
    cur_sum = 0
    for i in range(len(nums)):
        if (i + window_len) >= len(nums):
            break
        window = nums[i : i + window_len]
        # print("window", window)
        # Get sum to check
        cur_sum = nums[i + window_len]
        # print("cur_sum", cur_sum)

        # Find if cur_sum is a possible sum of a pair of nums the window
        invalid_sum = True
        for i in range(len(window)):
            if not invalid_sum:
                break
            # Get first number in pairing
            num = window[i]
            # print("num1", num)
            if num > cur_sum:
                continue
            elif cur_sum == num:
                invalid_sum = False
                break
            elif i == len(window):
                break
            else:
                for rnum in window[i + 1 :]:
                    # print(num ,"+", rnum)
                    if num + rnum == cur_sum:
                        # print("Found valid sum", num, "+", rnum)
                        invalid_sum = False
                        break
        # input(">>>")

        if invalid_sum:
            print("Found invalid sum", cur_sum)
            break

    print(cur_sum)
    # puzzle.answer_a = result

# Part 2
if True:
    window_found = False
    target = 138879426
    nums = nums[::-1]
    win_len = 2
    while True:
        if window_found:
            break
        for i in range(len(nums)):
            window = nums[i : i + win_len]
            if sum(window) == target:
                window_found = True
                print("Window found!")
                print("Window len:", win_len)
                print(window)
                print(min(window) + max(window))
                break
        win_len += 1

    # puzzle.answer_b = result

    # Possible optimizations
    # ==================================================================
    # when we shift the window, we will be recalculating a lot of sums,
    # If we could find a way to save those calculations and re-use them...

    # keep the window sorted, maintain dict of num->(index in sorted window), and a queue of
    # the indexes

    # then you can use binary search on the sorted window to search for the second number in
    # sum pairings
