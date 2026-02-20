# Advent of Code 2022
# Day 21

from utils import setup, load
import re


DAY = 21


def evaluate(monkeys, name):
    m = monkeys[name]
    if "value" in m:
        return m["value"]
    else:
        operand0 = m["operands"][0]
        operand1 = m["operands"][1]
        if m["op"] == "+":
            return evaluate(monkeys, operand0) + evaluate(monkeys, operand1)
        elif m["op"] == "-":
            return evaluate(monkeys, operand0) - evaluate(monkeys, operand1)
        elif m["op"] == "*":
            return evaluate(monkeys, operand0) * evaluate(monkeys, operand1)
        elif m["op"] == "/":
            return evaluate(monkeys, operand0) / evaluate(monkeys, operand1)
        elif m["op"] == "=":
            return evaluate(monkeys, operand0) == evaluate(monkeys, operand1)
        else:
            raise Exception("invalid operator")


def find_path(monkeys, node, name):
    m = monkeys[node]
    if node == name:
        return [name]
    if "value" in m:
        return None
    path = find_path(monkeys, m["operands"][0], name)
    if not path:
        path = find_path(monkeys, m["operands"][1], name)
    if not path:
        return None
    new_path = path.copy()
    new_path.insert(0, node)
    return new_path


def invert(monkeys, name, path, goal):
    if name == "humn":
        return goal
    m = monkeys[name]
    if m["operands"][0] not in path:
        operand0 = evaluate(monkeys, m["operands"][0])
        if m["op"] == "+":
            humn = invert(monkeys, m["operands"][1], path, goal - operand0)
        elif m["op"] == "-":
            humn = invert(monkeys, m["operands"][1], path, operand0 - goal)
        elif m["op"] == "*":
            humn = invert(monkeys, m["operands"][1], path, goal / operand0)
        elif m["op"] == "/":
            humn = invert(monkeys, m["operands"][1], path, operand0 / goal)
        elif m["op"] == "=":
            humn = invert(
                monkeys,
                m["operands"][1],
                path,
                operand0 if goal else -operand0,
            )
    else:
        operand1 = evaluate(monkeys, m["operands"][1])
        if m["op"] == "+":
            humn = invert(monkeys, m["operands"][0], path, goal - operand1)
        elif m["op"] == "-":
            humn = invert(monkeys, m["operands"][0], path, goal + operand1)
        elif m["op"] == "*":
            humn = invert(monkeys, m["operands"][0], path, goal / operand1)
        elif m["op"] == "/":
            humn = invert(monkeys, m["operands"][0], path, goal * operand1)
        elif m["op"] == "=":
            humn = invert(
                monkeys,
                m["operands"][0],
                path,
                operand1 if goal else -operand1,
            )
    return humn


def main() -> None:
    args = setup.parse_command_line(DAY)
    setup.print_banner(DAY, args.part)

    # Read the file.
    lines = load.lines(args.input)

    monkeys = {}
    for line in lines:
        match = re.search(r"([a-z]{4})\: (\d+|([a-z]{4}) ([\+\-\*\/]) ([a-z]{4}))", line)
        if match.group(3):
            monkey = {
                "op": match.group(4),
                "operands": [match.group(3), match.group(5)],
            }
        else:
            monkey = {"value": int(match.group(2))}
        monkeys[match.group(1)] = monkey

    root = monkeys["root"]

    if args.part == 1:
        value = evaluate(monkeys, "root")
        print("Result: ", int(value))

    if args.part == 2:
        root["op"] = "="

        n = "humn"
        test_path = ["humn"]
        while n != "root":
            for m in monkeys:
                if "value" not in monkeys[m]:
                    if n in monkeys[m]["operands"]:
                        n = m
                        test_path.append(m)
                        break

        path_to_humn = find_path(monkeys, "root", "humn")

        if root["operands"][0] not in path_to_humn:
            goal = evaluate(monkeys, root["operands"][0])
            humn = invert(monkeys, root["operands"][1], path_to_humn, goal)
        else:
            goal = evaluate(monkeys, root["operands"][1])
            humn = invert(monkeys, root["operands"][0], path_to_humn, goal)
        print("Result:", int(humn))


if __name__ == "__main__":
    main()
