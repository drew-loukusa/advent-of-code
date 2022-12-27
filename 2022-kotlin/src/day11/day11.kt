package day11

import AOC

fun main() {

    class Expression(expressionStr: String) {
        val lhs: String
        val rhs: String
        val op: (a: ULong, b: ULong) -> ULong

        init {
            val tokens = expressionStr.split(' ').filter { it.isNotEmpty() }
            val lhs = tokens[3]
            val op = tokens[4]
            val rhs = tokens[5]
            this.op = if (op == "*") {
                fun(a: ULong, b: ULong): ULong { return a * b }
            } else fun(a: ULong, b: ULong): ULong { return a + b }
            this.rhs = rhs
            this.lhs = lhs
        }

        fun run(old: ULong): ULong {
            val a = if (lhs == "old") old else lhs.toULong()
            val b = if (rhs == "old") old else rhs.toULong()
            val res = op(a, b)
            return res
        }
    }
    class Test(testStr: String, trueStr: String, falseStr: String){
        val divisor = testStr.split(' ').filter {it.isNotEmpty() }[3].toULong()
        val throwToIfTrue = trueStr.split(' ').filter {it.isNotEmpty() }[5].toInt()
        val throwToIfFalse = falseStr.split(' ').filter {it.isNotEmpty() }[5].toInt()
        fun run(worryValue: ULong): Int {
            return if (worryValue % divisor == 0UL) throwToIfTrue else throwToIfFalse
        }
    }
    data class Monkey(
        val items: MutableList<ULong>,
        val expression: Expression,
        val test: Test,
    )

    fun parseInputToMonkeys(input: List<String>): List<Monkey>{
        val monkeys = mutableListOf<Monkey>()
        val itr = input.iterator()
        val curMonkey = 0
        while (itr.hasNext()) {
            itr.next() // Skip Monkey N line
            val itemsTokens = itr.next().split(' ').filter { it.isNotEmpty() }
            val items = itemsTokens
                .slice(2 until itemsTokens.size)
                .map { it.trim(',').toULong() }
                .toMutableList()

            val expStr = itr.next()
            val testStr = itr.next()
            val trueStr = itr.next()
            val falseStr = itr.next()

            val monkey = Monkey(
                items,
                Expression(expStr),
                Test(testStr, trueStr, falseStr)
            )
            monkeys.add(monkey)
            if (itr.hasNext()) itr.next() // Skip blank line
        }
        return monkeys.toList()
    }

    fun part1(input: List<String>): Int {
        val roundsToRun = 20
        val monkeys = parseInputToMonkeys(input)
        val itemsCounted = mutableMapOf<Int, Int>()
        var round = 1
        repeat(roundsToRun) {
            for ((i, monkey) in monkeys.withIndex()){
                while (monkey.items.isNotEmpty()){
                    val worryValue = monkey.items.removeAt(0)
                    var newWorryValue = monkey.expression.run(worryValue)
                    newWorryValue /= 3UL
                    val monkeyToThrowTo = monkey.test.run(newWorryValue)
                    monkeys[monkeyToThrowTo].items.add(newWorryValue)
                    if (!itemsCounted.containsKey(i)){
                        itemsCounted[i] = 0
                    }
                    itemsCounted[i] = itemsCounted[i]!! + 1
                }
            }
            print('-')
            round += 1
        }
        val topCounts = itemsCounted.values
            .sorted()
            .reversed()
            .slice(0..2)
        return topCounts[0] * topCounts[1]
    }

    fun part2(input: List<String>): ULong {
        val roundsToRun = 10000
        val monkeys = parseInputToMonkeys(input)
        val itemsCounted = mutableMapOf<Int, Int>()
        var round = 1
        repeat(roundsToRun) {
            for ((i, monkey) in monkeys.withIndex()){
                while (monkey.items.isNotEmpty()){
                    val worryValue = monkey.items.removeAt(0)
                    val newWorryValue = monkey.expression.run(worryValue)
                    val monkeyToThrowTo = monkey.test.run(newWorryValue)
                    monkeys[monkeyToThrowTo].items.add(newWorryValue)
                    if (!itemsCounted.containsKey(i)){
                        itemsCounted[i] = 0
                    }
                    itemsCounted[i] = itemsCounted[i]!! + 1
                }
            }
            round += 1
        }
        val topCounts = itemsCounted.values
            .sorted()
            .reversed()
            //.slice(0..1)
        return topCounts[0].toULong() * topCounts[1].toULong()
    }

    // Setup utility class
    val aoc = AOC(pathFromSrc = "day11", verbose = true)

    // TESTS
    aoc.inputFilePath = "input_test"
    aoc.test(::part1, answer = 10605)
    aoc.test(::part2, answer = 2713310158)

    // PARTS 1 & 2
    aoc.inputFilePath = "input"
    aoc.test(::part1, answer = 64032)
    aoc.test(::part2, answer = -1)

    aoc.summary()
}

