import unittest

import maze_work
import maze_draw


TEST_SOLVE = [
    ["test_1.txt", [(0, 0), (3, 3)], [0, 1, 2, 3, 7, 11, 15]],
    ["test_1.txt", [(0, 0), (0, 1)], [0, 1, 5, 4]],
    ["test_1.txt", [(0, 0) ,(0, 3)], [0, 1, 5, 9, 8, 12]],
    ["test_1.txt", [(2, 2), (2, 3)], [10, 6 , 2, 3, 7, 11, 15, 14]],
    ["test_1.txt", [(3, 3), (0, 0)], [15 ,11, 7, 3, 2, 1, 0]]
]

class TestMazeWork(unittest.TestCase):
    """Тест-кейс модуля maze_work."""


    def test_solve(self) -> None:
        """Тест функции best_first_search."""
        for data in TEST_SOLVE:
            with open(data[0], 'r') as input_text_f:
                maze = maze_draw.text_file_to_maze(input_text_f)
            path, _ = maze_work.best_first_search(maze, data[1][0], data[1][1])
            self.assertEqual(path, data[2])

