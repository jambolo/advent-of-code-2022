# Advent of Code 2022
# Day 3

from utils import setup, load


DAY = 3


def main() -> None:
    args = setup.parse_command_line(DAY)
    setup.print_banner(DAY, args.part)

    priorities = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    # Read the file
    lines = load.lines(args.input)

    priority_sum = 0

    if args.part == 1:
        for line in lines:
            line = line.strip()
            count = int(len(line) / 2)
            if len(line) != count * 2:
                raise Exception(f"Invalid line length: {line}")
            compartment1 = sorted(line[:count])
            compartment2 = sorted(line[count:])

            i1 = 0
            i2 = 0
            found = ""
            while not found and i1 < count and i2 < count:
                while not found and compartment1[i1] <= compartment2[i2]:
                    if compartment1[i1] == compartment2[i2]:
                        found = compartment1[i1]
                    else:
                        i1 = i1 + 1
                i2 = i2 + 1
            if not found:
                raise Exception(f"Unable to find common letter in {line}")

            priority = priorities.index(found) + 1
            priority_sum = priority_sum + priority

    elif args.part == 2:
        i = 0
        while i < len(lines):
            line1 = sorted(lines[i].strip())
            line2 = sorted(lines[i + 1].strip())
            line3 = sorted(lines[i + 2].strip())

            count1 = len(line1)
            count2 = len(line2)
            count3 = len(line3)

            i1 = 0
            i2 = 0
            i3 = 0
            found = ""
            while not found and i1 < count1 and i2 < count2 and i3 < count3:
                while (line1[i1] < line2[i2] or line1[i1] < line3[i3]) and i1 < count1:
                    i1 += 1
                while (line2[i2] < line1[i1] or line2[i2] < line3[i3]) and i2 < count2:
                    i2 += 1
                while (line3[i3] < line1[i1] or line3[i3] < line2[i2]) and i3 < count3:
                    i3 += 1
                if line1[i1] == line2[i2] and line2[i2] == line3[i3]:
                    found = line1[i1]

            if not found:
                raise Exception("Unable to find common letter")

            priority = priorities.index(found) + 1
            priority_sum = priority_sum + priority

            i += 3

    print(f"Result: {priority_sum}")


if __name__ == "__main__":
    main()
