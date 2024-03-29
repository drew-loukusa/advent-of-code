# Before you leave, the Elves in accounting just need you to fix your expense
# report (your puzzle m); apparently, something isn't quite adding up.
# Specifically, they need you to find the two entries that sum to 2020 and
# then multiply those two numbers together.
# For example, suppose your expense report contained the following:

# 1721
# 979
# 366
# 299
# 675
# 1456

# In this list, the two entries that sum to 2020 are 1721 and 299. Multiplying them
# together produces 1721 * 299 = 514579, so the correct answer is 514579.
# Of course, your expense report is much larger. Find the two entries that
# sum to 2020; what do you get if you multiply them together?

example_input = [
    1721,
    979,
    366,
    299,
    675,
    1456,
]

day1_input = [int(item) for item in open("day1in.txt")]

# m = example_input
m = day1_input

# Part 1
if False:
    for i in range(len(m)):
        a = m[i]
        for j in range(i, len(m)):
            b = m[j]
            if a + b == 2020:
                print(a, b)
                print(a * b)

# Part 2

# Exmaple input: 979, 366, and 675. Multiplying them together produces the answer, 241861950.

# BRUUUUUUUUUUUUUUTE  FOOOOOOOOOOOOOOOOOOOORCE
if True:
    for i in range(len(m)):
        a = m[i]
        for j in range(i, len(m)):
            b = m[j]
            for k in range(j, len(m)):
                c = m[k]
                if a + b + c == 2020:
                    print(a, b, c)
                    print(a * b * c)
