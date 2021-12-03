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
        self.ball_loc = [0, 0]  # col, row
        self.pad_loc = [0, 0]  # col, row
        self.blocks = {}

        self.game_running = False

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

    def compute(self, user_inp=None, interval=0):
        """Iterates over self.tape, executing instructions until a HALT op is encountered,
        or data is returned (op 4) which pauses execution of the computer
        """
        # NOTE: '<index>' Is read as, The value at 'index'.
        # EXAMPLE: <p1> + <p2> Is read as " The value at index p1 plus the value at index p2 "

        def move_cursor(row, col):
            print(f"\u001b[{row};{col}H", end="")

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
                move_cursor(row=24, col=0)
                self.game_running = True
                # user_in = input(">>> Type in a number: ")
                # while len(user_in) == 0 or user_in not in ['0','1','-1']:
                #     user_in = input(">>> Type in a number: ")
                user_in = 0
                if self.ball_loc[0] < self.pad_loc[0]:
                    user_in = -1

                if self.ball_loc[0] > self.pad_loc[0]:
                    user_in = 1

                if self.ball_loc[0] == self.pad_loc[0]:
                    user_in = 0

                # user_in = self.inp_stack.pop(0)
                p1 = self.get_indexes(m1)
                self.set_(p1, val=int(user_in))
                self.i += 2

            elif op == "04":  # Return output
                if self.game_running:
                    sleep(interval)
                p1 = self.get_indexes(m1)
                output = self.get_(p1)
                self.last_computed_value = output

                self.i += 2  # Increment BEFORE returning

                self.output_list.append(output)
                # If we have 3 items to output, draw to the screen:
                if len(self.output_list) == 3:

                    tile_id = self.output_list.pop()
                    row = self.output_list.pop()
                    col = self.output_list.pop()

                    # move_cursor(row, col)

                    if col == -1 and row == 0:
                        move_cursor(row=25, col=0)
                        print("Score:", tile_id)

                    if tile_id == 0:
                        continue
                    if tile_id == 1:
                        move_cursor(row, col)
                        print("■")  # Wall tile

                    if tile_id == 2:

                        move_cursor(row, col)
                        self.blocks[(row, col)] = 1
                        print("▦")  # Block tile

                    if tile_id == 3:
                        # Remove old paddle:
                        last_pad_col = self.pad_loc[0]
                        last_pad_row = self.pad_loc[1]
                        move_cursor(last_pad_row, last_pad_col)
                        print(" ")
                        self.pad_loc = [col, row]

                        # Show new cursor location:
                        move_cursor(row, col)
                        print("▬")  # Paddle

                    if tile_id == 4:
                        # Remove old ball:
                        last_ball_col = self.ball_loc[0]
                        last_ball_row = self.ball_loc[1]
                        move_cursor(last_ball_row, last_ball_col)
                        print(" ")

                        self.ball_loc = [col, row]

                        # Print new one:
                        move_cursor(row, col)
                        print("●")  # Ball

                        # If ball "hits" a block, remove block (Visually that is:
                        # Collision logic is handeled by the intcode program)

                        # Hits Top:
                        if (row - 1, col) in self.blocks:
                            move_cursor(row - 1, col)
                            print(" ")
                            del self.blocks[(row - 1, col)]

                        # Hits left side
                        if (row, col + 1) in self.blocks:
                            move_cursor(row, col + 1)
                            print(" ")
                            del self.blocks[(row, col + 1)]

                        # Hits right side
                        if (row, col - 1) in self.blocks:
                            move_cursor(row, col - 1)
                            print(" ")
                            del self.blocks[(row, col - 1)]

                        # Hits bottom:
                        if (row + 1, col) in self.blocks:
                            move_cursor(row + 1, col)
                            print(" ")
                            del self.blocks[(row + 1, col)]

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


get_data = lambda path: [
    int(n.rstrip()) for n in open(path).readline().split(",") if len(n) > 0
]

# data =get_data("d13_test_input.txt")
data = get_data("d13_input.txt")

if os.name == "nt":
    os.system("cls")
    os.system("cls")

Computer(data).compute()
