package day02

import AOC

fun main() {
    fun part1(input: List<String>): Int {
        val shapesToPoints = mapOf("X" to 1, "Y" to 2, "Z" to 3)
        val yoursToTheirs = mapOf("X" to "C", "Y" to "A", "Z" to "B")
        val theirsToYours = mapOf("A" to "Z", "B" to "X", "C" to "Y")

        var yourTotalPoints = 0

        for (gameStr in input){
            val (theirShape, yourShape) = gameStr.split(' ')
            var yourPointsThisRound = shapesToPoints[yourShape]!!

            yourPointsThisRound += if (yoursToTheirs[yourShape] == theirShape) // you win
                6
            else if (theirsToYours[theirShape] == yourShape) // they won
                0
            else  // you tied
                3

            yourTotalPoints += yourPointsThisRound
        }
        return yourTotalPoints
    }

    fun part2(input: List<String>): Int {
        val shapesToPoints = mapOf("A" to 1, "B" to 2, "C" to 3)
        val shapeBeatenBy = mapOf("A" to "C", "B" to "A", "C" to "B")

        var yourTotalPoints = 0


        for (round in input){
            val (theirShape, desiredOutcome) = round.split(' ')
            var yourPointsThisRound = 0

            when (desiredOutcome) {
                "X" -> { // Must lose
                    yourPointsThisRound += 0
                    val losingShape = shapeBeatenBy[theirShape]
                    yourPointsThisRound += shapesToPoints[losingShape]!!
                }
                "Y" -> { // Must draw
                    yourPointsThisRound += 3
                    yourPointsThisRound += shapesToPoints[theirShape]!! // Pick same shape to draw
                }
                "Z" -> { // Must win
                    yourPointsThisRound += 6
                    val losingShape = shapeBeatenBy[theirShape]
                    val winningShape = shapeBeatenBy[losingShape]
                    yourPointsThisRound += shapesToPoints[winningShape]!!
                }
            }
            yourTotalPoints += yourPointsThisRound
        }
        return yourTotalPoints
    }

    // Setup utility class
    val aoc = AOC(pathFromSrc = "day02", verbose=true)

    // TESTS
    aoc.inputFilePath = "input_test"
    aoc.test(::part1, 15)   // 1
    aoc.test(::part2,  12)  // 2

    // PARTS 1 & 2
    aoc.inputFilePath = "input"
    aoc.test(::part1, 13484) // 3
    aoc.test(::part2, 13433) // 4

    // Print out test summary (and failures if in verbose mode)
    aoc.summary()
}
