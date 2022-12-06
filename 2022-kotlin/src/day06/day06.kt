package day06

import AOC

fun main() {
    fun slidingWindow(dataStream: String, windowSize: Int): Int {
        val window = mutableListOf<Char>()
        val charToCount = mutableMapOf<Char, Int>().withDefault { 0 }
        val itr = dataStream.iterator().withIndex()
        var markerIndex = -1
        while (itr.hasNext()){
            val (index, char) = itr.next()
            if (window.size == windowSize && charToCount.size != windowSize) {
                val leftChar = window.removeAt(0)
                charToCount[leftChar] = charToCount.getValue(leftChar) - 1
                if (charToCount[leftChar] == 0) {
                    charToCount.remove(leftChar)
                }
            }
            if (window.size < windowSize) {
                window.add(char)
                charToCount[char] = charToCount.getValue(char) + 1
            }
            if (window.size == windowSize && charToCount.size == windowSize){
                markerIndex = index + 1
                break
            }
        }
        return markerIndex
    }

    fun part1(input: List<String>): Int {
        return slidingWindow(input[0], 4)
    }

    fun part2(input: List<String>): Int {
        return slidingWindow(input[0], 14)
    }

    // Setup utility class
    val aoc = AOC(pathFromSrc = "day06", verbose = true)

    // TESTS
    aoc.inputFilePath = "input_test"
    aoc.test(::part1, answer = 5)
    aoc.test(::part2, answer = 23)

    aoc.inputFilePath = "input_test1"
    aoc.test(::part1, answer = 6)
    aoc.test(::part2, answer = 23)

    aoc.inputFilePath = "input_test2"
    aoc.test(::part1, answer = 10)
    aoc.test(::part2, answer = 29)

    aoc.inputFilePath = "input_test3"
    aoc.test(::part1, answer = 11)
    aoc.test(::part2, answer = 26)

    aoc.inputFilePath = "input_test4"
    aoc.test(::part1, answer = 7)
    aoc.test(::part2, answer = 19)

    // PARTS 1 & 2
    aoc.inputFilePath = "input"
    aoc.test(::part1, answer = 1175)
    aoc.test(::part2, answer = 3217)

    // Print out test summary (and failures if in verbose mode)
    aoc.summary()
}
