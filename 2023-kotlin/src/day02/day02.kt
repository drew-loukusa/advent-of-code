package day02

import AOC

data class CubePulls(val red: Int = 0, val green: Int = 0, val blue: Int = 0)

fun CubePulls.pullIsPossible(other: CubePulls): Boolean {
    return this.red >= other.red && this.green >= other.green && this.blue >= other.blue
}

typealias Bag = CubePulls

data class Game(val id: Int, val pulls: List<CubePulls>)

fun processInput(input: List<String>): List<Game> {
    val games = mutableListOf<Game>()
    input.forEach { line ->
        val (left, right) = line.split(':')
        val (_, idStr) = left.split(' ')
        val id = idStr.toInt()
        val phaseStrs = right.split(';')
        val phases = mutableListOf<CubePulls>()
        phaseStrs.forEach {
            val cubePullStrs = it.split(',')
            var (red, green, blue) = listOf(0, 0, 0)
            cubePullStrs.forEach { chunk ->
                val (numPulledStr, color) = chunk.trim().split(' ')
                val numPulled = numPulledStr.toInt()
                when (color) {
                    "red" -> red = numPulled
                    "blue" -> blue = numPulled
                    "green" -> green = numPulled
                }
            }
            phases.add(CubePulls(red, green, blue))
        }
        games.add(Game(id, phases))
    }
    return games
}

fun main() {
    fun part1(input: List<String>): Int {
        val games: List<Game> = processInput(input)
        val bag = Bag(red = 12, green = 13, blue = 14)

        val idSum = games.fold(0) { idSum, game ->
            val pullsPossible = game.pulls.fold(0) { validPulls, cubePull ->
                if (bag.pullIsPossible(cubePull)) validPulls + 1 else validPulls
            }

            if (pullsPossible == game.pulls.size) idSum + game.id else idSum
        }

        return idSum
    }

    fun part2(input: List<String>): Int {
        val games: List<Game> = processInput(input)
        val minForEachGame = mutableListOf<Bag>()

        games.forEach { game ->
            var (red, green, blue) = listOf(0,0,0)
            game.pulls.forEach { pull ->
                if (pull.red > red) red = pull.red
                if (pull.green > green) green = pull.green
                if (pull.blue > blue) blue = pull.blue
            }
            minForEachGame.add(Bag(red, green, blue))
        }

        return minForEachGame.fold(0) { acc, bag ->
            acc + (bag.red * bag.green * bag.blue)
        }
    }

    // Setup utility class
    val aoc = AOC(pathFromSrc = "day02", verbose = true)

    // TESTS
    aoc.inputFilePath = "input_test"
    aoc.test(::part1, answer = 8)
    aoc.test(::part2, answer = 2286)

    // PARTS 1 & 2
    aoc.inputFilePath = "input"
    aoc.test(::part1, answer = 2105)
    aoc.test(::part2, answer = 72422)

    // Print out test summary (and failures if in verbose mode)
    aoc.summary()
}
