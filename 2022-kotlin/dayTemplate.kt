package day{DAY_REPLACE}

import AOC

fun main() {
    fun part1(input: List<String>): Int {
        return 0
    }

    fun part2(input: List<String>): Int {
        return 0
    }

    // Setup utility class
    val aoc = AOC(pathFromSrc = "day{DAY_REPLACE}", verbose = true)

    // TESTS
    aoc.inputFilePath = "input_test"
    aoc.test(::part1, answer = -1)
    aoc.test(::part2, answer = -1)

    // PARTS 1 & 2
    aoc.inputFilePath = "input"
    aoc.test(::part1, answer = -1)
    aoc.test(::part2, answer = -1)

    // Print out test summary (and failures if in verbose mode)
    aoc.summary()
}
