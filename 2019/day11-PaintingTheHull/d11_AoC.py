from collections import defaultdict
from time import sleep
import sys
import os


class Computer:
    def __init__(self, tape, name=None, inp_stack=None, output_mode=None):
        self.name = name
        self.enabled = True
        self.tape = tape  # Stores this comptuers program
        self.inp_stack = inp_stack  # Op code 3 gets input from here

        if self.inp_stack == None:
            self.inp_stack = []

        self.i = 0  # Instruction pointer
        self.rel_base = 0

        self.output_mode = output_mode  # By default, output is printed to stdout
        # if mode='return', execution in method compute()
        # pauses and the output is returned to the calling thread

        self.last_computed_value = 0

        self.output_list = []

        # Increase the amount of "empty memory" available by default:
        self.tape += [0 for n in range(len(self.tape) * 500)]

        # Make tape a dict because why not ? Just doing this to see if it will be faster.
        # self.tape = { n:val for n,val in enumerate(self.tape) }

    def set_input(self, items: list):
        self.inp_stack = items

    def cur_instr(self):
        """Get instruction pointed at by self.i"""
        return self.tape[self.i]

    def set_(self, index, val):
        """Set value at position 'index' to be 'val'"""
        self.tape[index] = val

    def get_(self, index):
        """Return value stored at 'index'"""
        return self.tape[index]

    def get_indexes(self, *args):
        """Method for handeling the three different parameter modes.

        Accepts up to N args which are the modes for N parameters.

        Based on what a,b and c, etc are, returns the appropriate index to be used.
        a,b, and c, etc are the parameter modes.

        If you enter a, it will return just one index.
        If you enter a and b, it will return two indexes.
        If you enter a, b, and c, it will return three indexes.

        Up to N arguments.

        Modes:
        -----------------------------------------------------------
        The default mode is set to be immediate mode (mode 1):
        Indexes will be offsets of the current instruction pointer

        Positional mode: (mode 0)
        Indexes will be values located at addresses pointed at by
        whatever is at the current pointer offset locations:

        Relative mode: (mode 2)
        Same as positional mode, but add the current relative base to the index
        """

        def get_index(a, offset):
            p = self.i + offset  # Imediate mode
            if a == 0:
                p = self.get_(p)  # Positional
            elif a == 2:
                p = self.rel_base + self.get_(p)  # Relative
            return p

        indexes = [get_index(arg, offset) for offset, arg in enumerate(args, start=1)]

        return indexes[0] if len(indexes) == 1 else indexes

    def compute(self, user_inp=None):
        """Iterates over self.tape, executing instructions until a HALT op is encountered,
        or data is returned (op 4) which pauses execution of the computer
        """
        # NOTE: '<index>' Is read as, The value at 'index'.
        # EXAMPLE: <p1> + <p2> Is read as " The value at index p1 plus the value at index p2 "

        if user_inp != None:
            self.inp_stack.insert(0, user_inp)

        while self.i < len(self.tape):
            # Process instruction:
            instr = str(self.cur_instr())
            op = instr[len(instr) - 2 :]

            # Extract parameter modes from the instruction:
            pmodes = instr[: len(instr) - 2]
            m1, m2, m3 = 0, 0, 0
            if len(pmodes) > 0:
                pmodes = list(pmodes)
                reversed(pmodes)
                if len(pmodes) > 0:
                    m1 = int(pmodes.pop())
                if len(pmodes) > 0:
                    m2 = int(pmodes.pop())
                if len(pmodes) > 0:
                    m3 = int(pmodes.pop())

            # Make sure op is in correct format:
            if len(op) == 1:
                op = "0" + op

            # Execute the op:
            if op == "01":  # Adds <p1> + <p2>
                p1, p2, p3 = self.get_indexes(m1, m2, m3)
                self.set_(p3, val=(self.get_(p1) + self.get_(p2)))
                self.i += 4

            elif op == "02":  # Multiplies <p1> * <p2>
                p1, p2, p3 = self.get_indexes(m1, m2, m3)
                self.set_(p3, val=(self.get_(p1) * self.get_(p2)))
                self.i += 4

            elif op == "03":  # Get input
                # user_in = input(">>> type a number: ")
                user_in = self.inp_stack.pop(0)
                p1 = self.get_indexes(m1)
                self.set_(p1, val=int(user_in))
                self.i += 2

            elif op == "04":  # Return output
                p1 = self.get_indexes(m1)
                output = self.get_(p1)
                self.last_computed_value = output

                self.i += 2  # Increment BEFORE returning

                self.output_list.append(output)
                if len(self.output_list) == 2:
                    copy = self.output_list[:]
                    self.output_list = []
                    return copy
                # if self.output_mode=='return': return output
                # else:                          print(output)

            elif (
                op == "05"
            ):  # Jump-If-True: Sets instr pointer to <p2> if <p1> is non-zero
                p1, p2 = self.get_indexes(m1, m2)
                if self.get_(p1) > 0:
                    self.i = self.get_(p2)
                else:
                    self.i += 3

            elif (
                op == "06"
            ):  # Jump-If-False: Sets instr pointer to <p2> if <p1> is zero
                p1, p2 = self.get_indexes(m1, m2)
                if self.get_(p1) == 0:
                    self.i = self.get_(p2)
                else:
                    self.i += 3

            elif op == "07":  # Stores 1 in <p3> if <p1> < <p2> else stores 0
                p1, p2, p3 = self.get_indexes(m1, m2, m3)
                if self.get_(p1) < self.get_(p2):
                    self.set_(p3, val=1)
                else:
                    self.set_(p3, val=0)
                self.i += 4

            elif op == "08":  # Stores 1 if <p1> == <p2> else stores 1
                p1, p2, p3 = self.get_indexes(m1, m2, m3)
                if self.get_(p1) == self.get_(p2):
                    self.set_(p3, val=1)
                else:
                    self.set_(p3, val=0)
                self.i += 4

            elif op == "09":  # Change the relative boost value:
                p1 = self.get_indexes(m1)
                self.rel_base += self.get_(p1)
                self.i += 2

            elif op == "99":
                self.enabled = False
                self.i == len(self.tape)
                return "HALT"


