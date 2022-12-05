#                                   --- Day 4: Camp Cleanup ---
# Space needs to be cleared before the last supplies can be unloaded from the ships,
# and so several Elves have been assigned the job of cleaning up sections of the camp. Every section has a unique ID
# number, and each Elf is assigned a range of section IDs.
#
# However, as some of the Elves compare their section assignments with each other, they've noticed that many of the
# assignments overlap. To try to quickly find overlaps and reduce duplicated effort, the Elves pair up and make a big
# list of the section assignments for each pair (your puzzle input).
def get_section_assignments():
    input_file = open('input.txt', 'r')
    results = []

    for pair in [assignment.removesuffix('\n').split(',') for assignment in input_file.readlines()]:
        final_pair = []
        for elf in pair:
            [begin, end] = [int(sect) for sect in elf.split('-')]
            final_pair.append([*range(begin, end + 1)])
        results.append(final_pair)

    return results


# Some of the pairs have noticed that one of their assignments fully contains the other. For example,
# 2-8 fully contains 3-7, and 6-6 is fully contained by 4-6. In pairs where one assignment fully contains the other,
# one Elf in the pair would be exclusively cleaning sections their partner will already be cleaning, so these seem
# like the most in need of reconsideration. In this example, there are 2 such pairs.
#
# In how many assignment pairs does one range fully contain the other?
def find_redundant_pairs():
    assignments_per_group = get_section_assignments()
    redundant_counter = 0

    for pair in assignments_per_group:
        [first, second] = [set(elf) for elf in pair]
        if first.issubset(second) or second.issubset(first):
            redundant_counter += 1

    return redundant_counter


# It seems like there is still quite a bit of duplicate work planned. Instead, the Elves would like to know the
# number of pairs that overlap at all.
#
# In how many assignment pairs do the ranges overlap?
def find_overlapping_pairs():
    assignments_per_group = get_section_assignments()
    overlap_counter = 0

    for pair in assignments_per_group:
        [first, second] = [set(elf) for elf in pair]
        if first.intersection(second) != set():
            overlap_counter += 1

    return overlap_counter


print(find_redundant_pairs())
print(find_overlapping_pairs())
