package day01

import AOC
import readInput
import java.util.*
import kotlin.math.max

fun main() {
    fun part1(input: List<String>): Int {
        var curMaxCalories = 0
        var curElfCalories = 0
        input.forEach {
            if (it.isNotEmpty())
                curElfCalories += it.toInt()
            if (it.isEmpty()){
                curMaxCalories = max(curMaxCalories, curElfCalories)
                curElfCalories = 0
            }
        }
        return curMaxCalories
    }

    fun part2(input: List<String>): Int {
        val caloriesMaxHeap = PriorityQueue<Int>(3, Collections.reverseOrder())
        var curElfCalories = 0
        val itr = input.iterator()
        while (itr.hasNext()){
            val cals = itr.next()
            if (cals.isNotEmpty())
                curElfCalories += cals.toInt()
            if (cals.isEmpty() || !itr.hasNext()) {
                caloriesMaxHeap.add(curElfCalories)
                curElfCalories = 0
            }
        }
        val top3 = mutableListOf<Int>()
        repeat(3) {
            top3.add(caloriesMaxHeap.poll())
        }
        return top3.sum()
    }

    // Setup utility class
    val aoc = AOC(verbose=true)

    // TESTS
    aoc.inputFilePath = "day01_test"
    aoc.test(::part1, 24000)
    aoc.test(::part2,  45000)

    // PARTS 1 & 2
    aoc.inputFilePath = "day01"
    aoc.test(::part1, 71924)
    aoc.test(::part2, 210406)

    // Print out test summary (and failures if in verbose mode)
    aoc.summary()
}
