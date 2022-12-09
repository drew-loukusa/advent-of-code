package day08

import AOC
import java.lang.Integer.max

fun main() {


    fun part1(input: List<String>): Int {
        var visibleTrees = (input.size * 4) - 4
        val countedTrees = mutableSetOf<Pair<Int, Int>>()


        fun countVisibleTreesInRows(
            rows: List<String>,
            countedTrees: MutableSet<Pair<Int, Int>>,
            isTransposed: Boolean = false
        ): Int {
            val maxXIndex = input[0].length - 1
            var treesThatCanBeSeen = 0
            for ((y, row) in rows.withIndex()) {
                // Skip first and last rows (they're the outside rows and are always visible)
                if (y == 0 || y == input.size - 1) continue
                // Little closure to process the row
                fun processRow(curRow: String, reverseRow: Boolean = false) {
                    var x = 0
                    var stepTree = curRow[x]
                    while (x + 1 < maxXIndex) {
                        // bit messy, but it works
                        val xCoord = if (reverseRow) (maxXIndex - (x + 1)) else (x + 1)
                        val coords = if (isTransposed) (xCoord to y) else (y to xCoord)
                        val nextTree = curRow[x + 1]
                        if (nextTree > stepTree) {
                            if (!countedTrees.contains(coords)){
                                treesThatCanBeSeen += 1
                                // make sure track which trees we've already counted
                                // so we don't count them twice :)
                                countedTrees.add(coords)
                            }
                            stepTree = nextTree
                        }
                        x += 1
                    }
                }
                processRow(row)
                // Reverse the row, and we can re-use the same
                // logic for walking east to west as west to east
                processRow(row.reversed(), reverseRow = true)
            }
            return treesThatCanBeSeen
        }

        visibleTrees += countVisibleTreesInRows(input, countedTrees)

        // Transpose the input, and then we can re-use the same logic for walking
        // the matrix horizontally for the vertical walking
        val transposedInput = mutableListOf<String>()
        repeat(input.size) { transposedInput.add("") }
        for (row in input) {
            for ((x, char) in row.withIndex()) {
                transposedInput[x] = transposedInput[x] + char
            }
        }

        visibleTrees += countVisibleTreesInRows(transposedInput, countedTrees, true)

        return visibleTrees
    }

    fun part2(input: List<String>): Int {
        val maxXIndex = input[0].length - 1
        val maxYIndex = input.size - 1
        var maxScenicScore = 0
        for ((y, row) in input.withIndex()){
            if (y == 0 || y == input.size - 1) continue
            for ((x, tree) in row.withIndex()){
                if (x == 0 || x == row.length -1) continue
                // look in 4 dirs, calc scenic score
                // walk up
                var curY = y - 1
                var upScenicScore = 0
                while (curY >= 0){
                    if (curY < 0) break
                    val nextTree = input[curY][x]
                    if (nextTree < tree){
                        upScenicScore += 1
                        curY -= 1
                    }
                    else {
                        upScenicScore += 1
                        break
                    }
                }
                // walk right
                var curX = x + 1
                var rightScenicScore = 0
                while (curX <= maxXIndex){
                    if (curX > maxXIndex) break
                    val nextTree = input[y][curX]
                    if (nextTree < tree){
                        rightScenicScore += 1
                        curX += 1
                    }
                    else {
                        rightScenicScore += 1
                        break
                    }
                }
                // walk down
                curY = y + 1
                var downScenicScore = 0
                while (curY <= maxYIndex){
                    if (curY > maxYIndex) break
                    val nextTree = input[curY][x]
                    if (nextTree < tree){
                        downScenicScore += 1
                        curY += 1
                    }
                    else {
                        downScenicScore += 1
                        break
                    }
                }
                // walk left
                curX = x - 1
                var leftScenicScore = 0
                while (curX >= 0){
                    if (curX < 0) break
                    val nextTree = input[y][curX]
                    if (nextTree < tree){
                        leftScenicScore += 1
                        curX -= 1
                    }
                    else {
                        leftScenicScore += 1
                        break
                    }
                }
                val curTreeScenicScore = upScenicScore * downScenicScore * leftScenicScore * rightScenicScore
                maxScenicScore = max(maxScenicScore, curTreeScenicScore)
            }
        }
        return maxScenicScore
    }

    // Setup utility class
    val aoc = AOC(pathFromSrc = "day08", verbose = true)

    // TESTS
    aoc.inputFilePath = "input_test"
    aoc.test(::part1, answer = 21)
    aoc.test(::part2, answer = 8)


    // PARTS 1 & 2
    aoc.inputFilePath = "input"
    aoc.test(::part1, answer = 1647)
    aoc.test(::part2, answer = 392080)

    // Print out test summary (and failures if in verbose mode)
    aoc.summary()
}
