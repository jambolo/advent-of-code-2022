# Advent of Code 2022
# Day 15

from __future__ import annotations

import argparse
import re
from typing import Iterable, TypedDict, TypeAlias

from utils import interval, load, setup


DAY: int = 15


class Point(TypedDict):
    x: int
    y: int


class Sensor(TypedDict):
    sensor: Point
    distance: int


Beacon: TypeAlias = tuple[int, int]


def parse_input(lines: Iterable[str]) -> tuple[list[Sensor], set[Beacon]]:
    sensors: list[Sensor] = []
    beacons: set[Beacon] = set()

    for line in lines:
        match: re.Match[str] | None = re.search(
            r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)",
            line,
        )
        if match is None:
            raise ValueError(f"Invalid input line: {line!r}")
        sensor_x: int = int(match.group(1))
        sensor_y: int = int(match.group(2))
        beacon_x: int = int(match.group(3))
        beacon_y: int = int(match.group(4))

        sensors.append(
            {
                "sensor": {"x": sensor_x, "y": sensor_y},
                "distance": distance(sensor_x, sensor_y, beacon_x, beacon_y),
            }
        )
        beacons.add((beacon_x, beacon_y))

    return sensors, beacons


def distance(x0: int, y0: int, x1: int, y1: int) -> int:
    """Manhattan distance between two points."""
    return abs(x1 - x0) + abs(y1 - y0)


def compute_map_extents(sensors: list[Sensor]) -> tuple[int, int, int, int]:
    min_x: int = sensors[0]["sensor"]["x"]
    max_x: int = sensors[0]["sensor"]["x"]
    min_y: int = sensors[0]["sensor"]["y"]
    max_y: int = sensors[0]["sensor"]["y"]
    for sensor in sensors:
        sensor_x: int = sensor["sensor"]["x"]
        sensor_y: int = sensor["sensor"]["y"]
        beacon_x: int = sensor["beacon"]["x"]
        beacon_y: int = sensor["beacon"]["y"]
        d: int = sensor["distance"]
        min_x = min(min_x, sensor_x - d, beacon_x - d)
        max_x = max(max_x, sensor_x + d, beacon_x + d)
        min_y = min(min_y, sensor_y - d, beacon_y - d)
        max_y = max(max_y, sensor_y + d, beacon_y + d)
    return min_x, min_y, max_x, max_y


def coverage_at_row(sensor: Sensor, row: int) -> tuple[int, int] | None:
    """Compute the interval of x coordinates covered by a sensor at a given row, or None if the sensor does not cover that row.

    The returned interval is half-open: [start, end), meaning it includes start but not end.
    """
    sensor_x: int = sensor["sensor"]["x"]
    sensor_y: int = sensor["sensor"]["y"]
    d: int = sensor["distance"]
    offset: int = d - abs(row - sensor_y)
    if offset < 0:
        return None
    else:
        return [sensor_x - offset, sensor_x + offset + 1]


def main() -> None:
    args: argparse.Namespace = setup.parse_command_line(DAY)
    setup.print_banner(DAY, args.part)

    args.input = args.input

    # Read the file.
    lines: list[str] = load.lines(args.input)

    # Load the sensors
    sensors, beacons = parse_input(lines)

    if args.part == 1:
        ROW: int = 2000000

        # Compute the total coverage for the row
        total_coverage: list[interval.Interval] = []
        for s in sensors:
            sensor_coverage: tuple[int, int] | None = coverage_at_row(s, ROW)
            if sensor_coverage is not None:
                interval.add_interval(total_coverage, sensor_coverage)

        # Exclude the beacons at the row
        excluded_count: int = 0
        for b in beacons:
            if b[1] == ROW and interval.contains(total_coverage, b[0]):
                excluded_count += 1
        print("Result:", interval.size(total_coverage) - excluded_count)

    elif args.part == 2:
        min_x: int = 0
        max_x: int = 4000000
        min_y: int = 0
        max_y: int = 4000000

        # Exclude all points within beacon range
        # groups: list[list[list[int]]] = [[[min_x, max_x]]] * (max_y - min_y + 1)
        line_intervals: list[list[interval.Interval]] = [[] for _ in range(max_y - min_y + 1)]
        for s in sensors:
            sx: int = s["sensor"]["x"]
            sy: int = s["sensor"]["y"]
            d: int = s["distance"]
            for r in range(max(min_y, sy - d), min(max_y + 1, sy + d)):
                offset: int = d - abs(r - sy)
                interval.add_interval(line_intervals[r], [max(min_x, sx - offset), min(max_x + 1, sx + offset + 1)])

        for i in range(len(line_intervals)):
            y = min_y + i
            line: list[interval.Interval] = line_intervals[i]
            size: int = interval.size(line)
            if size < max_x - min_x + 1:
                x = line[0][1]
                print("Result:", x * 4000000 + y)
                break


if __name__ == "__main__":
    main()
