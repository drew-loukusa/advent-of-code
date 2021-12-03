#!/usr/bin/python3

nums_master = [
    int(n) for n in open("intcodes_input.txt").readline().rstrip().split(",")
]


def process_op(nums, i, op):
    a, b, c = nums[i + 1 : i + 4]
    nums[c] = op(nums[a], nums[b])


# Iterate through every possible combo of a and b from 0-99:
for a in range(100):
    for b in range(100):

        # Reset "memory" each time
        nums = nums_master[:]

        nums[1] = a
        nums[2] = b

        i = 0
        while i < len(nums):
            op = nums[i]
            if op == 99:
                break
            if op == 1:
                process_op(nums, i, lambda x, y: x + y)
            if op == 2:
                process_op(nums, i, lambda x, y: x * y)
            i += 4

        if nums[0] == 19690720:
            print(100 * a + b)
