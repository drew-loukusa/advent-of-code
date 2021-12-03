data = [n.rstrip("\n") for n in open("d6_input.txt")]
# data = [ n.rstrip('\n') for n in  open("d6_test_input.txt")]
from collections import defaultdict

orbit_count = 0


class Node:
    def __init__(self, name):
        self.parent = None
        self.name = name
        self.children = []

    def dump(self):
        if self.parent != None:
            print(self.name, end="->")
            self.parent.dump()
        else:
            print(self.name)

    def count(self, i=0):
        if self.parent != None:
            i = self.parent.count(i + 1)
        return i


def get_sat(name, sats):
    node = None
    if name not in sats:
        node = Node(name)
        sats[name] = node
    else:
        node = sats[name]
    return node


sats = {}
for line in data:
    pname, cname = line.split(")")

    parent = get_sat(pname, sats)
    child = get_sat(cname, sats)

    parent.children.append(child)
    child.parent = parent

# P1 Answer: 251208
count = 0
for name, planet in sats.items():
    count += planet.count()
print(count)
