package day04

import AOC

fun main() {

    data class Range(val start: Int, val end: Int)

    fun parseRanges(assA: String, assB: String): Pair<Range, Range> {
        var foo = assA.split('-').map { it.toInt() }
        var bar = assB.split('-').map { it.toInt() }

        val fooSize = foo[1] - foo[0]
        val barSize = bar[1] - bar[0]

        if (bar[0] < foo[0] || (bar[0] == foo[0] && barSize > fooSize))
            foo = bar.also { bar = foo }

        return Range(foo[0], foo[1]) to Range(bar[0], bar[1])
    }

    fun part1(input: List<String>): Int {
        var fullyContainedAssCount = 0
        for ((assA, assB) in input.map { it.split(',')}){
            val (a, b) = parseRanges(assA, assB)
            if (a.start <= b.start){
                if (a.end >= b.end)
                    fullyContainedAssCount += 1
            }
        }
        return fullyContainedAssCount
    }

    fun part2(input: List<String>): Int {
        var overlapAssCount = 0
        for ((assA, assB) in input.map { it.split(',')}){
            val (a, b) = parseRanges(assA, assB)
            if (a.start <= b.start){
                if (a.end >= b.end || // a fully contains b
                    a.end >= b.start) // partial overlap
                    overlapAssCount += 1
            }
        }
        return overlapAssCount
    }

    // Setup utility class
    val aoc = AOC(pathFromSrc = "day04", verbose = true)

    // TESTS
    aoc.inputFilePath = "input_test"
    aoc.test(::part1, answer = 2)
    aoc.test(::part2, answer = 4)

    // PARTS 1 & 2
    aoc.inputFilePath = "input"
    aoc.test(::part1, answer = 475)
    aoc.test(::part2, answer = 825)

    // Print out test summary (and failures if in verbose mode)
    aoc.summary()
}
