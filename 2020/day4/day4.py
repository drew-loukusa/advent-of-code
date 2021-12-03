from aocd.models import Puzzle
import re


def save_input_to_file(puzzle, day):
    filename = "day" + str(day) + ".txt"
    with open(filename, mode="w+") as f:
        data = puzzle.input_data
        f.write(data)


Year = 2020
Day = 4

puzzle = Puzzle(year=Year, day=Day)
# save_input_to_file(puzzle, day=Day)

infile = "day4ex.txt"
infile = "day4invalid.txt"
infile = "day4valid.txt"
infile = "day4.txt"
lines = [line.rstrip() for line in open(infile)]

valid_fields_no_cid = {
    "valid",
    "byr",
    "iyr",
    "eyr",
    "hgt",
    "hcl",
    "ecl",
    "pid",
}

valid_fields = {
    "valid",
    "byr",
    "iyr",
    "eyr",
    "hgt",
    "hcl",
    "ecl",
    "pid",
    "cid",
}


# Part 1
if False:
    num_valid = 0
    all_passports = []
    current_passport = {"valid": True}
    encountered_fields = set()

    for line in lines:
        # Split line on spaces
        spaces = line.split(" ")
        # print(spaces)
        if len(spaces[0]) == 0:
            # print("NEW PASSPORT")
            all_passports.append(current_passport)
            current_passport = {"valid": True}
            encountered_fields = set()
            continue

        # split each token on ':'
        for field in spaces:
            k, v = field.split(":")
            # print(k,v)
            encountered_fields.add(k)
            current_passport[k] = v

    all_passports.append(current_passport)

    for passport in all_passports:
        if (
            set(passport.keys()) == valid_fields_no_cid
            or set(passport.keys()) == valid_fields
        ):
            passport["valid"] = True
            num_valid += 1

    print(num_valid)
    # print(*all_passports, sep='\n')
    # print(len(all_passports))
    # puzzle.answer_a = num_valid

# Part 2
if True:
    num_valid = 0
    all_passports = []
    current_passport = {"valid": False}
    encountered_fields = set()

    for line in lines:
        # Split line on spaces
        spaces = line.split(" ")
        # print(spaces)
        if len(spaces[0]) == 0:
            # print("NEW PASSPORT")
            all_passports.append(current_passport)
            current_passport = {"valid": False}
            encountered_fields = set()
            continue

        # split each token on ':'
        for field in spaces:
            k, v = field.split(":")
            # print(k,v)
            encountered_fields.add(k)
            current_passport[k] = v

    all_passports.append(current_passport)

    for passport in all_passports:
        if (
            set(passport.keys()) == valid_fields_no_cid
            or set(passport.keys()) == valid_fields
        ):

            passport["valid"] = True

            for k, v in passport.items():
                if k == "byr":
                    # print(f"{k},'{v}'")
                    if re.match(r"(\d{4})", v) and int(v) >= 1920 and int(v) <= 2002:
                        # print("Found valid byr:", k,v)
                        pass
                    else:
                        # print("bad field:", k,v)
                        passport["valid"] = False
                if k == "iyr":
                    if re.match(r"(\d{4})", v) and int(v) >= 2010 and int(v) <= 2020:
                        # print("valid iyr", k,v)
                        pass
                    else:
                        # print("bad field:", k,v)
                        passport["valid"] = False
                if k == "eyr":
                    if re.match(r"(\d{4})", v) and int(v) >= 2020 and int(v) <= 2030:
                        # print("valid eyr", k,v)
                        pass
                    else:
                        # print("bad field:", k,v)
                        passport["valid"] = False
                if k == "hgt":
                    if p := re.match(r"(\d+)(cm|in)", v):
                        num = p.group(1)
                        meas = p.group(2)
                        if (meas == "cm" and int(num) >= 150 and int(num) <= 193) or (
                            meas == "in" and int(num) >= 59 and int(num) <= 76
                        ):
                            # print("valid", k,v)
                            pass
                        else:
                            # print("bad field:", k,v)
                            passport["valid"] = False
                    else:
                        passport["valid"] = False
                        # print("bad field:", k,v)
                if k == "hcl":
                    if re.match(r"#(\w{6}|\d{6})", v):
                        # print("valid",k,v)
                        pass
                    else:
                        passport["valid"] = False
                        # print("invalid", k,v)
                if k == "ecl":
                    if re.match(r"(amb|blu|brn|gry|grn|hzl|oth)", v):
                        # print("valid",k,v)
                        pass
                    else:
                        passport["valid"] = False
                        # print("invalid", k,v)
                if k == "pid":
                    if re.match(r"^\d{9}$", v):
                        pass
                    else:
                        passport["valid"] = False

                if k == "cid":
                    pass

            if passport["valid"] == True:
                num_valid += 1

    # print(len(all_passports))
    print(num_valid)
    # print(*all_passports, sep='\n')
    puzzle.answer_b = num_valid
