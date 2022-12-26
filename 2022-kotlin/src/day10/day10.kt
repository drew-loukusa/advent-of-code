package day10

import AOC

fun main() {

    data class Instruction(val name: String, val value: Int? = null, val counter: Int)

    fun parseInstructions(input: List<String>): List<Instruction> {
        val instructions = mutableListOf<Instruction>()
        for (line in input){
            val tokens = line.split(' ')
            when (tokens[0]){
                "noop" -> instructions.add(Instruction(name="noop", counter=1))
                "addx" -> {
                    val value = tokens[1].toInt()
                    instructions.add(Instruction(name="addx", value=value, counter=2))
                }
            }
        }
        return instructions.toList()
    }

    fun part1(input: List<String>): Int {
        val signalStrengths = mutableMapOf(20 to 0, 60 to 0, 100 to 0, 140 to 0, 180 to 0, 220 to 0)
        val instructions = parseInstructions(input)
        val itr = instructions.iterator()
        var regX = 1
        var cycleCount = 1 // 1 based indexing, 1st cycle is 1, 2nd cycle is 2 etc
        var curInstructionCounter = 0
        var curInstruction: Instruction? = null

        while (itr.hasNext() || curInstructionCounter > 0) {
            // START CYCLE

            // If not executing an instruction, get a new one
            if (curInstructionCounter == 0 || curInstruction == null) {
                curInstruction = itr.next()
                curInstructionCounter = curInstruction.counter
            }

            // DURING CYCLE

            // if current cycle is notable, calculate signal strength and record it
            if (signalStrengths.containsKey(cycleCount)){
                val strength = cycleCount * regX
                signalStrengths[cycleCount] = strength
            }

            // AFTER CYCLE

            curInstructionCounter -= 1
            if (curInstruction.name == "addx" && curInstructionCounter == 0){
                regX += curInstruction.value!!
            }

            cycleCount += 1
        }

        return signalStrengths.values.sum()
    }

    fun part2(input: List<String>): Int {

        val litPixel = '█'
        val darkPixel = ' '

        val signalStrengths = mutableMapOf(20 to 0, 60 to 0, 100 to 0, 140 to 0, 180 to 0, 220 to 0)
        val instructions = parseInstructions(input)
        val itr = instructions.iterator()
        var regX = 1
        var cycleCount = 1 // 1 based indexing, 1st cycle is 1, 2nd cycle is 2 etc
        var curInstructionCounter = 0
        var curInstruction: Instruction? = null

        while (itr.hasNext() || curInstructionCounter > 0) {
            // START CYCLE

            val cursorPosition = (cycleCount - 1) % 40

            // If not executing an instruction, get a new one
            if (curInstructionCounter == 0 || curInstruction == null) {
                curInstruction = itr.next()
                curInstructionCounter = curInstruction!!.counter
            }

            // DURING CYCLE

            // Check position of sprite
            if (arrayOf(regX - 1, regX, regX + 1).contains(cursorPosition)){
                print(litPixel)
            }
            else print(darkPixel)

            // AFTER CYCLE

            curInstructionCounter -= 1
            if (curInstruction!!.name == "addx" && curInstructionCounter == 0) {
                regX += curInstruction!!.value!!
            }

            if (cycleCount % 40 == 0)
                println()

            cycleCount += 1
        }
        return 0
    }

    // Setup utility class
    //val aoc = AOC(pathFromSrc = "day10", verbose = true)
    val aoc = AOC(pathFromSrc = "day10")

    // TESTS
    aoc.inputFilePath = "input_test"
    aoc.test(::part1, answer = 13140)
    aoc.test(::part2, answer = -1)

    println("--------------------")

    // PARTS 1 & 2
    aoc.inputFilePath = "input"
    //aoc.test(::part1, answer = 14060)
    aoc.test(::part2, answer = -1)

    // Print out test summary (and failures if in verbose mode)
    //aoc.summary()
}
