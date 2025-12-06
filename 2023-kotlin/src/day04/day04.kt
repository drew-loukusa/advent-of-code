package day04

import AOC
import java.lang.Math.pow
import kotlin.math.pow

fun main() {

    data class ScratchCard(val id: Int, val winningNums: Set<Int>, val possessedNums: Set<Int>)

    fun parseNums (numStr: String) =
        numStr.trim()
            .split(' ')
            .filter { it != "" }
            .map { it.toInt() }
            .toSet() // NOTE: ASSUMING NUMS ARE UNIQUE per side of |

    fun processInput(input: List<String>): List<ScratchCard> {
        val cards = mutableListOf<ScratchCard>()
        input.forEach { line ->
            val (left, right) = line.split('|')
            val (idStr, winningNumStr) = left.trim().split(':')
            val id = idStr.split(' ').filter { it != "" }[1].toInt()
            val winningNums = parseNums(winningNumStr)
            val possessedNums = parseNums(right)
            cards.add(ScratchCard(id, winningNums, possessedNums))
        }
        return cards
    }

    fun part1(input: List<String>): Int {
        val cards = processInput(input)

        return cards.fold(0) { cardsTotal, card ->
            val overlap = card.winningNums.intersect(card.possessedNums).size
            cardsTotal + 2.0.pow((overlap - 1)).toInt()
        }
    }

    fun part2(input: List<String>): Int {
        val cards = processInput(input).toMutableList()
        val cardsMap = mutableMapOf<Int, ScratchCard>()

        cards.withIndex().forEach { (i, card) ->
            cardsMap[i + 1] = card
        }


        var i = 0
        while (i < cards.size) {
            val card = cards[i]
            val overlap = card.winningNums.intersect(card.possessedNums).size
            (card.id + 1..card.id + overlap).forEach {
                if (it <= cardsMap.size) {
                    cards.add(cardsMap[it]!!)
                }
            }
            i += 1
        }

        return cards.size
    }

    // Setup utility class
    val aoc = AOC(pathFromSrc = "day04", verbose = true)

    // TESTS
    aoc.inputFilePath = "input_test"
    aoc.test(::part1, answer = 13)
    aoc.test(::part2, answer = 30)

    // PARTS 1 & 2
    aoc.inputFilePath = "input"
    aoc.test(::part1, answer = 32001)
    aoc.test(::part2, answer = 5037841)

    // Print out test summary (and failures if in verbose mode)
    aoc.summary()
}
