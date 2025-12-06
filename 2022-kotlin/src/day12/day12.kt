package day12

import AOC
import java.awt.Point
import kotlin.math.abs

fun main() {
    fun part1(input: List<String>): Int? {
        val ymax = input.size - 1
        val xmax = input[0].length - 1

        fun inBounds(p: Point) = p.y >= 0 && p.x <= xmax && p.x >= 0 && p.y <= ymax
        fun find(targetC: Char, input: List<String>): Point {
            for ((y,row) in input.withIndex()){
                for ((x, c) in row.withIndex()){
                    if (c == targetC){
                        return Point(x,y)
                    }
                }
            }
            return Point(-1, -1)
        }
        fun getHeight(p: Point) = if (input[p.y][p.x] == 'E') 'z' else input[p.y][p.x]

        val end = find('E', input)
        val visited = mutableMapOf(end to 0)
        val queue = mutableListOf(end)
        val qSet = mutableSetOf(end)
        fun bfs(end: Point, input: List<String>): Int? {
            while (queue.isNotEmpty()){
                val p = queue.removeAt(0)
                qSet.remove(p)
                visited[p] = 0

                val points = listOf(
                    Point(p.x, p.y - 1), // Up
                    Point(p.x, p.y + 1), // Down
                    Point(p.x + 1, p.y), // Right
                    Point(p.x - 1, p.y), // Left
                ).filter { inBounds(it) }
                val localVisited = points.filter { it in visited }
                val notVisited = points.filter { it !in visited }

                if (localVisited.isNotEmpty()){
                    val shortestPathToEnd = localVisited.mapNotNull { visited[it] }.min()
                    visited[p] = shortestPathToEnd + 1
                }

                for (newPoint in notVisited){
                    val pHeight = getHeight(p)
                    val npHeight = getHeight(newPoint)
                    if (newPoint !in qSet && (abs(npHeight - pHeight) <= 1) ){
                        queue.add(newPoint)
                        qSet.add(newPoint)
                    }
                }

            }

            val s = find('S', input)
            var points = listOf(
                Point(s.x, s.y - 1), // Up
                Point(s.x, s.y + 1), // Down
                Point(s.x + 1, s.y), // Right
            )
            points = points.filter { inBounds(it) }
            val shortestPathToEnd = points.mapNotNull {
               visited[it]
            }.min()
            visited[s] = shortestPathToEnd + 1
            return visited[s]
        }
        return bfs(end, input)
    }

    fun part2(input: List<String>): Int {
        return 0
    }

    // Setup utility class
    val aoc = AOC(pathFromSrc = "day12", verbose = true)

    // TESTS
    aoc.inputFilePath = "input_test"
    aoc.test(::part1, answer = 31)
    //aoc.test(::part2, answer = -1)

    // PARTS 1 & 2
    aoc.inputFilePath = "input"
    aoc.test(::part1, answer = -44)
    //aoc.test(::part2, answer = -1)

    aoc.summary()
}

