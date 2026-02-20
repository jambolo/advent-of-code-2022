"""A* search algorithm for finding the lowest-cost path between two nodes in a graph.

Nodes can be any hashable type. The graph structure, edge costs, and heuristic
are supplied as callback functions, making this implementation independent of
any particular graph representation.
"""

import heapq
from collections import defaultdict
from collections.abc import Hashable, Iterable
from itertools import count
from typing import Callable, TypeVar

N = TypeVar("N", bound=Hashable)


def _reconstruct_path(came_from: dict[N, N], start: N, end: N) -> list[N]:
    path: list[N] = []
    while end != start:
        path.insert(0, end)
        end = came_from[end]
    path.insert(0, end)
    return path


def a_star(
    start: N,
    goal: N,
    neighbors_of: Callable[[N], Iterable[N]],
    h: Callable[[N], float],
    cost_of: Callable[[N, N], float],
) -> tuple[float, list[N]]:
    """Find the lowest-cost path from *start* to *goal* using A*.

    Args:
        start: The starting node.
        goal: The target node.
        neighbors_of: Given a node, return an iterable of adjacent nodes.
        h: Heuristic function estimating the cost from a node to the goal.
            Must be admissible (never overestimate) for optimality.
        cost_of: Given two adjacent nodes (a, b), return the traversal cost
            from a to b.

    Returns:
        A tuple of (total_cost, path) where path is a list of nodes from
        start to goal inclusive. If no path exists, returns (inf, []).
    """
    # Tiebreaker counter so heapq never compares nodes directly. This hack is necessary because heapq can only compare the entire value.
    counter = count()

    # The set of discovered nodes that may need to be (re-)expanded.
    open_set: list[tuple[float, int, N]] = []
    heapq.heappush(open_set, (0, next(counter), start))

    # For node n, came_from[n] is the node immediately preceding it on the
    # cheapest path from start to n currently known.
    came_from: dict[N, N] = {}

    # For node n, g_scores[n] is the cost of the cheapest path from start to n
    # currently known.
    g_scores: defaultdict[N, float] = defaultdict(lambda: float("inf"))
    g_scores[start] = 0

    visited: set[N] = set()

    while open_set:
        _, _, node_id = heapq.heappop(open_set)
        if node_id == goal:
            return (g_scores[goal], _reconstruct_path(came_from, start, goal))
        if node_id in visited:
            continue
        visited.add(node_id)

        for neighbor_id in neighbors_of(node_id):
            tentative_g_score: float = g_scores[node_id] + cost_of(node_id, neighbor_id)
            if tentative_g_score < g_scores[neighbor_id]:
                came_from[neighbor_id] = node_id
                g_scores[neighbor_id] = tentative_g_score
                if neighbor_id not in visited:
                    f_score: float = tentative_g_score + h(neighbor_id)
                    heapq.heappush(open_set, (f_score, next(counter), neighbor_id))

    # Open set is empty but goal was never reached
    return (float("inf"), [])


def dijkstra(
    start: N,
    goal: N,
    neighbors_of: Callable[[N], Iterable[N]],
    cost_of: Callable[[N, N], float],
) -> tuple[float, list[N]]:
    """Find the lowest-cost path from *start* to *goal* using Dijkstra's algorithm.

    Args:
        start: The starting node.
        goal: The target node.
        neighbors_of: Given a node, return an iterable of adjacent nodes.
        cost_of: Given two adjacent nodes (a, b), return the traversal cost
            from a to b.

    Returns:
        A tuple of (total_cost, path) where path is a list of nodes from
        start to goal inclusive. If no path exists, returns (inf, []).
    """
    # Tiebreaker counter so heapq never compares nodes directly. This hack is necessary because heapq can only compare the entire value.
    counter = count()

    # The set of discovered nodes that may need to be (re-)expanded.
    open_set: list[tuple[float, int, N]] = []
    heapq.heappush(open_set, (0, next(counter), start))

    # For node n, came_from[n] is the node immediately preceding it on the
    # cheapest path from start to n currently known.
    came_from: dict[N, N] = {}

    # For node n, g_scores[n] is the cost of the cheapest path from start to n
    # currently known.
    costs: defaultdict[N, float] = defaultdict(lambda: float("inf"))
    costs[start] = 0

    visited: set[N] = set()

    while open_set:
        current_cost, _, current_node = heapq.heappop(open_set)
        if current_node == goal:
            return (current_cost, _reconstruct_path(came_from, start, goal))
        if current_node in visited:
            continue
        visited.add(current_node)

        for neighbor_id in neighbors_of(current_node):
            neighbor_cost: float = current_cost + cost_of(current_node, neighbor_id)
            if neighbor_cost < costs[neighbor_id]:
                came_from[neighbor_id] = current_node
                costs[neighbor_id] = neighbor_cost
                heapq.heappush(open_set, (neighbor_cost, next(counter), neighbor_id))

    # Open set is empty but goal was never reached
    return (float("inf"), [])
