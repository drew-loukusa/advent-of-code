#!/usr/bin/python3

nums = [int(n) for n in open("intcodes_input.txt").readline().rstrip().split(',')]



nums[1] = 12
nums[2] = 2

print(nums)

def process_op(nums, op,a,b,res):
    a = nums[a]
    b = nums[b]
    nums[res] = op(a,b)

i = 0
while i < len(nums):
    # Process op code
    op = nums[i] 
    if op == 99: break
    if op == 1: 
        process_op(nums, lambda x,y: x + y, nums[i+1], nums[i+2], nums[i+3])
    if op == 2: 
        process_op(nums, lambda x,y: x * y, nums[i+1], nums[i+2], nums[i+3])

    i += 4

print(nums)
print(nums[0])