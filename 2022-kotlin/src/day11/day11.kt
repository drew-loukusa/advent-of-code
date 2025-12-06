package day11

import AOC
import java.math.BigInteger

fun main() {

    class Expression(expressionStr: String) {
        val lhs: String
        val rhs: String
        val op: (a: BigInteger, b: BigInteger) -> BigInteger

        init {
            val tokens = expressionStr.split(' ').filter { it.isNotEmpty() }
            val lhs = tokens[3]
            val op = tokens[4]
            val rhs = tokens[5]
            this.op = if (op == "*") {
                fun(a: BigInteger, b: BigInteger): BigInteger { return a * b }
            } else fun(a: BigInteger, b: BigInteger): BigInteger { return a + b }
            this.rhs = rhs
            this.lhs = lhs
        }

        fun run(old: BigInteger): BigInteger {
            val a = if (lhs == "old") old else lhs.toBigInteger()
            val b = if (rhs == "old") old else rhs.toBigInteger()
            val res = op(a, b)
            return res
        }
    }
    class Test(testStr: String, trueStr: String, falseStr: String){
        val divisor = testStr.split(' ').filter {it.isNotEmpty() }[3].toBigInteger()
        val throwToIfTrue = trueStr.split(' ').filter {it.isNotEmpty() }[5].toInt()
        val throwToIfFalse = falseStr.split(' ').filter {it.isNotEmpty() }[5].toInt()
        fun run(worryValue: BigInteger): Int {
            return if (worryValue % divisor == 0.toBigInteger()) throwToIfTrue else throwToIfFalse
        }
    }
    data class Monkey(
        val items: MutableList<BigInteger>,
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
                .map { it.trim(',').toBigInteger() }
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
                    newWorryValue /= 3.toBigInteger()
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
            .slice(0..2)
        return topCounts[0] * topCounts[1]
    }

    fun part2(input: List<String>): BigInteger {
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
            println("Round: $round")
            round += 1
        }
        val topCounts = itemsCounted.values
            .sorted()
            .reversed()
            //.slice(0..1)
        return topCounts[0].toBigInteger() * topCounts[1].toBigInteger()
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
    // You're getting very large numbers, and they are overflowing standard data types (even longs)
    // You tried using BigInteger, but it just slows to a crawl; Ya gotta get clever.
    // Thoughts so far:
    // * If there is a cycle, (what defines a cycle in this instance?)
    //   then we could grab the value for the cycle and extrapolate the answer
    //
    //   The more I think about this the more I think we'll have to extrapolate the answer
    //   I suspect the time it takes to do each N cycles will probably increase exponentially
    //
    // * We could store values as 2 parts, part a: VALUE % 1000, part b: N * 1000
    //   Probably would need to make N very large, and
    //   sort out how to do math on a composite number

    // 125 / 10 = 12
    // 125 % 10 = 5

    // 125 * 277 = 34625
    // 125 + 277 = 402

    // (% 10, 277) -> (27, 7)
    // (% 10, 125) -> (12, 5)

    // (% 10, 402) -> (40, 2)
    // (% 10, 34625) -> (3462, 5)


    aoc.test(::part2, answer = -1)

    aoc.summary()
}

