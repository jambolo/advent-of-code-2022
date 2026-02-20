# Advent of Code 2022
# Day 19

from __future__ import annotations
from utils import setup, load
import re


DAY = 19

GEODE = 0
OBSIDIAN = 1
CLAY = 2
ORE = 3
GEODE_ROBOT = 4
OBSIDIAN_ROBOT = 5
CLAY_ROBOT = 6
ORE_ROBOT = 7

type Cost = tuple[int, int, int, int]
type Blueprint = tuple[Cost, Cost, Cost, Cost]
type State = tuple[int, int, int, int, int, int, int, int]


def build(state: State, idle_time: int, blueprint: Blueprint, robot: int):
    # Collect resources during idle time and the time to build the robot
    build_time = idle_time + 1
    geode = state[GEODE] + state[GEODE_ROBOT] * build_time
    obsidian = state[OBSIDIAN] + state[OBSIDIAN_ROBOT] * build_time
    clay = state[CLAY] + state[CLAY_ROBOT] * build_time
    ore = state[ORE] + state[ORE_ROBOT] * build_time

    # Spend resources to build the robot
    geode -= blueprint[robot][GEODE]
    obsidian -= blueprint[robot][OBSIDIAN]
    clay -= blueprint[robot][CLAY]
    ore -= blueprint[robot][ORE]

    geode_robots = state[GEODE_ROBOT] + (1 if robot == GEODE else 0)
    obsidian_robots = state[OBSIDIAN_ROBOT] + (1 if robot == OBSIDIAN else 0)
    clay_robots = state[CLAY_ROBOT] + (1 if robot == CLAY else 0)
    ore_robots = state[ORE_ROBOT] + (1 if robot == ORE else 0)

    return (geode, obsidian, clay, ore, geode_robots, obsidian_robots, clay_robots, ore_robots)


def parse_blueprints(lines: list[str]) -> list[Blueprint]:
    blueprints = []
    for line in lines:
        match = re.search(
            r"Blueprint \d+:"
            r" Each ore robot costs (\d+) ore."
            r" Each clay robot costs (\d+) ore."
            r" Each obsidian robot costs (\d+) ore and (\d+) clay."
            r" Each geode robot costs (\d+) ore and (\d+) obsidian.",
            line,
        )
        ore_robot_cost = (0, 0, 0, int(match.group(1)))
        clay_robot_cost = (0, 0, 0, int(match.group(2)))
        obsidian_robot_cost = (0, 0, int(match.group(4)), int(match.group(3)))
        geode_robot_cost = (0, int(match.group(6)), 0, int(match.group(5)))
        blueprint = (geode_robot_cost, obsidian_robot_cost, clay_robot_cost, ore_robot_cost)
        blueprints.append(blueprint)

    return blueprints


# Maps current state at the specified elapsed time to the best final state that can result from it.
type StateCacheKey = tuple[State, int]
type StateCache = dict[StateCacheKey, int]

state_cache: StateCache = dict()
state_cache_hits: int = 0
state_cache_misses: int = 0


def clear_state_cache() -> None:
    global state_cache, state_cache_hits, state_cache_misses
    state_cache.clear()
    state_cache_hits = 0
    state_cache_misses = 0


