# Advent of Code 2022
# Day 16

from collections import defaultdict
from utils import setup, load, pathfinding
import re


DAY = 16


IMPASSABLE = float("inf")


def parse_nodes(lines: list[str]) -> dict[str, dict]:
    nodes = {}

    for line in lines:
        line = line.strip()
        match = re.search(
            r"Valve ([A-Z]{2}) has flow rate=(\d+); tunnels? leads? to valves? (([A-Z]{2},? ?)+)",
            line,
        )
        nodes[match.group(1)] = {
            "flow": int(match.group(2)),
            "next": re.split(", ", match.group(3)),
        }

    return nodes


def build_distance_map(nodes: dict[str, dict]) -> dict[tuple[str, str], int]:
    def neighbors_of(n):
        return nodes[n]["next"]

    def cost(n0, n1):
        return 1

    distances: dict[tuple[str, str], int] = defaultdict(lambda: IMPASSABLE)
    for n0 in nodes:
        # Will never leave from a node with 0 flow (except 'AA"), so skip those
        if nodes[n0]["flow"] == 0 and n0 != "AA":
            continue
        for n1 in nodes:
            # Will never go to a node with 0 flow, so skip those
            if nodes[n1]["flow"] == 0:
                continue
            if n0 == n1:
                distances[(n0, n1)] = 0
            else:
                # Since there is no heuristic, Dijkstra's algorithm is used
                d, _ = pathfinding.dijkstra(n0, n1, neighbors_of, cost)
                if d == IMPASSABLE:
                    raise Exception("Impassable from", n0, "to", n1)
                distances[(n0, n1)] = d
    return distances


def node_ids_not_in_path(nodes: dict[str, dict], path: list[str]) -> list[str]:
    return [n for n in nodes if n not in path]


def find_best_flow(
    nodes: dict[str, dict],
    path: list[str],
    elapsed: int,
    cache: dict[tuple[str, tuple[str, ...], int], tuple[int, list[str]]],
    distances: dict[tuple[str, str], int],
    time_limit: int,
) -> tuple[int, list[str]]:
    remaining_node_ids = node_ids_not_in_path(nodes, path)
    if not remaining_node_ids:
        return 0, []

    # If this state has already been computed, return the cached value.
    cache_key = (path[-1], tuple(remaining_node_ids), elapsed)
    if cache_key in cache:
        return cache[cache_key]

    best_flow = 0
    best_path_remaining = []
    here = path[-1]
    for n in remaining_node_ids:
        new_elapsed = elapsed + distances[(here, n)] + 1  # + 1 for the time to open the valve
        new_time_remaining = time_limit - new_elapsed
        if new_time_remaining > 0:  # Note: greater than because if equal, there is no time left to get any flow
            flow_n = nodes[n]["flow"] * new_time_remaining
            flow_remaining, path_remaining = find_best_flow(nodes, path + [n], new_elapsed, cache, distances, time_limit)
            if flow_n + flow_remaining > best_flow:
                best_flow = flow_n + flow_remaining
                best_path_remaining = [n] + path_remaining

    cache[cache_key] = (best_flow, best_path_remaining)
    return best_flow, best_path_remaining


def find_best_flow_part2(
    nodes: dict[str, dict],
    path: list[str],
    elapsed: int,
    cache: dict[tuple[str, tuple[str, ...], int], tuple[int, list[str]]],
    distances: dict[tuple[str, str], int],
    time_limit: int,
) -> int:
    remaining_node_ids = node_ids_not_in_path(nodes, path)
    if not remaining_node_ids:
        return 0

    best_flow = 0
    here = path[-1]
    for n in remaining_node_ids:
        new_elapsed = elapsed + distances[(here, n)] + 1  # + 1 for the time to open the valve
        new_time_remaining = time_limit - new_elapsed
        if new_time_remaining > 0:  # Note: greater than because if equal, there is no time left to get any flow
            flow_n = nodes[n]["flow"] * new_time_remaining
            flow_remaining = find_best_flow_part2(nodes, path + [n], new_elapsed, cache, distances, time_limit)
            best_flow = max(best_flow, flow_n + flow_remaining)

    # What if the elephant takes the remaining nodes instead of me? (Only if there are any remaining nodes, otherwise we would have already returned above.)
    if remaining_node_ids:
        best_flow_e, _ = find_best_flow(nodes, path + ["AA"], 0, cache, distances, time_limit)
        best_flow = max(best_flow, best_flow_e)

    return best_flow


def main() -> None:
    args = setup.parse_command_line(DAY)
    setup.print_banner(DAY, args.part)

    lines = load.lines(args.input)
    nodes = parse_nodes(lines)

    # Determine the distances between nodes.
    distances = build_distance_map(nodes)

    # Only consider nodes with flow, since we will never visit nodes with 0 flow (except "AA").
    nodes_with_flow = {n: nodes[n] for n in nodes if nodes[n]["flow"] > 0}

    if args.part == 1:
        time_limit = 30
        flow, path = find_best_flow(nodes_with_flow, ["AA"], 0, {}, distances, time_limit)

        print("Result:", flow)

    if args.part == 2:
        time_limit = 26
        flow = find_best_flow_part2(nodes_with_flow, ["AA"], 0, {}, distances, time_limit)

        print("Result:", flow)


if __name__ == "__main__":
    main()
