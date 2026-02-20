from utils.pathfinding import a_star, _reconstruct_path


class TestReconstructPath:
    def test_single_step(self):
        # 0 -> 1
        came_from = {1: 0}
        assert _reconstruct_path(came_from, 0, 1) == [0, 1]

    def test_multi_step(self):
        # 0 -> 1 -> 2 -> 3
        came_from = {1: 0, 2: 1, 3: 2}
        assert _reconstruct_path(came_from, 0, 3) == [0, 1, 2, 3]

    def test_start_equals_end(self):
        came_from = {}
        assert _reconstruct_path(came_from, 0, 0) == [0]


def _unit_cost(a, b):
    return 1


def _make_grid_neighbors(width, height):
    """Build a neighbors function for a width x height grid."""

    def neighbors_of(n):
        r, c = divmod(n, width)
        result = []
        if r > 0:
            result.append(n - width)
        if r < height - 1:
            result.append(n + width)
        if c > 0:
            result.append(n - 1)
        if c < width - 1:
            result.append(n + 1)
        return result

    return neighbors_of


def _manhattan_heuristic(goal, width):
    """Manhattan distance heuristic for a grid."""
    gr, gc = divmod(goal, width)

    def h(n):
        r, c = divmod(n, width)
        return abs(r - gr) + abs(c - gc)

    return h


class TestAStar:
    def test_start_is_goal(self):
        total_cost, path = a_star(0, 0, lambda n: [], lambda n: 0, _unit_cost)
        assert total_cost == 0
        assert path == [0]

    def test_straight_line(self):
        # 0 - 1 - 2 - 3  (linear graph)
        def neighbors_of(n):
            result = []
            if n > 0:
                result.append(n - 1)
            if n < 3:
                result.append(n + 1)
            return result

        total_cost, path = a_star(0, 3, neighbors_of, lambda n: 3 - n, _unit_cost)
        assert total_cost == 3
        assert path == [0, 1, 2, 3]

    def test_2x2_grid(self):
        # 0 1
        # 2 3
        width, height = 2, 2
        neighbors_of = _make_grid_neighbors(width, height)
        h = _manhattan_heuristic(3, width)
        total_cost, path = a_star(0, 3, neighbors_of, h, _unit_cost)
        assert total_cost == 2
        assert path[0] == 0
        assert path[-1] == 3
        assert len(path) == 3

    def test_3x3_grid_corner_to_corner(self):
        # 0 1 2
        # 3 4 5
        # 6 7 8
        width, height = 3, 3
        neighbors_of = _make_grid_neighbors(width, height)
        h = _manhattan_heuristic(8, width)
        total_cost, path = a_star(0, 8, neighbors_of, h, _unit_cost)
        assert total_cost == 4
        assert path[0] == 0
        assert path[-1] == 8
        assert len(path) == 5  # 4 steps

    def test_no_path_returns_empty(self):
        # Two disconnected nodes
        total_cost, path = a_star(0, 1, lambda n: [], lambda n: 0, _unit_cost)
        assert total_cost == float("inf")
        assert path == []

    def test_weighted_edges(self):
        # 0 --1-- 1 --1-- 2
        # |               |
        # +------10-------+
        # Cheap path: 0->1->2, expensive: 0->2
        def neighbors_of(n):
            if n == 0:
                return [1, 2]
            elif n == 1:
                return [0, 2]
            else:
                return [0, 1]

        costs = {(0, 1): 1, (1, 0): 1, (0, 2): 10, (2, 0): 10, (1, 2): 1, (2, 1): 1}
        total_cost, path = a_star(0, 2, neighbors_of, lambda n: 0, lambda a, b: costs[(a, b)])
        assert total_cost == 2
        assert path == [0, 1, 2]

    def test_avoids_high_cost_path(self):
        # 0 --1-- 1 --1-- 3
        # |               |
        # +--1-- 2 --100--+
        # Cheap: 0->1->3, expensive via 2: 0->2->3
        def neighbors_of(n):
            if n == 0:
                return [1, 2]
            elif n == 1:
                return [0, 3]
            elif n == 2:
                return [0, 3]
            else:
                return [1, 2]

        costs = {
            (0, 1): 1,
            (1, 0): 1,
            (0, 2): 1,
            (2, 0): 1,
            (1, 3): 1,
            (3, 1): 1,
            (2, 3): 100,
            (3, 2): 100,
        }
        total_cost, path = a_star(0, 3, neighbors_of, lambda n: 0, lambda a, b: costs[(a, b)])
        assert total_cost == 2
        assert path == [0, 1, 3]

    def test_reverse_direction(self):
        # 3x3 grid, bottom-right to top-left
        width, height = 3, 3
        neighbors_of = _make_grid_neighbors(width, height)
        h = _manhattan_heuristic(0, width)
        total_cost, path = a_star(8, 0, neighbors_of, h, _unit_cost)
        assert total_cost == 4
        assert path[0] == 8
        assert path[-1] == 0
        assert len(path) == 5

    def test_adjacent_nodes(self):
        # Two adjacent nodes
        def neighbors_of(n):
            if n == 0:
                return [1]
            return [0]

        total_cost, path = a_star(0, 1, neighbors_of, lambda n: 0, lambda a, b: 5)
        assert total_cost == 5
        assert path == [0, 1]