def find_most_geodes(blueprint: Blueprint, max_demand: Cost, state: State, elapsed: int, best_so_far: int, time_limit: int) -> int:
    global state_cache, state_cache_hits, state_cache_misses

    if elapsed >= time_limit:
        return state[GEODE]

    # Check if we have already explored this state at this elapsed time.
    cache_key = (state, elapsed)
    if cache_key in state_cache:
        state_cache_hits += 1
        return state_cache[cache_key]
    else:
        state_cache_misses += 1

    remaining_time = time_limit - elapsed

    # If a state has already been found with at least as many geodes as can ever be found from
    # this state, then there is no point in exploring further.
    if best_so_far > best_possible_outcome(state, remaining_time):
        return state[GEODE]

    best_final_count = state[GEODE]

    final_count = build_geode_robot_next(blueprint, max_demand, state, elapsed, max(best_final_count, best_so_far), time_limit)
    if final_count > best_final_count:
        best_final_count = final_count

    # Try building an obsidian robot next, but only if there isn't already enough obsidian and obsidian robots.
    if state[OBSIDIAN] < max_demand[OBSIDIAN] * remaining_time and state[OBSIDIAN_ROBOT] < max_demand[OBSIDIAN]:
        final_count = build_obsidian_robot_next(
            blueprint, max_demand, state, elapsed, max(best_final_count, best_so_far), time_limit
        )
        if final_count > best_final_count:
            best_final_count = final_count

    # Try building a clay robot next, but only if there isn't already enough clay and clay robots.
    if state[CLAY] < max_demand[CLAY] * remaining_time and state[CLAY_ROBOT] < max_demand[CLAY]:
        final_count = build_clay_robot_next(blueprint, max_demand, state, elapsed, max(best_final_count, best_so_far), time_limit)
        if final_count > best_final_count:
            best_final_count = final_count

    # Try building an ore robot next, but only if there isn't already enough ore and ore robots.
    if state[ORE] < max_demand[ORE] * remaining_time and state[ORE_ROBOT] < max_demand[ORE]:
        final_count = build_ore_robot_next(blueprint, max_demand, state, elapsed, max(best_final_count, best_so_far), time_limit)
        if final_count > best_final_count:
            best_final_count = final_count

    # Try not building any more robots, and just collecting with the current robots until the end.
    final_count = state[GEODE] + state[GEODE_ROBOT] * remaining_time
    if final_count > best_final_count:
        best_final_count = final_count

    # Cache and return the best final count
    state_cache[cache_key] = best_final_count
    return best_final_count


def idle_time_for_obsidian(cost: Cost, state: State):
    if state[OBSIDIAN_ROBOT] == 0:
        return float("inf")
    elif state[OBSIDIAN] >= cost[OBSIDIAN]:
        return 0
    else:
        return (cost[OBSIDIAN] - state[OBSIDIAN] + state[OBSIDIAN_ROBOT] - 1) // state[OBSIDIAN_ROBOT]


def idle_time_for_clay(cost: Cost, state: State):
    if state[CLAY_ROBOT] == 0:
        return float("inf")
    elif state[CLAY] >= cost[CLAY]:
        return 0
    else:
        return (cost[CLAY] - state[CLAY] + state[CLAY_ROBOT] - 1) // state[CLAY_ROBOT]


def idle_time_for_ore(cost: Cost, state: State):
    if state[ORE_ROBOT] == 0:
        return float("inf")
    elif state[ORE] >= cost[ORE]:
        return 0
    else:
        return (cost[ORE] - state[ORE] + state[ORE_ROBOT] - 1) // state[ORE_ROBOT]


def build_geode_robot_next(
    blueprint: Blueprint, max_demand: Cost, state: State, elapsed: int, best_so_far: int, time_limit: int
) -> int:

    # Find how long to build a geode robot
    idle_time_ore = idle_time_for_ore(blueprint[GEODE], state)
    idle_time_obsidian = idle_time_for_obsidian(blueprint[GEODE], state)
    idle_time = max(idle_time_ore, idle_time_obsidian)
    idle_time = min(idle_time, time_limit - elapsed)

    # If there isn't time to build the robot and collect, then then building a geode robot will not increase the number of geodes
    # and the current state is the best that can be done.
    if time_limit - (elapsed + idle_time) < 2:
        return state[GEODE]

    # Build the geode robot
    next_state = build(state, idle_time, blueprint, GEODE)
    elapsed += idle_time + 1

    # Continue to build more robots
    return find_most_geodes(blueprint, max_demand, next_state, elapsed, best_so_far, time_limit)


def build_obsidian_robot_next(
    blueprint: Blueprint, max_demand: Cost, state: State, elapsed: int, best_so_far: int, time_limit: int
) -> int:

    # Find out how long to build an obsidian robot
    idle_time_ore = idle_time_for_ore(blueprint[OBSIDIAN], state)
    idle_time_clay = idle_time_for_clay(blueprint[OBSIDIAN], state)
    idle_time = max(idle_time_ore, idle_time_clay)
    idle_time = min(idle_time, time_limit - elapsed)

    # Ultimately, the obsidian produced by the new obsidian robot is used to build a new geode robot.
    # If there isn't enough time to
    #   1. build the obsidian robot and collect, and then
    #   2. build the geode robot and collect,
    # then building an obsidian robot will not increase the number of geodes.
    if time_limit - (elapsed + idle_time) < 4:
        return state[GEODE]

    # Build the obsidian robot
    next_state = build(state, idle_time, blueprint, OBSIDIAN)
    elapsed += idle_time + 1

    # Continue to build more robots
    return find_most_geodes(blueprint, max_demand, next_state, elapsed, best_so_far, time_limit)


