get_data = lambda path: [ int(n.rstrip('\n')) for n in open(path).readline().split(',')]

#+----------------------------------------------------------------------------+
#|                                  Tests                                     |
#+----------------------------------------------------------------------------+
if True:
    data = get_data("d10_p2_test1.txt")
    data = get_data("d10_p2_test2.txt")
    pass

data = get_data("d10_input.txt")