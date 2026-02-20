# Advent of Code 2022
# Day 11

from utils import setup, load
import re


DAY = 11

NUMBER_OF_MONKEYS = 8


def new_worry(value: str, op: str, worry: int) -> int:
    if value == "old":
        operand = worry
    else:
        operand = int(value)
    if op == "+":
        worry += operand
    elif op == "*":
        worry *= operand
    else:
        raise Exception("Invalid operation:", op)
    worry //= 3
    return worry


def new_worry2(value: str, op: str, divisor: int, worry: int) -> int:
    if value == "old":
        operand = worry
    else:
        operand = int(value)
    if op == "+":
        worry += operand
    elif op == "*":
        worry *= operand
    else:
        raise Exception("Invalid operation:", op)
    worry %= divisor
    return worry


def main() -> None:
    args = setup.parse_command_line(DAY)
    setup.print_banner(DAY, args.part)

    # Read the file
    lines = load.lines(args.input)

    if args.part == 1:
        number_of_rounds = 20
    if args.part == 2:
        number_of_rounds = 10000

    n_monkeys = 0
    i_line = 0
    monkeys = []
    while i_line < len(lines):
        # Read monkey number
        match = re.findall(r"\d+", lines[i_line])
        i_line += 1
        if int(match[0]) != n_monkeys:
            raise Exception(f"Unexpected monkey {match[0]}")

        # Read the monkey's starting items
        match = re.findall(r"\d+", lines[i_line])
        i_line += 1
        items = []
        for m in match:
            w = int(m)
            items.append([w for i in range(NUMBER_OF_MONKEYS)])

        # Read operation
        match = re.search(r"\s*Operation: new = old (.) (.+)", lines[i_line])
        i_line += 1
        op = match.group(1)
        value = match.group(2)

        # Read test
        match = re.findall(r"\d+", lines[i_line])
        i_line += 1
        test = int(match[0])
        match = re.findall(r"\d+", lines[i_line])
        i_line += 1
        true_action = int(match[0])
        if true_action == n_monkeys:
            raise Exception("Monkey throwing to self.")
        match = re.findall(r"\d+", lines[i_line])
        i_line += 1
        false_action = int(match[0])
        if false_action == n_monkeys:
            raise Exception("Monkey throwing to self.")

        monkey = {
            "items": items,
            "op": op,
            "value": value,
            "test": test,
            "trueAction": true_action,
            "falseAction": false_action,
            "inspectionCount": 0,
        }
        monkeys.append(monkey)
        i_line += 1  # Skip blank line
        n_monkeys += 1

    if n_monkeys != NUMBER_OF_MONKEYS:
        raise Exception(f"Expected {NUMBER_OF_MONKEYS} monkeys")

    for round in range(1, number_of_rounds + 1):
        for k in range(NUMBER_OF_MONKEYS):
            m = monkeys[k]
            for item in m["items"]:
                if args.part == 2:
                    for i in range(len(item)):  # for each monkey
                        item[i] = new_worry2(m["value"], m["op"], monkeys[i]["test"], item[i])
                else:
                    for i in range(len(item)):  # for each monkey
                        item[i] = new_worry(m["value"], m["op"], item[i])
                if (args.part == 1 and item[k] % m["test"] == 0) or (args.part == 2 and item[k] == 0):
                    monkeys[m["trueAction"]]["items"].append(item)
                else:
                    monkeys[m["falseAction"]]["items"].append(item)
            m["inspectionCount"] += len(m["items"])
            m["items"] = []

    # Find the top 2
    count1 = 0
    count2 = 0
    for m in monkeys:
        if m["inspectionCount"] > count1:
            count2 = count1
            count1 = m["inspectionCount"]
        elif m["inspectionCount"] > count2:
            count2 = m["inspectionCount"]

    print(f"Result: {count1 * count2}")


if __name__ == "__main__":
    main()
