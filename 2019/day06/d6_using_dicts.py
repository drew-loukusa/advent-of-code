data = [n.rstrip("\n") for n in open("d6_input.txt")]
# data = [ n.rstrip('\n') for n in  open("d6_test_input_p2.txt")]


def count(sat, i=0):
    if sat["par"]:
        i = count(sat["par"], i + 1)
    return i


def get_sat(name, sats):
    sat = None
    if name not in sats:
        sat = {"name": name, "par": None, "kids": []}
        sats[name] = sat
    else:
        sat = sats[name]
    return sat


def recurse_down(sat, transfers):
    for i, kid in enumerate(sat["kids"]):
        if kid and kid["name"] == "SAN":
            print(transfers)
        elif kid:
            recurse_down(kid, transfers + 1)
            sat["kids"][i] = None


def you_to_santa(sat, transfers):
    recurse_down(sat, transfers)
    if sat["par"] and sat["par"]["name"] != "SAN":
        you_to_santa(sat["par"], transfers + 1)
    elif sat["par"] and sat["par"]["name"] == "SAN":
        print(transfers)


sats = {}
for line in data:
    pname, cname = line.split(")")

    par = get_sat(pname, sats)
    kid = get_sat(cname, sats)

    par["kids"].append(kid)
    kid["par"] = par

# Part 1: 251208
orbit_count = 0
for name, sat in sats.items():
    orbit_count += count(sat)
print(orbit_count)

# Part 2: 397
you_to_santa(sats["YOU"]["par"], transfers=0)
