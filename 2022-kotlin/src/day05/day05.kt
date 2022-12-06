package day05

import AOC
import javax.swing.Box

typealias BoxStacks = MutableList<MutableList<Char>>
typealias Instructions = MutableList<List<Int>>

fun main() {
    fun processInput(input: List<String>): Pair<BoxStacks, Instructions> {
        val itr = input.iterator()
        // Process current state of stacks
        val stacks = mutableListOf<MutableList<Char>>()
        repeat(10) { stacks.add(mutableListOf()) }
        while (itr.hasNext()) {
            val line = itr.next()
            if (line.isEmpty())
                break
            var stackIndex = 1
            val charItr = line.iterator()
            while (charItr.hasNext()){
                // Process 3 chars
                charItr.next()
                val char = charItr.next()
                charItr.next()

                if (charItr.hasNext())
                    charItr.next()
                else{
                    if (char != ' ')
                        stacks[stackIndex].add(0, char)
                    break
                }

                if (char.isDigit())
                    break

                // Add char if not blank
                if (char != ' ')
                    stacks[stackIndex].add(0, char)

                // Move stack index
                stackIndex += 1
            }
        }

        // Process instructions
        val instructions = mutableListOf<List<Int>>()
        while (itr.hasNext()) {
            val line = itr.next()
            instructions.add(
                line.split(' ')
                    .filter { it.toIntOrNull() != null }
                    .map { it.toInt() }
            )
        }
        return stacks to instructions
    }

    fun getTopBoxes(stacks: BoxStacks) = stacks.mapNotNull { it.lastOrNull() }.joinToString("")

    fun part1(input: List<String>): String {
        val (stacks, instructions) = processInput(input)
        for (moveSet in instructions) {
            val (numBoxesToMove, sourceStack, destStack) = moveSet
            repeat(numBoxesToMove) {
                stacks[destStack].add(stacks[sourceStack].removeLast())
            }
        }
        return getTopBoxes(stacks)
    }

    fun part2(input: List<String>): String {
        val (stacks, instructions) = processInput(input)
        for (moveSet in instructions) {
            val (numBoxesToMove, sourceStack, destStack) = moveSet
            val tempStack = mutableListOf<Char>()
            repeat(numBoxesToMove) {
                tempStack.add(0, stacks[sourceStack].removeLast())
            }
            stacks[destStack].addAll(tempStack)
        }
        return getTopBoxes(stacks)
    }

    // Setup utility class
    val aoc = AOC(pathFromSrc = "day05", verbose = true)

    // TESTS
    aoc.inputFilePath = "input_test"
    aoc.test(::part1, answer = "CMZ")
    aoc.test(::part2, answer = "MCD")

    // PARTS 1 & 2
    aoc.inputFilePath = "input"
    aoc.test(::part1, answer = "BWNCQRMDB")
    aoc.test(::part2, answer = "NHWZCBNBF")

    // Print out test summary (and failures if in verbose mode)
    aoc.summary()
}
