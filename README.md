# Advent of Code 2022

[![CI Status](https://github.com/jambolo/advent-of-code-2022/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/jambolo/advent-of-code-2022/actions/workflows/ci.yml)

Advent of Code solutions for 2022 in Python. The development environment is VS Code and WSL Ubuntu.

## Day 1

| Part | Answer |
|------|--------|
| 1    |  69883 |
| 2    | 207576 |

## Day 2

| Part | Answer |
|------|--------|
| 1    |  12855 |
| 2    |  13726 |

## Day 3

| Part | Answer |
|------|--------|
| 1    |   7875 |
| 2    |   2479 |

## Day 4

| Part | Answer |
|------|--------|
| 1    |    453 |
| 2    |    919 |

## Day 5

| Part |   Answer  |
|------|-----------|
| 1    | QNHWJVJZW |
| 2    | BPCZJLFJW |

## Day 6

| Part | Answer |
|------|--------|
| 1    |   1343 |
| 2    |   2193 |

## Day 7

| Part |  Answer |
|------|---------|
| 1    | 1315285 |
| 2    | 9847279 |

## Day 8

| Part | Answer |
|------|--------|
| 1    |   1713 |
| 2    | 268464 |

## Day 9

| Part | Answer |
|------|--------|
| 1    |   6175 |
| 2    |   2578 |

## Day 10

| Part |  Answer  |
|------|----------|
| 1    |    11720 |
| 2    | ERCREPCJ |

*Part 2 draws the answer as pixels and requires visual inspection of the output.*

## Day 11

| Part |   Answer    |
|------|-------------|
| 1    |       98280 |
| 2    | 17673687232 |

## Day 12

| Part | Answer |
|------|--------|
| 1    |    437 |
| 2    |    430 |

*Part 2 takes about 2 seconds to run.*

## Day 13

| Part | Answer |
|------|--------|
| 1    |   4821 |
| 2    |  21890 |

## Day 14

| Part | Answer |
|------|--------|
| 1    |    655 |
| 2    |  26484 |

## Day 15

| Part |     Answer     |
|------|----------------|
| 1    |        4811413 |
| 2    | 13171855019123 |

*Part 2 takes about 30 seconds to run. Perhaps there is an optimization.*

## Day 16

I revisited this one after a couple years and found a more effective way to solve it using a different approach and more importantly a cache.

| Part | Answer |
|------|--------|
| 1    |   1862 |
| 2    |   2422 |

*Note: Part 2 takes about 15 seconds to run.*

## Day 17

Spent too much time on cleaning up the code.

| Part |     Answer    |
|------|---------------|
| 1    |          3100 |
| 2    | 1540634005751 |

## Day 18

| Part | Answer |
|------|--------|
| 1    |   3526 |
| 2    |   2090 |

## Day 19

I decided to redo this one because it was taking too long. It turned out to be a major effort. The key to this puzzle is branching on the next robot to build rather than every time step and pruning:

  1. If there are already enough of a robot type to supply the resources for building any robot in one turn, then don't build any more of that robot.
  2. If there is enough of a resource to build any robot on each turn until the end, then don't build any more of this robot.
  3. If the maximum possible number of geodes that can be built from a node is less than the best so far, then there is no reason to continue.

I implemented state caching, but the pruning was effective enough to make the cache unnecessary.

| Part | Answer |
|------|--------|
| 1    |   1395 |
| 2    |   2700 |

## Day 20

| Part |     Answer    |
|------|---------------|
| 1    |         14888 |
| 2    | 3760092545849 |

*Note: Part 2 takes about 5 seconds to run.*

## Day 21

| Part |      Answer     |
|------|-----------------|
| 1    | 379578518396784 |
| 2    |   3353687996514 |

## Day 22

| Part | Answer |
|------|--------|
| 1    | 191010 |
| 2    |  55364 |

## Day 23

The original version used lists for everything and it was slow. I replaced coordinates and offsets with tuples and the elves list with a set and the proposed list with a dict. It is much faster now.

| Part | Answer |
|------|--------|
| 1    |   3987 |
| 2    |    938 |

*Note: Part 2 takes about 3 seconds to run.*

## Day 24

| Part | Answer |
|------|--------|
| 1    |    230 |
| 2    |    713 |

*Note: Part 2 takes about 6 seconds to run.*

## Day 25

| Part |        Answer        |
|------|----------------------|
| 1    | 2=001=-2=--0212-22-2 |

## Summary

### Python Language

I don't like Python. It has several features that I consider to be problems. The run-time environment is clunky. The development environment is clunky. I guess it might have value as a scripting language, but I wouldn't use it for any kind application or tool.

### Algorithms and Techniques

A list of notable techniques and algorithms used in the solutions:

| Day |                             Algorithms & Techniques                             |
|-----|---------------------------------------------------------------------------------|
|   4 | Interval/range overlap detection                                                |
|   7 | Tree traversal (DFS), recursive descent parsing                                 |
|  11 | Chinese Remainder Theorem pattern                                               |
|  12 | A* pathfinding, priority queue (min-heap)                                       |
|  15 | Interval merging/normalization, range union                                     |
|  16 | Dijkstra's algorithm, memoization with caching                                  |
|  17 | Cycle detection                                                                 |
|  18 | Flood fill (BFS)                                                                |
|  19 | Branch-and-bound search, pruning heuristics, recursive search with memoization  |
|  21 | Expression trees, recursive evaluation, algebraic equation solving by inversion |
|  24 | Dynamic A\* (A\* with time dimension), priority queue (min-heap)                |
|  25 | Balanced base-5 (SNAFU) number system, radix conversion                         |
