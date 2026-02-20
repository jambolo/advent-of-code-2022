# Advent of Code 2022
# Day 23

from utils import setup, load


DAY = 23

# Direction constants (8 directions, counter-clockwise starting from E)
E = 0
NE = 1
N = 2
NW = 3
W = 4
SW = 5
S = 6
SE = 7

type Vec2 = tuple[int, int]  # [x, y]
type ElfList = set[Vec2]
type ProposalCheck = tuple[int, int, int]  # 3 offsets to check. The proposed movement is the 2nd offset.


DIRECTION_OFFSETS: list[Vec2] = [
    (+1, 0),  # E
    (+1, -1),  # NE
    (0, -1),  # N
    (-1, -1),  # NW
    (-1, 0),  # W
    (-1, +1),  # SW
    (0, +1),  # S
    (+1, +1),  # SE
]

# List of proposal checks in the initial order (N< S< W< E).
INITIAL_PROPOSAL_CHECKS: list[ProposalCheck] = [(NW, N, NE), (SW, S, SE), (NW, W, SW), (NE, E, SE)]


def replace_at_index(s: str, i: int, c: str) -> str:
    """Returns a copy of s with the string starting at index i replaced by c."""
    return s[:i] + c + s[i + len(c) :]


def compute_extents(elves: ElfList) -> tuple[int, int, int, int]:
    """Computes the extents of the elves' positions. Returns (min_x, max_x, min_y, max_y)"""
    xs, ys = zip(*elves)
    return (min(xs), max(xs), min(ys), max(ys))


def alone(e: Vec2, elves: ElfList) -> bool:
    for offset in DIRECTION_OFFSETS:
        if (e[0] + offset[0], e[1] + offset[1]) in elves:
            return False
    return True


def can_move(e: Vec2, elves: ElfList, check: ProposalCheck) -> bool:
    for c in check:
        offset = DIRECTION_OFFSETS[c]
        if (e[0] + offset[0], e[1] + offset[1]) in elves:
            return False
    return True


def proposed_movement(e: Vec2, check: ProposalCheck) -> Vec2:
    offset = DIRECTION_OFFSETS[check[1]]
    return (e[0] + offset[0], e[1] + offset[1])


def main() -> None:
    args = setup.parse_command_line(DAY)
    setup.print_banner(DAY, args.part)

    # Read the file.
    lines: list[str] = load.lines(args.input)

    elves: ElfList = set()
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            if lines[y][x] == "#":
                elves.add((x, y))

    proposal_checks = INITIAL_PROPOSAL_CHECKS.copy()

    if args.part == 1:
        number_of_rounds = 10
    if args.part == 2:
        number_of_rounds = 2000000000  # arbitrary large number

    for round in range(number_of_rounds):
        proposed: dict[Vec2, list[Vec2]] = {}
        stationary_count: int = 0

        # Propose movement
        for e in elves:
            proposal: Vec2 | None
            if alone(e, elves):
                proposal = None
                stationary_count += 1
            elif can_move(e, elves, proposal_checks[(round + 0) % 4]):
                proposal = proposed_movement(e, proposal_checks[(round + 0) % 4])
            elif can_move(e, elves, proposal_checks[(round + 1) % 4]):
                proposal = proposed_movement(e, proposal_checks[(round + 1) % 4])
            elif can_move(e, elves, proposal_checks[(round + 2) % 4]):
                proposal = proposed_movement(e, proposal_checks[(round + 2) % 4])
            elif can_move(e, elves, proposal_checks[(round + 3) % 4]):
                proposal = proposed_movement(e, proposal_checks[(round + 3) % 4])
            else:
                proposal = None
                stationary_count += 1

            if proposal is not None:
                if proposal not in proposed:
                    proposed[proposal] = []
                proposed[proposal].append(e)
            else:
                if e not in proposed:
                    proposed[e] = []
                proposed[e].append(e)

        if args.part == 2 and stationary_count == len(elves):
            print("Result:", round + 1)
            return

        # Resolve
        for p, elves_list in proposed.items():
            if len(elves_list) == 1:
                e = elves_list[0]
                elves.remove(e)
                elves.add(p)

        round += 1

    if args.part == 1:
        (min_x, max_x, min_y, max_y) = compute_extents(elves)

        empty_spaces = (max_x - min_x + 1) * (max_y - min_y + 1) - len(elves)
        print("Result:", empty_spaces)


if __name__ == "__main__":
    main()
