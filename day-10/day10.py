# --- Day 10: Cathode-Ray Tube ---
# You avoid the ropes, plunge into the river, and swim to shore.
#
# The Elves yell something about meeting back up with them upriver, but the river is too loud to tell exactly what
# they're saying. They finish crossing the bridge and disappear from view.
#
# Situations like this must be why the Elves prioritized getting the communication system on your handheld device
# working. You pull it out of your pack, but the amount of water slowly draining from a big crack in its screen tells
# you it probably won't be of much immediate use.
#
# Unless, that is, you can design a replacement for the device's video system! It seems to be some kind of
# cathode-ray tube screen and simple CPU that are both driven by a precise clock circuit. The clock circuit ticks at
# a constant rate; each tick is called a cycle.
#
# Start by figuring out the signal being sent by the CPU. The CPU has a single register, X, which starts with the
# value 1. It supports only two instructions:
#
# - addx V takes two cycles to complete. After two cycles, the X register is increased by the value V. (V can be
# negative.)
# - noop takes one cycle to complete. It has no other effect. The CPU uses these instructions in a program (
# your puzzle input) to, somehow, tell the screen what to draw.
def parse_code():
    input_file = open('./input.txt', 'r')

    result = []
    for line in input_file.readlines():
        ins = line.removesuffix('\n').split(' ')
        if len(ins) > 1:
            ins[1] = int(ins[1])
        result.append(ins)
    result.reverse()
    return result


class CPU:
    X = 1
    CLK = 1
    program = []
    instruction = None
    instruction_cycles = 0

    def is_executing(self):
        return self.instruction is not None

    def load_program(self, ins):
        self.program = ins
        instruction = self.program.pop()
        self.set_instruction(instruction)

    def addX(self, args):
        self.X += int(args[0])

    def noop(self, args):
        return

    def set_instruction(self, instruction):
        self.instruction = instruction
        self.instruction_cycles = self.instructions[instruction[0]][1]

    def move_clock(self):
        self.CLK += 1
        self.instruction_cycles -= 1

        if self.instruction_cycles == 0:
            self.execute(self.instruction)

            if len(self.program) == 0:
                self.instruction = None
                return
            new_instruction = self.program.pop()
            self.set_instruction(new_instruction)

    def execute(self, instruction):
        self.instructions[instruction[0]][0](self, instruction[1:])

    instructions = {
        'addx': (addX, 2),
        'noop': (noop, 1)
    }


def get_interesting_signals():
    instructions = parse_code()
    cpu = CPU()
    signals = []

    cpu.load_program(instructions)

    while cpu.is_executing():
        if (cpu.CLK - 20) % 40 == 0:
            signals.append(cpu.X * cpu.CLK)

        cpu.move_clock()

    return sum(signals)


# It seems like the X register controls the horizontal position of a sprite. Specifically, the sprite is 3 pixels
# wide, and the X register sets the horizontal position of the middle of that sprite. (In this system, there is no
# such thing as "vertical position": if the sprite's horizontal position puts its pixels where the CRT is currently
# drawing, then those pixels will be drawn.)
#
# You count the pixels on the CRT: 40 wide and 6 high. This CRT screen draws the top row of pixels left-to-right,
# then the row below that, and so on. The left-most pixel in each row is in position 0, and the right-most pixel in
# each row is in position 39.
#
# Like the CPU, the CRT is tied closely to the clock circuit: the CRT draws a single pixel during each cycle.
# Representing each pixel of the screen as a #, here are the cycles during which the first and last pixel in each row
# are drawn:
#
# So, by carefully timing the CPU instructions and the CRT drawing operations, you should be able to
# determine whether the sprite is visible the instant each pixel is drawn. If the sprite is positioned such that one
# of its three pixels is the pixel currently being drawn, the screen produces a lit pixel (#); otherwise, the screen
# leaves the pixel dark (.).

def draw(screen, x, y, clk):
    rendering = current_pixel(clk)

    # print('x', str(x))
    # print('y', str(y))
    # print('clk', str(clk))
    # print('px', str(rendering))

    screen[rendering[1]][rendering[0]] = '.' if y != rendering[1] or not rendering[0] in [x - 1, x, x + 1] else '#'

    # print(''.join(screen[rendering[1]]) + '\n')
    return screen


def render(screen):
    for line in screen:
        print("".join(line))


def current_pixel(clk):
    return int((clk - 1) % 40), int((clk - 1) / 40)


def print_screen():
    instructions = parse_code()
    cpu = CPU()
    image = [['' for _ in range(40)] for _ in range(6)]

    cpu.load_program(instructions)

    while True:
        line = int((cpu.CLK - 1) / 40)

        image = draw(image, cpu.X, line, cpu.CLK)
        cpu.move_clock()

        if not cpu.is_executing():
            break

    render(image)


print(get_interesting_signals())
print_screen()
