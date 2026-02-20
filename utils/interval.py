"""Interval math utilities.

This module provides small helpers for working with **integer intervals** represented as
a list of 2-tuples.

Representation
--------------

- An **interval** is a 2-tuple ``(start, end)``.
- Intervals are **half-open**: ``[start, end)`` (inclusive start, exclusive end).
    For integer coordinates, this covers points ``{start, start+1, ..., end-1}``.
- ``start`` and ``end`` are integers and should satisfy ``start < end`` for a
    non-empty interval.

Interval lists
--------------

Many functions operate on an *interval list* which is ``list[tuple[int, int]]``.

Some functions require a *normalized* interval list. A normalized list has:

- Sorted order by ``start`` (ascending).
- No overlapping intervals.
"""

from __future__ import annotations


Interval = tuple[int, int]


def add_interval(intervals: list[Interval], add: Interval) -> list[Interval]:
    """Add an interval to a normalized interval list.

    The input list is expected to be normalized. The result is also normalized.

    Args:
        intervals: A normalized interval list. This list is *mutated*.
        add: Half-open interval ``(start, end)`` representing ``[start, end)``.

    Returns:
        The mutated list of intervals, including the new interval.
    """
    intervals.append(add)
    return normalize(intervals)


def subtract_interval(intervals: list[Interval], remove: Interval) -> list[Interval]:
    """Subtract an interval from a normalized interval list.

    The input list is expected to be normalized. The result is also normalized.

    Args:
        intervals: A normalized interval list. This list is *mutated*.
        remove: Half-open interval ``(start, end)`` representing ``[start, end)``.

    Returns:
        The mutated interval list, excluding the removed interval.
    """
    new_intervals: list[Interval] = []
    remove_start, remove_end = remove
    for start, end in intervals:
        if end <= remove_start or start >= remove_end:
            # No overlap
            new_intervals.append((start, end))
        else:
            # Overlap exists, split if necessary
            if start < remove_start:
                new_intervals.append((start, remove_start))
            if end > remove_end:
                new_intervals.append((remove_end, end))
    intervals[:] = new_intervals
    return intervals


def union(list1: list[Interval], list2: list[Interval]) -> list[Interval]:
    """Returns the union of two normalized interval lists.

    Both inputs are expected to be normalized. The result is also normalized.

    Args:
        list1: First normalized interval list.
        list2: Second normalized interval list.

    Returns:
        A new normalized interval list containing the union of the intervals.
    """

    if len(list1) == 0:
        return list2
    if len(list2) == 0:
        return list1

    i1 = 0
    i2 = 0

    # Start the merged list with the lowest interval of either list
    if list1[i1][0] < list2[i2][0]:
        merged = [list1[i1]]
        i1 += 1
    else:
        merged = [list2[i2]]
        i2 += 1

    while i1 < len(list1) and i2 < len(list2):
        if list1[i1][0] < list2[i2][0]:
            current = list1[i1]
            i1 += 1
        else:
            current = list2[i2]
            i2 += 1

        last_start, last_end = merged[-1]
        if current[0] <= last_end:
            # The intervals overlap, so merge them.
            merged[-1] = (last_start, max(last_end, current[1]))
        else:
            # The intervals do not overlap, so add the current interval to the merged list.
            merged.append(current)

    # Append any remaining intervals from either list. (only one of these will actually add intervals)
    if i1 < len(list1):
        merged.extend(list1[i1:])
        normalize(merged)
    if i2 < len(list2):
        merged.extend(list2[i2:])
        normalize(merged)

    return merged


def normalize(intervals: list[Interval]) -> list[Interval]:
    """Normalize an interval list by sorting and merging overlaps.

    This function modifies the input list in-place. If you need to preserve the original order/list, pass a copy.

    Args:
        intervals: A list of half-open intervals.

    Returns:
        The mutated list of intervals, now normalized.
    """
    if len(intervals) == 0:
        return intervals

    # Sort the intervals by their start point.
    intervals.sort(key=lambda i: i[0])

    merged: list[Interval] = [intervals[0]]
    for i in range(1, len(intervals)):
        last_start, last_end = merged[-1]
        current_start, current_end = intervals[i]

        if current_start <= last_end:
            # The intervals overlap, so merge them.
            merged[-1] = (last_start, max(last_end, current_end))
        else:
            # The intervals do not overlap, so add the current interval to the merged list.
            merged.append((current_start, current_end))
    # Update the input list with the merged intervals (side-effect).
    intervals[:] = merged
    return intervals


def size(intervals: list[Interval]) -> int:
    """Return the total number of integer points covered by the normalized interval list.

    Args:
        intervals: An interval list.

    Returns:
        Total covered size (count of integers).
    """
    return sum(e - s for s, e in intervals)


def split(intervals: list[Interval], point: int) -> tuple[list[Interval], list[Interval]]:
    """Split a normalized interval list at a given point into two lists.

    The input list is expected to be normalized. The resulting lists are also normalized.
    If the point is within an interval, that interval is split into two at the point and the point is included in the second list.

    Args:
        intervals: A normalized interval list.
        point: The integer point at which to split intervals.

    Returns:
        A tuple of two normalized interval lists.
    """

    if len(intervals) == 0:
        return [], []

    if point < intervals[0][0]:
        return [], intervals
    elif point >= intervals[-1][1]:
        return intervals, []

    for i in range(len(intervals)):
        if intervals[i][0] >= point:
            return intervals[:i], intervals[i:]
        elif intervals[i][1] > point:
            return intervals[:i] + [(intervals[i][0], point)], [(point, intervals[i][1])] + intervals[i + 1 :]


def intersects(intervals1: list[Interval], intervals2: list[Interval]) -> bool:
    """Return whether two normalized interval lists have any intersection.

    Both inputs are expected to be normalized.

    Args:
        intervals1: First normalized interval list.
        intervals2: Second normalized interval list.

    Returns:
        True if there is any intersection, False otherwise.
    """
    i1 = 0
    i2 = 0

    while i1 < len(intervals1) and i2 < len(intervals2):
        s1, e1 = intervals1[i1]
        s2, e2 = intervals2[i2]

        if s1 < e2 and s2 < e1:
            return True
        elif s1 < s2:
            i1 += 1
        else:
            i2 += 1

    return False


def contains(intervals: list[Interval], point: int) -> bool:
    """Return whether a normalized interval list contains a given point.

    The input list is expected to be normalized.

    Args:
        intervals: A normalized interval list.
        point: An integer point.

    Returns:
        True if the point is contained in any interval, False otherwise.
    """
    if len(intervals) == 0:
        return False

    if point < intervals[0][0] or point >= intervals[-1][1]:
        return False

    for start, end in intervals:
        if start <= point < end:
            return True
        elif start > point:
            # Since the intervals are sorted, we can stop checking once we reach an interval that starts after the point.
            break
    return False
