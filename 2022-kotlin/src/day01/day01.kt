package day01

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
        val top3 = MutableList(0) { it }
        repeat(3) {
            top3.add(caloriesMaxHeap.poll())
        }
        return top3.sum()
    }

    val testInput = readInput("day01_test")
    val input = readInput("day01")

    check(part1(testInput) == 24000)
    val p1 = part1(input)
    check(p1 == 71924)
    println(p1)

    check(part2(testInput) == 45000)
    val p2 = part2(input);
    check(p2 == 210406)
    println(part2(input))
}
