from utils.interval import add_interval, subtract_interval, union, normalize, size, split, intersects, contains


# --- normalize ---


class TestNormalize:
    def test_empty(self):
        assert normalize([]) == []

    def test_single(self):
        assert normalize([(1, 5)]) == [(1, 5)]

    def test_already_normalized(self):
        assert normalize([(1, 3), (5, 7)]) == [(1, 3), (5, 7)]

    def test_unsorted(self):
        assert normalize([(5, 7), (1, 3)]) == [(1, 3), (5, 7)]

    def test_overlapping(self):
        assert normalize([(1, 5), (3, 7)]) == [(1, 7)]

    def test_adjacent(self):
        # [1,3) and [3,5) touch at 3 -> merged
        assert normalize([(1, 3), (3, 5)]) == [(1, 5)]

    def test_contained(self):
        assert normalize([(1, 10), (3, 5)]) == [(1, 10)]

    def test_multiple_overlapping(self):
        assert normalize([(1, 3), (2, 5), (4, 8)]) == [(1, 8)]

    def test_mixed(self):
        assert normalize([(10, 20), (1, 3), (5, 7), (2, 6)]) == [(1, 7), (10, 20)]

    def test_mutates_input(self):
        lst = [(5, 7), (1, 3)]
        result = normalize(lst)
        assert result is lst
        assert lst == [(1, 3), (5, 7)]


# --- subtract_interval ---


class TestSubtractInterval:
    def test_empty_list(self):
        assert subtract_interval([], (1, 5)) == []

    def test_no_overlap_before(self):
        assert subtract_interval([(1, 3)], (5, 7)) == [(1, 3)]

    def test_no_overlap_after(self):
        assert subtract_interval([(5, 7)], (1, 3)) == [(5, 7)]

    def test_adjacent_at_end(self):
        # [1,3) and remove [3,5) — no overlap in half-open
        assert subtract_interval([(1, 3)], (3, 5)) == [(1, 3)]

    def test_adjacent_at_start(self):
        # [3,5) and remove [1,3) — no overlap in half-open
        assert subtract_interval([(3, 5)], (1, 3)) == [(3, 5)]

    def test_remove_exact(self):
        assert subtract_interval([(1, 5)], (1, 5)) == []

    def test_remove_containing(self):
        # Remove larger than interval
        assert subtract_interval([(2, 4)], (1, 5)) == []

    def test_remove_left_overlap(self):
        assert subtract_interval([(1, 5)], (0, 3)) == [(3, 5)]

    def test_remove_right_overlap(self):
        assert subtract_interval([(1, 5)], (3, 7)) == [(1, 3)]

    def test_remove_middle_splits(self):
        assert subtract_interval([(1, 10)], (3, 7)) == [(1, 3), (7, 10)]

    def test_remove_from_start(self):
        assert subtract_interval([(1, 10)], (1, 5)) == [(5, 10)]

    def test_remove_from_end(self):
        assert subtract_interval([(1, 10)], (5, 10)) == [(1, 5)]

    def test_remove_spanning_multiple(self):
        assert subtract_interval([(1, 3), (5, 7), (9, 11)], (2, 10)) == [(1, 2), (10, 11)]

    def test_remove_covering_all(self):
        assert subtract_interval([(1, 3), (5, 7)], (0, 10)) == []

    def test_remove_between_intervals(self):
        # Remove in the gap — nothing changes
        assert subtract_interval([(1, 3), (7, 9)], (4, 6)) == [(1, 3), (7, 9)]

    def test_remove_one_of_multiple(self):
        assert subtract_interval([(1, 3), (5, 7), (9, 11)], (5, 7)) == [(1, 3), (9, 11)]

    def test_remove_partial_multiple(self):
        assert subtract_interval([(1, 5), (8, 12)], (3, 10)) == [(1, 3), (10, 12)]

    def test_mutates_input(self):
        lst = [(1, 10)]
        result = subtract_interval(lst, (3, 7))
        assert result is lst
        assert lst == [(1, 3), (7, 10)]

    def test_single_point_removal(self):
        # Remove [5,6) from [1,10) — removes just point 5
        assert subtract_interval([(1, 10)], (5, 6)) == [(1, 5), (6, 10)]


# --- add_interval ---


class TestAddInterval:
    def test_add_to_empty(self):
        assert add_interval([], (1, 5)) == [(1, 5)]

    def test_add_non_overlapping(self):
        assert add_interval([(1, 3)], (5, 7)) == [(1, 3), (5, 7)]

    def test_add_overlapping(self):
        assert add_interval([(1, 5)], (3, 7)) == [(1, 7)]

    def test_add_before(self):
        assert add_interval([(5, 7)], (1, 3)) == [(1, 3), (5, 7)]

    def test_add_bridging(self):
        assert add_interval([(1, 3), (7, 9)], (2, 8)) == [(1, 9)]


