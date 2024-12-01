#                                   --- Day 2: Rock Paper Scissors ---
# The Elves begin to set up camp on the beach. To decide whose tent gets to be
# closest to the snack storage, a giant Rock Paper Scissors tournament is already in progress.
#
# Rock Paper Scissors is a game between two players. Each game contains many rounds; in each round, the players each
# simultaneously choose one of Rock, Paper, or Scissors using a hand shape. Then, a winner for that round is
# selected: Rock defeats Scissors, Scissors defeats Paper, and Paper defeats Rock. If both players choose the same
# shape, the round instead ends in a draw.
#
# Appreciative of your help yesterday, one Elf gives you an encrypted strategy guide (your puzzle input) that they
# say will be sure to help you win. "The first column is what your opponent is going to play: A for Rock,
# B for Paper, and C for Scissors. The second column--" Suddenly, the Elf is called away to help with someone's tent.
#
# The second column, you reason, must be what you should play in response: X for Rock, Y for Paper, and Z for
# Scissors. Winning every time would be suspicious, so the responses must have been carefully chosen.

# The winner of the whole tournament is the player with the highest score. Your total score is the sum of your scores
# for each round. The score for a single round is the score for the shape you selected (1 for Rock, 2 for Paper,
# and 3 for Scissors) plus the score for the outcome of the round (0 if you lost, 3 if the round was a draw,
# and 6 if you won).

OPPONENT = 0
PLAYER = 1
DECODED = 2
ROCK = ['A', 'X', 0]
PAPER = ['B', 'Y', 1]
SCISSORS = ['C', 'Z', 2]

WIN_VALUE = 6
DRAW_VALUE = 3
LOSE_VALUE = 0


def parse_moves():
    input_file = open("input.txt", "r")
    lines = input_file.readlines()

    return [line.removesuffix('\n').split(' ') for line in lines]


def decode_move(move, is_player):
    idx = PLAYER if is_player else OPPONENT
    return [ROCK[idx], PAPER[idx], SCISSORS[idx]].index(move)


def encode_move(move, is_player):
    idx = PLAYER if is_player else OPPONENT
    return [ROCK[idx], PAPER[idx], SCISSORS[idx]][move]


def shape_score(move):
    return ord(move) - ord(ROCK[PLAYER]) + 1


def score_for_round(player, opponent):
    shape = shape_score(player)
    player_move = decode_move(player, True)
    opponent_move = decode_move(opponent, False)

    if player_move == opponent_move:
        game_score = DRAW_VALUE
    elif player_move == ROCK[DECODED]:
        game_score = WIN_VALUE if opponent_move == SCISSORS[DECODED] else LOSE_VALUE
    elif player_move == PAPER[DECODED]:
        game_score = WIN_VALUE if opponent_move == ROCK[DECODED] else LOSE_VALUE
    elif player_move == SCISSORS[DECODED]:
        game_score = WIN_VALUE if opponent_move == PAPER[DECODED] else LOSE_VALUE
    else:
        raise Exception("bad player move")

    return shape + game_score


# Since you can't be sure if the Elf is trying to help you or trick you, you should calculate the score you would get
# if you were to follow the strategy guide.
#
# What would your total score be if everything goes exactly according to your strategy guide?
def calculate_projected_score(array):
    return sum([score_for_round(player, opponent) for [opponent, player] in array])


# The Elf finishes helping with the tent and sneaks back over to you. "Anyway, the second column says how the round
# needs to end: X means you need to lose, Y means you need to end the round in a draw, and Z means you need to win.
# Good luck!"
#
# Following the Elf's instructions for the second column, what would your total score be if everything goes exactly
# according to your strategy guide?

LOSE = 'X'
DRAW = 'Y'
WIN = 'Z'


def calculate_final_score(moves):
    # Going to translate into the key we THOUGHT we had
    for move in moves:
        [opponent, result] = move
        if result == DRAW:
            move[1] = encode_move(decode_move(opponent, False), True)
        elif result == WIN:
            for m in [0, 1, 2]:
                encoded_move = encode_move(m, True)
                if score_for_round(encoded_move, opponent) - shape_score(encoded_move) == WIN_VALUE:
                    move[1] = encoded_move
                    break
        elif result == LOSE:
            for m in [0, 1, 2]:
                encoded_move = encode_move(m, True)
                if score_for_round(encoded_move, opponent) - shape_score(encoded_move) == LOSE_VALUE:
                    move[1] = encoded_move
                    break
        else:
            raise Exception("Bad match result " + result)

    return calculate_projected_score(moves)


print(calculate_projected_score(parse_moves()))
print(calculate_final_score(parse_moves()))
