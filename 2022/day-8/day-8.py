import math


#
#                                        --- Day 8: Treetop Tree House ---
# The expedition comes across a peculiar patch of tall trees all planted carefully
# in a grid. The Elves explain that a previous expedition planted these trees as a reforestation effort. Now,
# they're curious if this would be a good location for a tree house.
#
# First, determine whether there is enough tree cover here to keep a tree house hidden. To do this, you need to count
# the number of trees that are visible from outside the grid when looking directly along a row or column.
#
# Each tree is represented as a single digit whose value is its height, where 0 is the shortest and 9 is the tallest.
#
# A tree is visible if all of the other trees between it and an edge of the grid are shorter than it. Only consider
# trees in the same row or column; that is, only look up, down, left, or right from any given tree.
#
# All of the trees around the edge of the grid are visible - since they are already on the edge, there are no trees
# to block the view.
def parse_map():
    input_file = open('input.txt', 'r')

    return [[int(tree)
             for tree in list(line.removesuffix('\n'))]
            for line in input_file.readlines()]


def get_dimensions(tree_map):
    return [len(tree_map[0]), len(tree_map)]


def get_cardinal_trees(tree_map, a, b):
    dim = get_dimensions(tree_map)
    up = [tree_map[i][b] for i in range(a-1, -1, -1)]
    down = [tree_map[i][b] for i in range(a + 1, dim[0])]
    left = [tree_map[a][i] for i in range(b-1, -1, -1)]
    right = [tree_map[a][i] for i in range(b + 1, dim[1])]

    return [up, down, left, right]


def is_tree_visible(tree_map, a, b):
    dim = get_dimensions(tree_map)

    if a in [0, dim[0] - 1] or b in [0, dim[1] - 1]:
        return True

    tree = tree_map[a][b]

    for search_area in get_cardinal_trees(tree_map, a, b):
        if all([t < tree for t in search_area]):
            return True
    return False


# Consider your map; how many trees are visible from outside the grid?
def count_visible_trees():
    tree_map = parse_map()
    dim = get_dimensions(tree_map)
    count = 0

    for i in range(dim[0]):
        for j in range(dim[1]):
            if is_tree_visible(tree_map, i, j):
                count += 1
    return count


# Content with the amount of tree cover available, the Elves just need to know the best spot to build their tree
# house: they would like to be able to see a lot of trees.
#
# To measure the viewing distance from a given tree, look up, down, left, and right from that tree; stop if you reach
# an edge or at the first tree that is the same height or taller than the tree under consideration. (If a tree is
# right on the edge, at least one of its viewing distances will be zero.)
#
# The Elves don't care about distant trees taller than those found by the rules above; the proposed tree house has
# large eaves to keep it dry, so they wouldn't be able to see higher than the tree house anyway.
# A tree's scenic score is found by multiplying together its viewing distance in each of the four directions.
#
# Consider each tree on your map. What is the highest scenic score possible for any tree?
def get_viewing_distance(tree_list, tree):
    count = 0

    for t in tree_list:
        count += 1

        if t >= tree:
            break
    return count


def calc_scenic_score(tree_map, a, b):
    tree = tree_map[a][b]
    directions = get_cardinal_trees(tree_map, a, b)
    distances = [get_viewing_distance(direction, tree) for direction in directions]
    return math.prod(distances)


def get_highest_score():
    tree_map = parse_map()
    dim = get_dimensions(tree_map)

    result = 0
    for i in range(dim[0]):
        for j in range(dim[1]):
            result = max(result, calc_scenic_score(tree_map, i, j))
    return result


print(count_visible_trees())
print(get_highest_score())