def build_clay_robot_next(
    blueprint: Blueprint, max_demand: Cost, state: State, elapsed: int, best_so_far: int, time_limit: int
) -> int:
    # Find out how long to build a clay robot
    idle_time = idle_time_for_ore(blueprint[CLAY], state)
    idle_time = min(idle_time, time_limit - elapsed)

    # Ultimately, the clay produced by the new clay robot is used to build a new obsidian robot, and then a new geode robot.
    # If there isn't enough time to
    #   1. build the clay robot and collect, and then
    #   2. build the obsidian robot and collect, and finally
    #   3. build the geode robot and collect,
    # then building a clay robot will not increase the number of geodes.
    if time_limit - (elapsed + idle_time) < 6:
        return state[GEODE]

    # Build the clay robot
    next_state = build(state, idle_time, blueprint, CLAY)
    elapsed += idle_time + 1

    # Continue to build more robots
    return find_most_geodes(blueprint, max_demand, next_state, elapsed, best_so_far, time_limit)


def build_ore_robot_next(
    blueprint: Blueprint, max_demand: Cost, state: State, elapsed: int, best_so_far: int, time_limit: int
) -> int:
    # Find out how long to build an ore robot
    idle_time = idle_time_for_ore(blueprint[ORE], state)
    idle_time = min(idle_time, time_limit - elapsed)

    # Ultimately, the ore produced by the new ore robot is used to build a new geode robot.
    # If there isn't enough time to:
    #   1. build the ore robot and collect, and then
    #   2. build the geode robot and collect,
    # then building an ore robot will not increase the number of geodes, so return the current value
    if time_limit - (elapsed + idle_time) < 4:
        return state[GEODE]

    # Build an ore robot
    next_state = build(state, idle_time, blueprint, ORE)
    elapsed += idle_time + 1

    # Continue to build more robots
    return find_most_geodes(blueprint, max_demand, next_state, elapsed, best_so_far, time_limit)


def best_possible_outcome(state: State, time_remaining: int) -> int:
    """Calculate the best possible number of geodes we can get from this state, assuming we can build a geode robot every minute."""
    return state[GEODE] + state[GEODE_ROBOT] * time_remaining + (time_remaining * (time_remaining - 1)) // 2


def calculate_max_demand(b):
    max_demand = (
        max(b[GEODE][GEODE], b[OBSIDIAN][GEODE], b[CLAY][GEODE], b[ORE][GEODE]),
        max(b[GEODE][OBSIDIAN], b[OBSIDIAN][OBSIDIAN], b[CLAY][OBSIDIAN], b[ORE][OBSIDIAN]),
        max(b[GEODE][CLAY], b[OBSIDIAN][CLAY], b[CLAY][CLAY], b[ORE][CLAY]),
        max(b[GEODE][ORE], b[OBSIDIAN][ORE], b[CLAY][ORE], b[ORE][ORE]),
    )
    return max_demand


def main() -> None:
    args = setup.parse_command_line(DAY)
    setup.print_banner(DAY, args.part)

    if args.part == 1:
        TIME_LIMIT = 24
    else:
        TIME_LIMIT = 32

    # Read the file.
    lines = load.lines(args.input)
    blueprints = parse_blueprints(lines)

    if args.part == 1:
        quality_sum = 0
        for i, b in enumerate(blueprints):
            clear_state_cache()
            initial_state = (0, 0, 0, 0, 0, 0, 0, 1)
            max_demand = calculate_max_demand(b)
            count = find_most_geodes(b, max_demand, initial_state, 0, 0, TIME_LIMIT)
            quality = count * (i + 1)
            quality_sum += quality
        print("Result:", quality_sum)

    if args.part == 2:
        product = 1
        for i, b in enumerate(blueprints[:3]):
            clear_state_cache()
            initial_state = (0, 0, 0, 0, 0, 0, 0, 1)
            max_demand = calculate_max_demand(b)
            count = find_most_geodes(b, max_demand, initial_state, 0, 0, TIME_LIMIT)
            product *= count
        print("Result:", product)

    return max_demand


if __name__ == "__main__":
    main()
