import java.io.File
import java.io.PrintWriter
import java.io.StringWriter
import java.lang.Exception
import java.math.BigInteger
import java.security.MessageDigest

/**
 * Reads lines from the given input txt file.
 */
fun readInput(name: String): List<String> {
    val dayPrefix = name.split('_')[0]
    return File("src", "$dayPrefix/$name.txt")
        .readLines() as List<String>
}

/**
 * Converts string to md5 hash.
 */
fun String.md5() = BigInteger(1, MessageDigest.getInstance("MD5").digest(toByteArray()))
    .toString(16)
    .padStart(32, '0')


class AOC(
    private var verbose: Boolean = false,
    var inputFilePath: String = ""
) {
    private var testCounter = 0
    private var numFailedTests = 0
    private var numExceptionTests = 0
    private var failedTests = mutableListOf<Int>()
    private var exceptionTests = mutableListOf<Int>()

    fun test(
        part: (input: List<String>) -> Int,
        answer: Int,
        newInputFilePath: String = ""
    ): Int {
        testCounter += 1
        try {
            val result = part(readInput(newInputFilePath.ifBlank { inputFilePath }))
            val testPassed = (result == answer)
            if (!testPassed) {
                if (verbose) {
                    println("================================================")
                    println("Test #$testCounter failed!")
                    println("Expected:")
                    println(answer)
                    println("------------------------------------------------")
                    println("Got:")
                    println(result)
                }
                failedTests.add(testCounter)
                numFailedTests += 1
            }
            return result
        } catch (e: Exception) {
            exceptionTests.add(testCounter)
            numExceptionTests += 1
            val sw = StringWriter()
            e.printStackTrace(PrintWriter(sw))
            val exceptionAsString = sw.toString()
            if (verbose) {
                println("================================================")
                println("Exception in test #$testCounter!")
                println(exceptionAsString)
            }
        }
        return 0
    }

    fun summary() {
        println("************************************************")
        println("Num Tests: $testCounter")
        val numPassedTests = testCounter - numFailedTests - numExceptionTests
        println("Passed: $numPassedTests Failed: $numFailedTests Exceptions: $numExceptionTests")
        if (numFailedTests > 0) {
            println("Failed tests: $failedTests")
        }
        if (numFailedTests > 0) {
            println("Tests with exceptions: $exceptionTests")
        }
        println("************************************************")
//        Runtime.getRuntime().exec("cls")
    }
}