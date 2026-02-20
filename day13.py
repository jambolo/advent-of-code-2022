# Advent of Code 2022
# Day 13

from utils import setup, load
import json
import functools


DAY = 13


def determine_order(left: list, right: list) -> int:
    i = 0
    while i < len(left) and i < len(right):
        if type(left[i]) is int and type(right[i]) is int:
            order = left[i] - right[i]
            if order != 0:
                return order
        elif type(left[i]) is int and type(right[i]) is list:
            listified = [left[i]]
            order = determine_order(listified, right[i])
            if order != 0:
                return order
        elif type(left[i]) is list and type(right[i]) is int:
            listified = [right[i]]
            order = determine_order(left[i], listified)
            if order != 0:
                return order
        elif type(left[i]) is list and type(right[i]) is list:
            order = determine_order(left[i], right[i])
            if order != 0:
                return order
        else:
            raise Exception("Invalid data type")
        i += 1

    return len(left) - len(right)


def main() -> None:
    args = setup.parse_command_line(DAY)
    setup.print_banner(DAY, args.part)

    # Read the file
    lines = load.lines(args.input)

    iLine = 0
    iPair = 1
    correctPairs = []

    while iLine < len(lines):
        # Load a pair
        left = json.loads(lines[iLine])
        iLine += 1
        if iLine >= len(lines):
            break

        right = json.loads(lines[iLine])
        iLine += 1
        iLine += 1  # skip blank line

        # If it is in the correct order, save the index
        order = determine_order(left, right)
        if order < 0:
            correctPairs.append(iPair)

        iPair += 1

    if args.part == 1:
        pair_sum = 0
        for p in correctPairs:
            pair_sum += p

        print("Result:", pair_sum)

    if args.part == 2:
        all_packets = [json.loads(line) for line in lines if len(line.strip()) > 0]
        all_packets.append([[2]])
        all_packets.append([[6]])
        s = sorted(all_packets, key=functools.cmp_to_key(determine_order))

        first = s.index([[2]]) + 1
        last = s.index([[6]]) + 1

        print("Result:", first * last)


if __name__ == "__main__":
    main()
