package day05

import AOC
import kotlin.math.min

typealias LinesConsumed = Int
typealias SourceNum = Long
typealias DestNum = Long
typealias SourceName = String

fun main() {

    data class SourceDestRanges(val source: LongRange, val dest: LongRange)

    data class ResourceMap(
        val sourceName: String,
        val destName: String,
        val ranges: List<SourceDestRanges>
    )

    data class SeedsAndMaps(
        val seeds: List<Long>,
        val resourceMaps: Map<SourceName, ResourceMap> // Map from 'source name' -> 'source to dest map'
    )

    fun parseMap(startIndex: Int, input: List<String>): Pair<LinesConsumed, ResourceMap> {
        val (sourceName, _, destName) = input[startIndex].split(' ')[0].split('-')
        var curIndex = startIndex + 1
        var linesConsumed = 1
        val ranges = mutableListOf<SourceDestRanges>()

        while (curIndex < input.size) {
            val line = input[curIndex]

            // Parse until we find an empty line which
            // signifies the end of the current resource map
            if (line.isBlank()) {
                break
            }

            val (destStart, sourceStart, rangeLength) = line.split(' ').map { it.toLong() }
            val destRange = (destStart..(destStart + rangeLength))
            val sourceRange = (sourceStart..(sourceStart + rangeLength))

            ranges.add(SourceDestRanges(source = sourceRange, dest = destRange))
            curIndex += 1
            linesConsumed += 1
        }

        return linesConsumed to ResourceMap(
            sourceName = sourceName,
            destName = destName,
            ranges = ranges
        )
    }

    fun parseInput(input: List<String>): SeedsAndMaps {
        var curIndex = 0
        val seeds = input[curIndex].split(':')[1].trim().split(' ').map { it.toLong() }
        curIndex += 1

        val maps = mutableMapOf<String, ResourceMap>()

        // While not at EOF, keep trying to parse maps
        while (curIndex < input.size) {
            val line = input[curIndex]
            // Skip empty lines
            if (line.isBlank()) {
                curIndex += 1
                continue
            }

            val (linesConsumed, map) = parseMap(startIndex = curIndex, input = input)

            // Move index based on how many lines were consumed by parsing last map
            curIndex += linesConsumed
            maps[map.sourceName] = map
        }
        return SeedsAndMaps(seeds = seeds, resourceMaps = maps)
    }

    // For each seed in starting seed set
    //   For next map
    //      For each source range in list of range pairs
    //          Is seed in bounds of range?
    //              YES
    //                  Find offset from start of range: (startNum - rangeStart)
    //                  Take offset, and calculate landing num in dest range: (destRangeSTart + offset)
    //                  Insert into "mapped Seeds" for current MAP step
    //                  DONE
    //              NO
    //                  continue to next range
    //      If cur seed not contained in any source range, it maps to itself
    //          Insert into mapped seeds for current map step
    //       Go to next map

    fun findMinSeedFromIterable(seedsIterable: Iterable<Long>, maps: Map<SourceName, ResourceMap>): Long {
        var minSeedValue = Long.MAX_VALUE
        seedsIterable.forEach { seed ->
            var curMapKey = "seed"
            val mappedValues = mutableListOf(seed)
            repeat(maps.size) {
                val curValue = mappedValues.last()
                val (_, destName, ranges) = maps[curMapKey]!!
                var mappedByRange = false
                for (range in ranges) {
                    val (source, dest) = range
                    if (source.contains(curValue)) {
                        val offset = curValue - source.first
                        val destNum = dest.first + offset
                        mappedValues.add(destNum)
                        mappedByRange = true
                        break // NOTE: I'm assuming there are no overlaps between ranges in a given map
                    }
                }
                if (!mappedByRange) {
                    mappedValues.add(curValue)
                }
                curMapKey = destName
            }
            minSeedValue = min(minSeedValue, mappedValues.last())
        }

        return minSeedValue
    }

    fun part1(input: List<String>): Long {
        val (seeds, maps) = parseInput(input)
        return findMinSeedFromIterable(seeds, maps)
    }

    fun buildSeedRanges(seeds: List<Long>): List<LongRange> {
        val seedRanges = mutableListOf<LongRange>()
        var i = 0
        while (i < seeds.size) {
            val rangeStart = seeds[i]
            val rangeEnd = seeds[i] + seeds[i+1]
            seedRanges.add(rangeStart..rangeEnd)
            i += 2
        }
        return seedRanges
    }

    fun part2(input: List<String>): Long {
        val (seeds, maps) = parseInput(input)

        var metaMinSeedValue = Long.MAX_VALUE

        val seedRanges = buildSeedRanges(seeds)

        seedRanges.withIndex().forEach { (i, seedRange) ->
            println("Processing seed range $i")
            val minSeedValue = findMinSeedFromIterable(seedRange, maps)
            metaMinSeedValue = min(metaMinSeedValue, minSeedValue)
        }

        // Brute force is still too slow for part 2, even with us not generating the ranges of numebrs
        // for each map

        // Need some kind of trick, probably involving dynamic programming. You might be able to
        // build up a local solution at each map (cheapest range is this one) and maybe work backwards
        // from the last map?
        // Like, pick the smallest range, in the last map, and pick the smallest value from that range
        // Map backwards through the resource maps, and see if it maps to a valid initial seed value

        return metaMinSeedValue
    }

    // Setup utility class
    val aoc = AOC(pathFromSrc = "day05", verbose = true)

    // TESTS
    aoc.inputFilePath = "input_test"
    aoc.test(::part1, answer = 35)
    aoc.test(::part2, answer = 46)

    // PARTS 1 & 2
    aoc.inputFilePath = "input"
    aoc.test(::part1, answer = 313045984)
    aoc.test(::part2, answer = -1)

    // Print out test summary (and failures if in verbose mode)
    aoc.summary()
}