# --- union ---


class TestUnion:
    def test_both_empty(self):
        assert union([], []) == []

    def test_first_empty(self):
        assert union([], [(1, 3)]) == [(1, 3)]

    def test_second_empty(self):
        assert union([(1, 3)], []) == [(1, 3)]

    def test_non_overlapping_ordered(self):
        assert union([(1, 3)], [(5, 7)]) == [(1, 3), (5, 7)]

    def test_non_overlapping_reversed(self):
        assert union([(5, 7)], [(1, 3)]) == [(1, 3), (5, 7)]

    def test_overlapping(self):
        assert union([(1, 5)], [(3, 7)]) == [(1, 7)]

    def test_adjacent(self):
        assert union([(1, 3)], [(3, 5)]) == [(1, 5)]

    def test_interleaved(self):
        assert union([(1, 3), (5, 7)], [(2, 4), (6, 8)]) == [(1, 4), (5, 8)]

    def test_one_contains_other(self):
        assert union([(1, 10)], [(3, 5)]) == [(1, 10)]

    def test_multiple_merges(self):
        assert union([(1, 3), (5, 7), (9, 11)], [(2, 10)]) == [(1, 11)]


# --- size ---


class TestSize:
    def test_empty(self):
        assert size([]) == 0

    def test_single(self):
        assert size([(1, 5)]) == 4

    def test_multiple(self):
        assert size([(1, 3), (5, 8)]) == 5

    def test_unit(self):
        assert size([(0, 1)]) == 1


# --- split ---


class TestSplit:
    def test_empty(self):
        assert split([], 5) == ([], [])

    def test_point_before_all(self):
        assert split([(3, 7)], 1) == ([], [(3, 7)])

    def test_point_after_all(self):
        assert split([(3, 7)], 10) == ([(3, 7)], [])

    def test_point_at_end(self):
        assert split([(3, 7)], 7) == ([(3, 7)], [])

    def test_point_between_intervals(self):
        assert split([(1, 3), (5, 7)], 4) == ([(1, 3)], [(5, 7)])

    def test_point_at_interval_boundary(self):
        assert split([(1, 3), (5, 7)], 5) == ([(1, 3)], [(5, 7)])

    def test_point_inside_interval(self):
        left, right = split([(1, 10)], 5)
        assert left == [(1, 5)]
        assert right == [(5, 10)]

    def test_split_second_interval(self):
        left, right = split([(1, 3), (5, 10)], 7)
        assert left == [(1, 3), (5, 7)]
        assert right == [(7, 10)]

    def test_split_preserves_sizes(self):
        intervals = [(0, 10), (20, 30)]
        left, right = split(intervals, 25)
        assert size(left) + size(right) == size(intervals)


# --- intersects ---


class TestIntersects:
    def test_no_overlap(self):
        assert intersects([(1, 3)], [(5, 7)]) is False

    def test_adjacent_no_overlap(self):
        # [1,3) and [3,5) share no points in half-open representation
        assert intersects([(1, 3)], [(3, 5)]) is False

    def test_overlap(self):
        assert intersects([(1, 5)], [(3, 7)]) is True

    def test_contained(self):
        assert intersects([(1, 10)], [(3, 5)]) is True

    def test_both_empty(self):
        assert intersects([], []) is False

    def test_one_empty(self):
        assert intersects([(1, 3)], []) is False

    def test_multiple_no_overlap(self):
        assert intersects([(1, 3), (5, 7)], [(3, 5), (7, 9)]) is False

    def test_multiple_with_overlap(self):
        assert intersects([(1, 3), (5, 7)], [(4, 6)]) is True


# --- contains ---


class TestContains:
    def test_empty(self):
        assert contains([], 5) is False

    def test_point_inside(self):
        assert contains([(1, 5)], 3) is True

    def test_point_at_start(self):
        assert contains([(1, 5)], 1) is True

    def test_point_at_end_exclusive(self):
        assert contains([(1, 5)], 5) is False

    def test_point_before(self):
        assert contains([(3, 7)], 1) is False

    def test_point_after(self):
        assert contains([(3, 7)], 10) is False

    def test_point_in_gap(self):
        assert contains([(1, 3), (5, 7)], 4) is False

    def test_point_in_second_interval(self):
        assert contains([(1, 3), (5, 7)], 6) is True
