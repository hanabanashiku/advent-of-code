#                                         --- Day 1: Calorie Counting ---
# The jungle must be too overgrown and difficult to navigate in vehicles or access from the air; the Elves'
# expedition traditionally goes on foot. As your boats approach land, the Elves begin taking inventory of their
# supplies. One important consideration is food - in particular, the number of Calories each Elf is carrying (your
# puzzle input).
#
# The Elves take turns writing down the number of Calories contained by the various meals, snacks, rations,
# etc. that they've brought with them, one item per line. Each Elf separates their own inventory from the previous
# Elf's inventory (if any) by a blank line.

def parse_into_elves():
    input_file = open("input.txt", "r")
    elves = []

    lines = input_file.readlines()
    i = 0

    for line in lines:
        if line == "\n":
            i += 1
            continue

        if i not in elves:
            elves.append([])

        elves[i].append(int(line))

    return elves


# In case the Elves get hungry and need extra snacks, they need to know which Elf to ask: they'd like to know how
# many Calories are being carried by the Elf carrying the most Calories.
#
# Find the Elf carrying the most Calories. How many total Calories is that Elf carrying?
def calculate_max_calories():
    elves = parse_into_elves()
    elf = max(elves, key=sum)
    return sum(elf)


# By the time you calculate the answer to the Elves' question, they've already realized that the Elf carrying the
# most Calories of food might eventually run out of snacks.
#
# To avoid this unacceptable situation, the Elves would instead like to know the total Calories carried by the top
# three Elves carrying the most Calories. That way, even if one of those Elves runs out of snacks, they still have
# two backups.
#
# Find the top three Elves carrying the most Calories. How many Calories are those Elves carrying in total?
def calculate_top_three():
    elves = parse_into_elves()
    sorted_list = sorted(elves, key=sum, reverse=True)
    return sum([item for sublist in sorted_list[:3] for item in sublist])


print(calculate_max_calories())
print(calculate_top_three())

