package day09

import AOC
import java.lang.Math.pow

import kotlin.math.exp
import kotlin.math.pow
import kotlin.math.sqrt

fun main() {

    data class Point(var x: Int = 0, var y: Int = 0)

    fun part1(input: List<String>): Int {
        val positions = mutableSetOf(0 to 0)
        val head = Point()
        val tail = Point()
        for (vector in input) {
            val (direction, amountStr) = vector.split(' ')
            val amount = amountStr.toInt()

            // For each increment in AMOUNT
            repeat(amount) {
                // Move head
                when (direction) {
                    "U" -> head.y += 1
                    "D" -> head.y -= 1
                    "R" -> head.x += 1
                    "L" -> head.x -= 1
                }

                // Distance formula
                val dx = (head.x - tail.x).toDouble()
                val dy = (head.y - tail.y).toDouble()
                val distanceAway = sqrt(dx.pow(2) + dy.pow(2))

                // Check if we need to move tail, and move it if needed
                if (distanceAway >= 2) {
                    if (dx > 0) tail.x += 1
                    if (dx < 0) tail.x -= 1
                    if (dy > 0) tail.y += 1
                    if (dy < 0) tail.y -= 1
                    positions.add(tail.x to tail.y)
                }
            }
        }
        return positions.size
    }

    fun part2(input: List<String>): Int {
        val positions = mutableSetOf(0 to 0)
        val rope = MutableList(8) { Point() }
        val head = Point()
        val tail = Point()
        rope.add(0, head); rope.add(tail)
        for (vector in input) {
            val (direction, amountStr) = vector.split(' ')
            val amount = amountStr.toInt()

            // For each increment in AMOUNT
            repeat(amount) {
                // Move head
                when (direction) {
                    "U" -> head.y += 1
                    "D" -> head.y -= 1
                    "R" -> head.x += 1
                    "L" -> head.x -= 1
                }

                for ((i, knot) in rope.withIndex()){
                    if (i == 0) continue
                    val nextKnot = rope[i - 1]
                    // Distance formula
                    val dx = (nextKnot.x - knot.x).toDouble()
                    val dy = (nextKnot.y - knot.y).toDouble()
                    val distanceAway = sqrt(dx.pow(2) + dy.pow(2))

                    // Check if we need to move tail, and move it if needed
                    if (distanceAway >= 2) {
                        if (dx > 0) knot.x += 1
                        if (dx < 0) knot.x -= 1
                        if (dy > 0) knot.y += 1
                        if (dy < 0) knot.y -= 1
                        //if (knot == tail){
                        if (i == rope.size - 1){
                            positions.add(knot.x to knot.y)
                        }
                    }
                }
            }
        }
        return positions.size
    }

    // Setup utility class
    val aoc = AOC(pathFromSrc = "day09", verbose = true)

    // TESTS
    aoc.inputFilePath = "input_test"
    aoc.test(::part1, answer = 13)

    aoc.inputFilePath = "input_test1"
    aoc.test(::part2, answer = 36)

    // PARTS 1 & 2
    aoc.inputFilePath = "input"
    aoc.test(::part1, answer = 6256)
    aoc.test(::part2, answer = 2665)

    // Print out test summary (and failures if in verbose mode)
    aoc.summary()
}
