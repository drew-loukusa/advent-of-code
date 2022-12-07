package day07

import AOC

fun main() {

    data class File(val name: String, val size: Int)

    data class Directory(
        var name: String = "",
        var size: Int = 0,
        var files: MutableList<File> = mutableListOf(),
        var parent: Directory ?,
        var dirs: MutableMap<String, Directory> = mutableMapOf()
    )

    fun getNext(itr: Iterator<String>): List<String> {
        if (itr.hasNext()){
            val line = itr.next()
            //println(line)
            return line.split(' ')
        }
        return listOf()
    }

    fun updateDirSizeRec(curDir: Directory): Int {
        // Because we don't know how big a directory will be until after we
        // process all the dirs, run a recursive process after the fact to update the sizes

        // base case
        if (curDir.dirs.isEmpty()) return curDir.size

        for (childDir in curDir.dirs.values){
            curDir.size += updateDirSizeRec(childDir)
        }

        return curDir.size
    }

    fun parseTerminalHistory(input: List<String>): Directory {
        val rootDir = Directory("/", parent = null)
        var currentDir = rootDir
        val itr = input.iterator()
        itr.next() // Skip $ cd /
        var tokens = getNext(itr)
        while (itr.hasNext()){
            when (tokens[1]){
                "cd" -> {
                    currentDir = when (tokens[2]){
                        ".." -> currentDir.parent !!
                        "/" -> rootDir
                        else -> currentDir.dirs[tokens[2]] !!
                    }
                    tokens = getNext(itr)
                }
                "ls" -> {
                    // process files for current dir
                    tokens = getNext(itr)
                    while (tokens[0] != "$") {
                        when (tokens[0]) {
                            "dir" -> {
                                // create child dir
                                val name = tokens[1]
                                currentDir.dirs[name] = Directory(name, parent = currentDir)
                            }
                            else -> {
                                // Create file in current dir
                                val (sizeStr, name) = tokens
                                val size = sizeStr.toInt()
                                currentDir.files.add(File(name, size))
                                currentDir.size += size
                            }
                        }
                        tokens = getNext(itr)
                        if (tokens.isEmpty()) break
                    }
                }
            }
        }
        updateDirSizeRec(rootDir)
        return rootDir
    }

    fun findDirsWithSizeAtMost(rootDir: Directory, maxSize: Int): Int {
        var dirSum = 0
        val dirQueue = mutableListOf(rootDir)
        while (dirQueue.isNotEmpty()){
            val curDir = dirQueue.removeAt(0)
            if (curDir.size <= maxSize){
                dirSum += curDir.size
            }
            dirQueue.addAll(curDir.dirs.values)
        }
        return dirSum
    }

    fun part1(input: List<String>): Int {
        val rootDir = parseTerminalHistory(input)
        return findDirsWithSizeAtMost(rootDir, 100000)
    }

    fun part2(input: List<String>): Int {
        val rootDir = parseTerminalHistory(input)
        val totalDiskSpace = 70000000
        val updateSize = 30000000
        val amountToClear = updateSize - (totalDiskSpace - rootDir.size)

        var candidateDir = rootDir
        val dirQueue = mutableListOf(candidateDir)
        while (dirQueue.isNotEmpty()){
            val curDir = dirQueue.removeAt(0)

            if (curDir.size >= amountToClear && curDir.size < candidateDir.size)
                candidateDir = curDir

            dirQueue.addAll(curDir.dirs.values)
        }
        return candidateDir.size
    }

    // Setup utility class
    val aoc = AOC(pathFromSrc = "day07", verbose = true)

    // TESTS
    aoc.inputFilePath = "input_test"
    aoc.test(::part1, answer = 95437)
    aoc.test(::part2, answer = 24933642)


    // PARTS 1 & 2
    aoc.inputFilePath = "input"
    aoc.test(::part1, answer = 1908462)
    aoc.test(::part2, answer = 3979145)

    // Print out test summary (and failures if in verbose mode)
    aoc.summary()
}
