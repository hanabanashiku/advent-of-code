import re


#                                          --- Day 5: Supply Stacks ---
# The expedition can depart as soon as the final supplies have been unloaded from the
# ships. Supplies are stored in stacks of marked crates, but because the needed supplies are buried under many other
# crates, the crates need to be rearranged.
#
# The ship has a giant cargo crane capable of moving crates between stacks. To ensure none of the crates get crushed
# or fall over, the crane operator will rearrange them in a series of carefully-planned steps. After the crates are
# rearranged, the desired crates will be at the top of each stack.
#
# The Elves don't want to interrupt the crane operator during this delicate procedure, but they forgot to ask her
# which crate will end up where, and they want to be ready to unload them as soon as possible so they can embark.
#
# They do, however, have a drawing of the starting stacks of crates and the rearrangement procedure (your puzzle input).
# Then, the rearrangement procedure is given. In each step of the procedure, a quantity of crates is moved from one
# stack to a different stack.
def strip_spaces(line):
    list_str = list(line.removesuffix('\n'))
    del list_str[3::4]
    result = ''.join(list_str)
    result = re.sub(r'\s{3}', ' ', result)
    result = re.sub(r'[\[\]]', '', result)
    return result


def get_initial_config():
    input_file = open('input.txt', 'r')

    i = 0
    lines = input_file.readlines()
    parsed_lines = []
    while re.search(r'^((\[\w\]|\s)\s)+', lines[i]):
        line = list(strip_spaces(lines[i]))
        for j in range(len(line)):
            if len(parsed_lines) < j + 1:
                parsed_lines.append([])
            if line[j] != ' ':
                parsed_lines[j].insert(0, line[j])
        i += 1

    return parsed_lines


def parse_instructions():
    input_file = open('input.txt', 'r')
    lines = input_file.readlines()
    instructions = []

    for line in lines:
        match = re.match(r'^move (\d+) from (\d+) to (\d+)\n?$', line)
        if match is None:
            continue
        instructions.append([int(i) for i in list(match.groups())])
    return instructions


def execute_instruction(stacks, instruction):
    [amount, from_stack, to_stack] = instruction

    for i in range(amount):
        stacks[to_stack - 1].append(stacks[from_stack - 1].pop())
    return stacks


# The Elves just need to know which crate will end up on top of each stack; in this example, the top crates are C in
# stack 1, M in stack 2, and Z in stack 3, so you should combine these together and give the Elves the message CMZ.
#
# After the rearrangement procedure completes, what crate ends up on top of each stack?
def get_top_crates():
    stacks = get_initial_config()
    instructions = parse_instructions()

    for instruction in instructions:
        stacks = execute_instruction(stacks, instruction)

    tops = []
    for stack in stacks:
        tops.append(' ' if len(stack) == 0 else stack.pop())
    return tops


# As you watch the crane operator expertly rearrange the crates, you notice the process isn't following your prediction.
#
# Some mud was covering the writing on the side of the crane, and you quickly wipe it away. The crane isn't a
# CrateMover 9000 - it's a CrateMover 9001.
#
# The CrateMover 9001 is notable for many new and exciting features: air conditioning, leather seats, an extra cup
# holder, and the ability to pick up and move multiple crates at once.
#
# Before the rearrangement process finishes, update your simulation so that the Elves know where they should stand to
# be ready to unload the final supplies. After the rearrangement procedure completes, what crate ends up on top of
# each stack?
def execute_instruction_9001(stacks, instruction):
    [amount, from_stack, to_stack] = instruction

    stacks_to_move = [stacks[from_stack - 1].pop() for _ in range(amount)]
    stacks_to_move.reverse()
    stacks[to_stack - 1] = stacks[to_stack - 1] + stacks_to_move
    return stacks


def get_top_crates_9001():
    stacks = get_initial_config()
    instructions = parse_instructions()

    for instruction in instructions:
        stacks = execute_instruction_9001(stacks, instruction)

    tops = []
    for stack in stacks:
        tops.append(' ' if len(stack) == 0 else stack.pop())
    return tops


print(''.join(get_top_crates()))
print(''.join(get_top_crates_9001()))
