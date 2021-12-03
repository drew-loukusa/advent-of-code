data = [n.rstrip("\n") for n in open("d6_input.txt")]
data = [n.rstrip("\n") for n in open("d6_test_input_p2.txt")]
from collections import defaultdict

orbit_count = 0


class Node:
    def __init__(self, name):
        self.parent = None
        self.name = name
        self.children = []

    def dump(self):
        if self.parent:
            print(self.name, end="->")
            self.parent.dump()
        else:
            print(self.name)

    def count(self, i=0):
        if self.parent:
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


def recurse_down(node, transfers):
    for i, child in enumerate(node.children):
        if child and child.name == "SAN":
            print(transfers)
        elif child:
            recurse_down(child, transfers + 1)
            node.children[i] = None


def you_to_santa(node, transfers):
    recurse_down(node, transfers)
    if node.parent and node.parent.name != "SAN":
        you_to_santa(node.parent, transfers + 1)
    elif node.parent and node.parent.name == "SAN":
        print(transfers)


sats = {}
for line in data:
    pname, cname = line.split(")")

    parent = get_sat(pname, sats)
    child = get_sat(cname, sats)

    parent.children.append(child)
    child.parent = parent
you_to_santa(sats["YOU"].parent, transfers=0)
