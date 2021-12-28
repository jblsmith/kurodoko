# Kurodoko solver

Contains code to solve a [Kurodoko](https://en.wikipedia.org/wiki/Kuromasu) puzzle.

## Rules

Kurodoko is a type of puzzle published by Nikoli. Like most other puzzles they publish, the fun comes from navigating a combination of local rules and global rules that are simple but which can interact in complex ways.

In this case, the local rules are:

- a cell with a number is a white cell that should "see" (vertically and horizontally) that number of white cells (including itself)
- black cells cannot be adjacent (vertically or horizontally)

And the global rule is:

- all the white cells must be contiguous; i.e., black cells cannot cut off two regions of the grid.

## How to use

TODO

To run the website and solve a puzzle, run `bash run.sh`.

## How it works

TODO