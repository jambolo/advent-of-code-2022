# Advent of Code 2022
# Day 24

from utils import setup, load
import heapq


DAY = 24

horizontal_blizzards = []
vertical_blizzards = []
maps = []
graphs = []
width = 0
height = 0
start_index = 0
goal_index = 0
t_0 = 0


def replace_at(s, i, c):
    """
    Replaces a portion of a string starting at the given index with another string

    Returns the new string

    s   - string to be replaced
    i   - index to start the replacement
    c   - replacement string
    """
    if i >= 0:
        out = s[:i] + c + s[i + len(c) :]
    else:
        return s[:i] + c + s[len(s) + i + len(c) :]
    return out


def create_map(t):
    global horizontal_blizzards, vertical_blizzards, width, height, t_0

    map = ["." * width for r in range(height)]
    for b in horizontal_blizzards:
        r = b["start"][0]
        c = (b["start"][1] + (t + t_0) * b["d"]) % width
        map[r] = replace_at(map[r], c, "#")
    for b in vertical_blizzards:
        r = (b["start"][0] + (t + t_0) * b["d"]) % height
        c = b["start"][1]
        map[r] = replace_at(map[r], c, "#")
    return map


def print_map(map, i=-1):
    global width, height

    row = "+." + "-" * (width - 1) + "+"
    if i == 0:
        row = replace_at(row, 1, "E")
    print(row)
    eR = (i - 1) // width
    eC = (i - 1) % width
    for r in range(height):
        row = map[r]
        if 0 < i <= height * width and eR == r:
            row = replace_at(row, eC, "E")
        print("|" + row + "|")
    row = "+" + "#" * (width - 1) + ".+"
    if i > width * height:
        row = replace_at(row, width - 2, "E")
    print(row)


def node_index(r, c):
    global width

    return r * width + c + 1


def create_graph(map):
    global width, height, start_index, goal_index

    graph = []

    # Add start node
    node = [start_index]  # Not moving is an option, but it still costs 1
    if map[0][0] != "#":
        node.append(node_index(0, 0))  # Include the only node adjacent to the start node if it is open
    graph.append(node)

    # Add map nodes
    for r in range(height):
        for c in range(width):
            node = []
            for r1, c1 in ((r, c), (r - 1, c), (r, c - 1), (r, c + 1), (r + 1, c)):
                if 0 <= r1 < height and 0 <= c1 < width and map[r1][c1] != "#":
                    node.append(node_index(r1, c1))
            graph.append(node)

    # Add goal node
    node = [goal_index]  # Append the goal node last, index is width*height + 1
    if map[height - 1][width - 1] != "#":
        node.append(node_index(height - 1, width - 1))  # Include the only node adjacent to the goal node if it is open
    graph.append(node)  # Append the goal node last, index is width*height + 1

    # Always able to reach start and goal nodes
    graph[node_index(0, 0)].append(start_index)
    graph[node_index(height - 1, width - 1)].append(goal_index)

    return graph


def h(i):
    global width, height, start_index, goal_index

    if i == start_index:  # start node
        cost = width + height
    elif i == goal_index:  # goal node
        cost = 0
    else:
        r = i // width
        c = i % width
        cost = (width - 1 - c) + (height - 1 - r) + 1
    return cost


def neighbors_of(t, i):
    global maps, graphs

    for j in range(len(graphs), t + 1):
        assert len(maps) == j
        maps.append(create_map(j))
        graph = create_graph(maps[j])
        assert len(graphs) == j
        graphs.append(graph)
    return graphs[t][i]


def dynamic_a_star(start, goal, h, neighbors_of):
    openSet = []
    predecessors = {}
    gScore = set()

    # Initially, only the start node is known.
    heapq.heappush(openSet, (h(start), 0, start))
    gScore.add((0, start))

    while len(openSet) > 0:
        # Get the next node. < 0 indicates a replaced entry
        _, t0, n = openSet[0]
        heapq.heappop(openSet)  # Remove the current node

        # If the goal is reached, then return the path by iteratively looking up the goal's predecessors
        if n == goal:
            path = []
            end = goal
            t = t0
            while t != 0:
                path.insert(0, end)
                t, end = predecessors[(t, end)]
            path.insert(0, start)
            return path

        t1 = t0 + 1
        neighbors = neighbors_of(t1, n)
        for neighbor in neighbors:
            if (t1, neighbor) not in gScore:
                predecessors[(t1, neighbor)] = (
                    t0,
                    n,
                )  # Any path to the neighbor should go through n
                gScore.add((t1, neighbor))
                fScore = t1 + h(neighbor)
                heapq.heappush(openSet, (fScore, t1, neighbor))

    # The open set is empty but goal was never reached. That means that there is no path from start to goal.
    return []


def main() -> None:
    global horizontal_blizzards, vertical_blizzards, width, height, start_index, goal_index, t_0, maps, graphs

    args = setup.parse_command_line(DAY)
    setup.print_banner(DAY, args.part)

    # Read the file.
    lines = []
    lines = load.lines(args.input)

    # Load the blizzards

    width = len(lines[0].rstrip()) - 2
    height = len(lines) - 2
    start_index = 0
    goal_index = width * height + 1

    for r in range(height):
        line = lines[r + 1].rstrip()[1:-1]
        for c in range(width):
            x = line[c]
            if x == "<":
                blizzard = {"start": (r, c), "d": -1}
                horizontal_blizzards.append(blizzard)
            elif x == ">":
                blizzard = {"start": (r, c), "d": 1}
                horizontal_blizzards.append(blizzard)
            elif x == "^":
                blizzard = {"start": (r, c), "d": -1}
                vertical_blizzards.append(blizzard)
            elif x == "v":
                blizzard = {"start": (r, c), "d": 1}
                vertical_blizzards.append(blizzard)
            elif x == ".":
                pass
            else:
                raise Exception("invalid map character")

    maps.append(create_map(0))
    graphs.append(create_graph(maps[0]))

    path = dynamic_a_star(start_index, goal_index, h, neighbors_of)

    if args.part == 1:
        print("Result:", len(path) - 1)

    if args.part == 2:
        first = len(path) - 1
        t_0 = first
        maps = [create_map(0)]
        graphs = [create_graph(maps[0])]
        path = dynamic_a_star(goal_index, start_index, h, neighbors_of)
        second = len(path) - 1
        t_0 = first + second
        maps = [create_map(0)]
        graphs = [create_graph(maps[0])]
        path = dynamic_a_star(start_index, goal_index, h, neighbors_of)
        third = len(path) - 1
        print("Result:", first + second + third)


if __name__ == "__main__":
    main()