get_data = lambda path: [int(n.rstrip("\n")) for n in open(path).readline().split(",")]

# +----------------------------------------------------------------------------+
# |                                  Part 1                                    |
# +----------------------------------------------------------------------------+

G_OFFSET = 10


class HullPainter:
    def __init__(self, data):
        self.computer = Computer(tape=data, output_mode="return")
        self.x = 0
        self.y = 0
        self.painted = defaultdict(int)
        self.dirs = ["up", "right", "down", "left"]
        self.dir_str = "up"
        self.dir_p = 0

        self.painted_black = 0
        self.painted_white = 0

    def get_loc(self):
        return self.x, self.y

    def get_dir(self):
        return self.dirs[self.dir_p]

    def change_dir(self, turn_dir):
        if turn_dir == 0:  # Turn left
            self.dir_p -= 1
            if self.dir_p < 0:
                self.dir_p = 3

        if turn_dir == 1:  # Turn right
            self.dir_p += 1
            if self.dir_p > 3:
                self.dir_p = 0

        self.dir_str = self.get_dir()

    def move(self):
        cur_dir = self.get_dir()
        if cur_dir == "up":
            self.y -= 1
        if cur_dir == "down":
            self.y += 1
        if cur_dir == "right":
            self.x += 1
        if cur_dir == "left":
            self.x -= 1

    def move_cursor(self, row, col):
        print(f"\u001b[{row};{col}H", end="")

    def paint_hull(self, visualize=False, interval=0):
        if visualize:
            if os.name == "nt":
                os.system("cls")
            else:
                os.system("clear")
                os.system("setterm -cursor off")

        max_row = 0
        cycles = 0
        while self.computer.enabled:

            self.move_cursor(0, 0)
            print("Cycles:", cycles)

            # Get current location:
            cur_loc = self.get_loc()

            if visualize:  # Print robot direction:
                col, row = cur_loc
                self.move_cursor(row + G_OFFSET, col + G_OFFSET)
                icons = {"up": "▲", "down": "▼", "left": "◀", "right": "▶"}
                print(icons[self.dir_str])

            # Get Current Color: (Default is black)
            cur_color = self.painted[cur_loc]

            # Send color to computer:
            if cycles == 0:
                cur_color = 1
            self.computer.inp_stack = [cur_color]

            # Get new color and new direction:
            result = self.computer.compute()
            if result == "HALT":
                continue
            new_color, new_dirc = result

            self.painted[cur_loc] = new_color  # Paint
            self.change_dir(new_dirc)  # Turn
            self.move()  # ...

            if new_color == 0:
                self.painted_black += 1
            else:
                self.painted_white += 1

            # For visulazation:
            if visualize:
                sleep(interval)
                col, row = cur_loc
                col, row = col + G_OFFSET, row + G_OFFSET
                self.move_cursor(row, col)
                if new_color == 1:
                    print("▮")
                if new_color == 0:
                    print(".")

                if row > max_row:
                    max_row = row
            cycles += 1

        if visualize:
            if os.name == "posix":
                os.system("setterm -cursor on")
            # Move cursor to bottom of the picture:
            print(f"\u001b[{max_row+G_OFFSET};{0}H", end="")

        print("Robot cycles:", cycles)


if __name__ == "__main__":
    try:
        bobby = HullPainter(get_data("d11_input.txt"))
        bobby.paint_hull(visualize=True, interval=0.01)
        # bobby.paint_hull()
        print("Panels Painted:", len(bobby.painted))
        print("Black:", bobby.painted_black, "White:", bobby.painted_white)
    except KeyboardInterrupt:
        if os.name == "nt":
            os.system("cls")
            os.system("cls")
        else:
            os.system("clear")
            os.system("clear")
            os.system("setterm -cursor off")
