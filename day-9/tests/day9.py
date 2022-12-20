import unittest
from mock import patch
from ..day9 import valid_tail_pos, move_head, count_tail_positions


class Day9Tests(unittest.TestCase):
    @staticmethod
    def parse_movements():
        input_file = open('../example.txt', 'r')
        return [(line[0], int(line[2])) for line in input_file.readlines()]

    def test_valid_tail_pos(self):
        self.assertTrue(valid_tail_pos((2, 1), (1, 1)))
        self.assertFalse(valid_tail_pos((1, 1), (3, 1)))
        self.assertTrue(valid_tail_pos((1, 2), (1, 1)))
        self.assertFalse(valid_tail_pos((1, 3), (1, 1)))
        self.assertTrue(valid_tail_pos((2, 2), (1, 3)))
        self.assertFalse(valid_tail_pos((2, 1), (1, 3)))
        self.assertFalse(valid_tail_pos((3, 2), (1, 3)))

    def test_move_head(self):
        self.assertEqual(
            [(3, 1), (2, 1), {(1, 1), (2, 1)}],
            move_head((2, 1), (1, 1), ['R', 1])
        )

        self.assertEqual(
            [(1, 3), (1, 2), {(1, 1), (1, 2)}],
            move_head((1, 2), (1, 1), ['D', 1])
        )

        self.assertEqual(
            [(2, 1), (2, 2), {(1, 3), (2, 2)}],
            move_head((2, 2), (1, 3), ['U', 1]),
        )

        self.assertEqual(
            [(3, 2), (2, 2), {(1, 3), (2, 2)}],
            move_head((2, 2), (1, 3), ['R', 1])
        )


if __name__ == '__main__':
    unittest.main()
