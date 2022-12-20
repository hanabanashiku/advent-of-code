def parse_movements():
    input_file = open('input.txt', 'r')
    return [(line[0], int(line[2])) for line in input_file.readlines()]


def sign(x):
    return int(x / abs(x))


def valid_tail_pos(head_pos, tail_pos):
    (hx, hy) = head_pos
    (tx, ty) = tail_pos

    # if hx == tx and hy == ty:
    #     return True
    # if hx == tx:
    #     return abs(hy - ty) <= 1
    # if hy == ty:
    #     return abs(hx - tx) <= 1
    #
    # return abs(hx - tx) < 2 and abs(hy - ty) < 2
    return not(abs(hx - tx) > 1 or abs(hy - ty) > 1)


move_func = {
    "D": lambda head_pos: (head_pos[0], head_pos[1] + 1),
    "U": lambda head_pos: (head_pos[0], head_pos[1] - 1),
    "L": lambda head_pos: (head_pos[0] - 1, head_pos[1]),
    "R": lambda head_pos: (head_pos[0] + 1, head_pos[1])
}


def move_head(head_pos, tail_pos, move):
    [direction, amount] = move
    tail_history = {tail_pos}

    for _ in range(amount):
        last_head = head_pos
        head_pos = move_func[direction](head_pos)

        if valid_tail_pos(head_pos, tail_pos):
            continue

        tail_pos = last_head
        tail_history.add(tail_pos)

    return [head_pos, tail_pos, tail_history]


def count_tail_positions():
    tail_positions = set()
    head_pos = (0, 0)
    tail_pos = (0, 0)

    for move in parse_movements():
        [new_head, new_tail, history] = move_head(head_pos, tail_pos, move)

        head_pos = new_head
        tail_pos = new_tail
        tail_positions = tail_positions.union(history)

    return len(tail_positions)


if __name__ == '__main__':
    print(count_tail_positions())

