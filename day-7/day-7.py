#                                 --- Day 7: No Space Left On Device ---
# You can hear birds chirping and raindrops hitting leaves as the expedition
# proceeds. Occasionally, you can even hear much louder sounds in the distance; how big do the animals get out here,
# anyway?
#
# The device the Elves gave you has problems with more than just its communication system. You try to run a system
# update:
#
# $ system-update --please --pretty-please-with-sugar-on-top
# Error: No space left on device
# Perhaps you can delete some files to make space for the update?
#
# You browse around the filesystem to assess the situation and save the resulting terminal output (your puzzle input).
#
# The filesystem consists of a tree of files (plain data) and directories (which can contain other directories or
# files). The outermost directory is called /. You can navigate around the filesystem, moving into or out of
# directories and listing the contents of the directory you're currently in.
#
# Within the terminal output, lines that begin with $ are commands you executed, very much like some modern computers:
#
# cd means change directory. This changes which directory is the current directory, but the specific result depends
# on the argument: cd x moves in one level: it looks in the current directory for the directory named x and makes it
# the current directory. cd .. moves out one level: it finds the directory that contains the current directory,
# then makes that directory the current directory. cd / switches the current directory to the outermost directory,
# /. ls means list. It prints out all of the files and directories immediately contained by the current directory:
# 123 abc means that the current directory contains a file named abc with size 123. dir xyz means that the current
# directory contains a directory named xyz.
#
# Since the disk is full, your first step should probably be to find directories that are good candidates for
# deletion. To do this, you need to determine the total size of each directory. The total size of a directory is the
# sum of the sizes of the files it contains, directly or indirectly. (Directories themselves do not count as having
# any intrinsic size.)
#
# To begin, find all of the directories with a total size of at most 100000, then calculate the sum of their total
# sizes. In the example above, these directories are a and e; the sum of their total sizes is 95437 (94853 + 584). (
# As in this example, this process can count files more than once!)

SIZE_LIMIT = 100000
SYSTEM_SIZE = 70000000
REQUIRED_FREE_SPACE = 30000000


class Node:
    def __init__(self, name, size=0):
        self.name = name
        self.children = []
        self.parent = None
        self.size = size
        self.is_file = size != 0

    def add_child(self, node):
        if self.is_file:
            raise Exception("Can't add a child to a file")

        if any(child.name == node.name for child in self.children):
            return

        node.parent = self
        self.children.append(node)

    def get_child(self, name):
        return next(child for child in self.children if child.name == name)

    def get_directory_size(self):
        if self.is_file:
            return self.size

        return sum(child.get_directory_size() for child in self.children)

    def __str__(self):
        if self.name == '':
            return '/ (dir)'
        if self.is_file:
            return self.name + '(file, size=' + str(self.size) + ')'
        return self.name + ' (dir)'


def parse_file_system():
    input_file = open('input.txt', 'r')

    pwd = '/'
    parent_node = Node('')
    current_node = parent_node
    is_ls = False

    for line in input_file.readlines():
        line = line.removesuffix('\n')
        if line == '$ cd /':
            continue

        parts = line.split(' ')

        if parts[0] == '$':
            if parts[1] != 'ls':
                is_ls = False

            if parts[1] == 'cd':
                if parts[2] == '..':
                    current_node = current_node.parent
                    pwd = current_node.name
                    continue
                elif parts[2] == '/':
                    current_node = parent_node
                    pwd = '/'
                    continue

                pwd = parts[2]
                current_node = current_node.get_child(parts[2])
                continue

            elif parts[1] == 'ls':
                is_ls = True
                continue
            else:
                raise Exception('Unknown command ' + parts[1])

        else:
            if not is_ls:
                raise Exception('Unknown line')

            current_node.add_child(Node(parts[1], 0 if parts[0] == 'dir' else int(parts[0])))

    return parent_node


# Find all of the directories with a total size of at most 100000. What is the sum of the total sizes of those
# directories?
def get_total_sizes():
    file_system = parse_file_system()
    return calc_child_sizes(file_system)


def calc_child_sizes(node):
    if node.is_file:
        return 0

    current_size = 0

    for child in node.children:
        if child.is_file:
            continue

        size = child.get_directory_size()
        if size <= SIZE_LIMIT:
            current_size += size

        current_size += calc_child_sizes(child)
    return current_size


# Now, you're ready to choose a directory to delete.
#
# The total disk space available to the filesystem is 70000000. To run the update, you need unused space of at least
# 30000000. You need to find a directory you can delete that will free up enough space to run the update.
def deleted_directory_size():
    file_system = parse_file_system()
    used_space = file_system.get_directory_size()
    space_to_free = REQUIRED_FREE_SPACE - (SYSTEM_SIZE - used_space)

    return find_closest_dir(file_system, space_to_free)


def find_closest_dir(node, space_to_free):
    closest = 999999999

    if node.is_file:
        return 999999999

    size = node.get_directory_size()

    if size >= space_to_free:
        closest = size
    # don't search the tree, nothing will be big enough
    else:
        return closest

    for child in node.children:
        if child.is_file:
            continue

        closest = min(closest, find_closest_dir(child, space_to_free))
    return closest


print(get_total_sizes())
print(deleted_directory_size())
