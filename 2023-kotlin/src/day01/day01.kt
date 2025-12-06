package day01

import AOC

fun main() {

    fun findNumber(line: String): Int {
        var firstDigit: Char = ' '
        var lastDigit: Char = ' '
        line.forEach {
            if (firstDigit == ' ' && it.isDigit()){
                firstDigit = it
                lastDigit = it
            }
            else if (it.isDigit()) {
                lastDigit = it
            }
        }

        assert(firstDigit != ' ')
        assert(lastDigit != ' ')

        return "$firstDigit$lastDigit".toInt()
    }

    // Recognizing a digit
    //  If is digit char, DONE
    //  If is letter char
    //      Could just start accumulating chars
    //          Issue: If you don't start with valid char (z is not start of any number word) you won't see valid words)
    //      If is not start of number word, throw out of window
    //      If is start of number word, enter accumulation mode

    data class NumberWordParseResult(val charsConsumed: Int, val digit: Char?)

    fun parseNumberWord(line: String, index: Int, wordToParse: String): NumberWordParseResult {
        var curWord = ""
        var wordIndex = 0
        var charsConsumed = 0
        var curIndex = index
        while (wordIndex < wordToParse.length && curIndex < line.length) {

            val curChar = line[curIndex]
            val wordChar = wordToParse[wordIndex]

            if (curChar != wordChar)
                return NumberWordParseResult(charsConsumed, null)

            curWord += curChar

            wordIndex += 1
            curIndex += 1
            charsConsumed += 1
        }

        val digit = when (curWord) {
            "one" -> '1'
            "two" -> '2'
            "three" -> '3'
            "four" -> '4'
            "five" -> '5'
            "six" -> '6'
            "seven" -> '7'
            "eight" -> '8'
            "nine" -> '9'
            else -> ' '
        }

        assert(digit != ' ')

        return NumberWordParseResult(charsConsumed, digit)
    }

    fun findNumberV2(line: String): Int {
        var firstDigit: Char = ' '
        var lastDigit: Char = ' '
        line.withIndex().forEach { (index, curChar) ->

            var curDigit = ' '
            if (curChar.isDigit()) {
                curDigit = curChar
            }

            else if (curChar.isLetter()) {
                var result = NumberWordParseResult(1, null)
                when (curChar) {
                    'o' -> {
                        result = parseNumberWord(line, index, "one")
                    }
                    't' -> {
                        val a = parseNumberWord(line, index, "two")
                        val b = parseNumberWord(line, index, "three")
                        result = if (a.digit != null) a else b
                    }
                    'f' -> {
                        val a = parseNumberWord(line, index, "four")
                        val b = parseNumberWord(line, index, "five")
                        result = if (a.digit != null) a else b
                    }
                    's' -> {
                        val a = parseNumberWord(line, index, "six")
                        val b = parseNumberWord(line, index, "seven")
                        result = if (a.digit != null) a else b
                    }
                    'e' -> {
                        result = parseNumberWord(line, index, "eight")
                    }
                    'n' -> {
                        result = parseNumberWord(line, index, "nine")
                    }
                }
                if (result.digit != null) {
                    curDigit = result.digit!!
                }
            }

            if (curDigit != ' ') {
                if (firstDigit == ' '){
                    firstDigit = curDigit
                }
                lastDigit = curDigit
            }
        }

        assert(firstDigit != ' ')
        assert(lastDigit != ' ')

        return "$firstDigit$lastDigit".toInt()
    }

    fun part1(input: List<String>): Int =
        input.fold(initial = 0) { acc, line ->
            acc + findNumber(line)
        }

    fun part2(input: List<String>): Int =
        input.fold(initial = 0) { acc, line ->
        acc + findNumberV2(line)
    }
    // Setup utility class
    val aoc = AOC(pathFromSrc = "day01", verbose = true)

    // TESTS
     aoc.inputFilePath = "input_test"
     aoc.test(::part1, answer = 142)
     aoc.inputFilePath = "input_test2"
     aoc.test(::part2, answer = 281)

    // PARTS 1 & 2
    aoc.inputFilePath = "input"
    aoc.test(::part1, answer = 54601)
    aoc.test(::part2, answer = -1)

    // Print out test summary (and failures if in verbose mode)
    aoc.summary()
}
