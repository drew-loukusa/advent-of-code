package day03

import AOC

fun main() {

    fun priorityOf(char: Char): Int {
        if (char.isLowerCase()){
            return char.code - 96
        }
        return char.code - 38
    }

    fun part1(input: List<String>): Int {
        var prioritySum = 0
        for (rucksack in input){
            val middle = rucksack.length / 2
            val compartmentA = rucksack.substring(0 until middle).toSet()
            val compartmentB = rucksack.substring(middle).toSet()
            val commonChar = compartmentA.intersect(compartmentB).random() // Should only be 1 item
            prioritySum += priorityOf(commonChar)
        }
        return prioritySum
    }

    fun part2(input: List<String>): Int {
        val itr = input.iterator()
        var groupPriorityTypeSum = 0
        while (itr.hasNext()) {
            val sackSets = mutableListOf<Set<Char>>()
            repeat(3) {
                sackSets.add(itr.next().toSet())
            }
            val foo = sackSets[0].intersect(sackSets[1])
            val bar = sackSets[1].intersect(sackSets[2])
            groupPriorityTypeSum += priorityOf(foo.intersect(bar).random())
        }
        return groupPriorityTypeSum
    }

    // Setup utility class
    val aoc = AOC(pathFromSrc = "day03", verbose = true)

    // TESTS
    aoc.inputFilePath = "input_test"
    aoc.test(::part1, answer = 157)
    aoc.test(::part2, answer = 70)

    // PARTS 1 & 2
    aoc.inputFilePath = "input"
    aoc.test(::part1, answer = 7811)
    aoc.test(::part2, answer = 2639)

    // Print out test summary (and failures if in verbose mode)
    aoc.summary()
}
