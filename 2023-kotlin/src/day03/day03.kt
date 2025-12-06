package day03

import AOC
import kotlin.math.max
import kotlin.math.min

fun main() {

    val validSymbols = Regex("[^(.|\\d)]")

    fun part1(input: List<String>): Int {

        // Walk string until you see a valid symbol [^.]: If you see one enter SEARCH MODE:
        //  Examine each square around the current char in a 3 x 3, where the symbol is in the middle
        //  If any char in the surrounding 3 x 3 grid is a digit, parse that number (enter PARSE_NUMBER mode):
        //          If number is centered over a symbol like this:
        //
        //                      1234567
        //                         *
        //          Then how do you parse it? We could have a rule where we always walk left
        //          as far as possible, then also parse going right.
        //
        //          To prevent a number being parsed multiple times, we can store the coordinates
        //          of each digit in a set called "parsedDigitsCoords" or something
        //          and if we find a digit in the set skip entering PARSE_NUMBER mode
        //          NOTE: the set is only valid for any given symbol
        //
        //          Question: If a number is adjacent to 2 or more symbols, should it be counted
        //                      multiple times?
        //          I'll leave my code alone, assuming the answer is yes. Part 1 passes anyways.

        val (MIN_X, MAX_X) = listOf(0, input[0].length - 1)
        val (MIN_Y, MAX_Y) = listOf(0, input.size - 1)

        var partCountSum = 0

        // The nesting here is a bit much, but it works

        // Walk over each char in grid
        input.withIndex().forEach { (y, line) ->
            line.withIndex().forEach { (x, char) ->
                if (validSymbols.matches(char.toString())) {

                    // Build a list of points to analyze
                    val xRange: IntRange = max(MIN_X, x - 1)..min(x + 1, MAX_X)
                    val yRange: IntRange = max(MIN_Y, y - 1)..min(y + 1, MAX_Y)

                    val numCoordSet = mutableSetOf<Pair<Int, Int>>()

                    // Examine 3 x 3 grid around current symbol
                    yRange.forEach { ys ->
                        xRange.forEach { xs ->
                            val curChar = input[ys][xs]

                            // If we find digit, parse number
                            if (curChar.isDigit() && !numCoordSet.contains(ys to xs)) {
                                numCoordSet.add(ys to xs)
                                // GO LEFT
                                var numStr = input[ys][xs].toString()
                                var leftI = xs - 1
                                while (leftI >= MIN_X && input[ys][leftI].isDigit()) {
                                    numCoordSet.add(ys to leftI)
                                    numStr = input[ys][leftI] + numStr
                                    leftI -= 1
                                }
                                // GO RIGHT
                                var rightI = xs + 1
                                while (rightI <= MAX_X && input[ys][rightI].isDigit()) {
                                    numCoordSet.add(ys to rightI)
                                    numStr += input[ys][rightI]
                                    rightI += 1
                                }

                                partCountSum += numStr.toInt()
                            }
                        }
                    }
                }
            }
        }

        return partCountSum
    }

    fun part2(input: List<String>): Int {
        // Walk string until you see a valid symbol [^.]: If you see one enter SEARCH MODE:
        //  Examine each square around the current char in a 3 x 3, where the symbol is in the middle
        //  If any char in the surrounding 3 x 3 grid is a digit, parse that number (enter PARSE_NUMBER mode):
        //          If number is centered over a symbol like this:
        //
        //                      1234567
        //                         *
        //          Then how do you parse it? We could have a rule where we always walk left
        //          as far as possible, then also parse going right.
        //
        //          To prevent a number being parsed multiple times, we can store the coordinates
        //          of each digit in a set called "parsedDigitsCoords" or something
        //          and if we find a digit in the set skip entering PARSE_NUMBER mode
        //          NOTE: the set is only valid for any given symbol
        //
        //          Question: If a number is adjacent to 2 or more symbols, should it be counted
        //                      multiple times?
        //          I'll leave my code alone, assuming the answer is yes. Part 1 passes anyways.

        val (MIN_X, MAX_X) = listOf(0, input[0].length - 1)
        val (MIN_Y, MAX_Y) = listOf(0, input.size - 1)

        var gearRatioSum = 0

        // The nesting here is a bit much, but it works

        // Walk over each char in grid
        input.withIndex().forEach { (y, line) ->
            line.withIndex().forEach { (x, char) ->
                if (char == '*') {

                    // Build a list of points to analyze
                    val xRange: IntRange = max(MIN_X, x - 1)..min(x + 1, MAX_X)
                    val yRange: IntRange = max(MIN_Y, y - 1)..min(y + 1, MAX_Y)

                    val numCoordSet = mutableSetOf<Pair<Int, Int>>()

                    // Examine 3 x 3 grid around current symbol

                    val numbersFound = mutableListOf<Int>()

                    yRange.forEach { ys ->
                        xRange.forEach { xs ->
                            val curChar = input[ys][xs]

                            // If we find digit, parse number
                            if (curChar.isDigit() && !numCoordSet.contains(ys to xs)) {
                                numCoordSet.add(ys to xs)
                                // GO LEFT
                                var numStr = input[ys][xs].toString()
                                var leftI = xs - 1
                                while (leftI >= MIN_X && input[ys][leftI].isDigit()) {
                                    numCoordSet.add(ys to leftI)
                                    numStr = input[ys][leftI] + numStr
                                    leftI -= 1
                                }
                                // GO RIGHT
                                var rightI = xs + 1
                                while (rightI <= MAX_X && input[ys][rightI].isDigit()) {
                                    numCoordSet.add(ys to rightI)
                                    numStr += input[ys][rightI]
                                    rightI += 1
                                }

                                numbersFound.add(numStr.toInt())
                            }
                        }
                    }

                    if (numbersFound.size == 2) {
                        gearRatioSum += numbersFound[0] * numbersFound[1]
                    }
                }
            }
        }

        return gearRatioSum
    }

    // Setup utility class
    val aoc = AOC(pathFromSrc = "day03", verbose = true)

    // TESTS
    aoc.inputFilePath = "input_test"
    aoc.test(::part1, answer = 4361)
    aoc.test(::part2, answer = 467835)

    // PARTS 1 & 2
    aoc.inputFilePath = "input"
    aoc.test(::part1, answer = 540025)
    aoc.test(::part2, answer = 84584891)

    // Print out test summary (and failures if in verbose mode)
    aoc.summary()
}
