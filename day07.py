# Advent of Code 2022
# Day 7

from __future__ import annotations

from utils import setup, load
import re


DAY = 7

THRESHOLD = 100000
TOTAL_SPACE = 70000000
MINIMUM_UNUSED = 30000000


class Node:
    def __init__(self, name: str, size: int, parent: Node | None = None) -> None:
        self.parent: Node | None = parent
        self.name: str = name
        self.size: int = size
        self.nodes: list[Node] = []
        self.files: list[Node] = []


def cd(where: str, node: Node, root: Node) -> Node | None:
    if where == "/":
        cwd = None
    elif where == "..":
        if node == root:
            raise Exception("cd .. at root")
        cwd = node.parent
    else:
        for n in node.nodes:
            if n.name == where:
                cwd = n
                break
    return cwd


def add_node(name: str, node: Node, cwd: Node) -> None:
    found = False
    for n in node.nodes:
        if n.name == name:
            found = True
            break
    if not found:
        node.nodes.append(Node(name, 0, cwd))


def add_file(name: str, size: int, node: Node) -> None:
    found = False
    for n in node.files:
        if n.name == name:
            found = True
            break
    if not found:
        node.files.append(Node(name, size))
        n = node
        while n:
            n.size += size
            n = n.parent


def find_nodes_under_threshold(node: Node, result: list[Node]) -> None:
    if node.size <= THRESHOLD:
        result.append(node)
    for n in node.nodes:
        find_nodes_under_threshold(n, result)


def find_smallest_node(node: Node, minimum: int) -> int:
    best = 0
    for n in node.nodes:
        size = find_smallest_node(n, minimum)
        if size >= minimum and (not best or size < best):
            best = size
    if node.size >= minimum and (not best or node.size < best):
        best = node.size
    return best


def main() -> None:
    args = setup.parse_command_line(DAY)
    setup.print_banner(DAY, args.part)

    # Read the file
    lines = load.lines(args.input)

    root = Node("/", 0)
    cwd = root

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        i = i + 1

        # Determine what the command is
        if line[0] != "$":
            raise Exception(f"Command expected at line {i}. Found this: {line}")

        command = line[2:]
        if command[:2] == "cd":
            where = command[3:]
            cwd = cd(where, cwd, root)
            if not cwd:
                cwd = root
        elif command == "ls":
            while i < len(lines) and lines[i][0] != "$":
                line = lines[i].strip()
                i = i + 1
                if line[:3] == "dir":
                    add_node(line[4:], cwd, cwd)
                else:
                    match = re.search(r"(\d+)\s+(.+)", line)
                    size = int(match.group(1))
                    name = match.group(2)
                    add_file(name, size, cwd)
        else:
            raise Exception(f"Unknown command at line {i + 1}. Found this: {command}")

    #    draw_file_system(root, '')

    # Part 1 solution
    if args.part == 1:
        result = []
        find_nodes_under_threshold(root, result)

        total = 0
        for r in result:
            total += r.size

        print(f"Result: {total}")

    # Part 2 solution
    if args.part == 2:
        used = root.size
        unused = TOTAL_SPACE - used
        needed = MINIMUM_UNUSED - unused
        best = find_smallest_node(root, needed)
        print(f"Result: {best}")


if __name__ == "__main__":
    main()
