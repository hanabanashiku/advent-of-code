import re

# As you finally start making your way upriver, you realize your pack is much lighter than you remember. Just then,
# one of the items from your pack goes flying overhead. Monkeys are playing Keep Away with your missing things!
#
# To get your stuff back, you need to be able to predict where the monkeys will throw your items. After some careful
# observation, you realize the monkeys operate based on how worried you are about each item.
#
# You take some notes (your puzzle input) on the items each monkey currently has, how worried you are about those
# items, and how the monkey makes decisions based on your worry level.
#
# Chasing all of the monkeys at once is impossible; you're going to have to focus on the two most active monkeys if
# you want any hope of getting your stuff back. Count the total number of times each monkey inspects items over 20
# rounds
#
# Figure out which monkeys to chase by counting how many items they inspect over 20 rounds. What is the level of
# monkey business after 20 rounds of stuff-slinging simian shenanigans?


def parse_monkeys():
    input_file = open('input.txt', 'r').read()
    return [Monkey(m) for m in input_file.split('\n\n')]


class Monkey:
    items = []
    inspection_count = 0

    def __init__(self, string):
        lines = string.split('\n')
        self.id = int(re.match(r'Monkey (\d+):', lines[0])[1])

        items = re.findall(r'(\d+)', lines[1])
        self.items = [int(item) for item in items]

        op_match = re.match(r'Operation:new=old([+\-*/])(old|\d+)', lines[2].replace(' ', ''))
        self.operation = [op_match[1], op_match[2]]

        divisible_by = int(re.match(r'Test:divisibleby(\d+)', lines[3].replace(' ', ''))[1])
        true_monkey = int(re.match(r'Iftrue:throwtomonkey(\d+)', lines[4].replace(' ', ''))[1])
        false_monkey = int(re.match(r'Iffalse:throwtomonkey(\d+)', lines[5].replace(' ', ''))[1])

        self.test = {
            "divisible_by": divisible_by,
            "result": {
                True: true_monkey,
                False: false_monkey
            }
        }
        self.pointer = 0

    def take_round(self, monkeys, no_relief_mode):
        self.items = self.items[self.pointer:]
        self.pointer = 0

        for i in range(len(self.items)):
            item = self.items[i]
            item = self.inspect_item(item, no_relief_mode)
            self.throw_to_monkey(item, monkeys)
            self.pointer += 1

    def inspect_item(self, old, no_relief_mode):
        self.inspection_count += 1
        x = old if self.operation[1] == 'old' else int(self.operation[1])
        op = self.operation[0]

        if op == '+':
            inspected = old + x
        elif op == '*':
            inspected = old * x
        elif op == '-':
            inspected = old - x
        elif op == '/':
            inspected = old / x
        else:
            raise Exception()

        return int(inspected / 3) if not no_relief_mode else inspected

    def throw_to_monkey(self, item, monkeys):
        # self.items = self.items[1:]
        monkeys[self.test["result"][item % self.test["divisible_by"] == 0]].catch(item)

    def catch(self, item):
        self.items.append(item)


def calculate_monkey_business(no_relief_mode=False):
    monkeys = parse_monkeys()

    for i in range(20 if not no_relief_mode else 10000):
        if no_relief_mode:
            print(i)
        for monkey in monkeys:
            monkey.take_round(monkeys, no_relief_mode)

    sorted_monkeys = sorted(monkeys, key=lambda monke: -monke.inspection_count)

    return sorted_monkeys[0].inspection_count * sorted_monkeys[1].inspection_count


# You're worried you might not ever get your items back. So worried, in fact, that your relief that a monkey's
# inspection didn't damage an item no longer causes your worry level to be divided by three.
#
# Unfortunately, that relief was all that was keeping your worry levels from reaching ridiculous levels. You'll need
# to find another way to keep your worry levels manageable.
#
# At this rate, you might be putting up with these monkeys for a very long time - possibly 10000 rounds!
#
# With these new rules, you can still figure out the monkey business after 10000 rounds.

# print(calculate_monkey_business())
print(calculate_monkey_business(True))
