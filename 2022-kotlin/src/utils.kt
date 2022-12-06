import java.io.File
import java.io.PrintWriter
import java.io.StringWriter
import java.lang.Exception
import java.math.BigInteger
import java.security.MessageDigest

/**
 * Reads lines from the given input txt file.
 */
fun readInput(name: String): List<String> = File("src", "$name.txt")
    .readLines()

/**
 * Converts string to md5 hash.
 */
fun String.md5() = BigInteger(1, MessageDigest.getInstance("MD5").digest(toByteArray()))
    .toString(16)
    .padStart(32, '0')


class AOC(
    var pathFromSrc: String,
    var inputFilePath: String = "",
    private var verbose: Boolean = false
) {
    private var testCounter = 0
    private var numFailedTests = 0
    private var numExceptionTests = 0
    private var failedTests = mutableListOf<Int>()
    private var exceptionTests = mutableListOf<Int>()

    fun <T> test(
        part: (input: List<String>) -> T,
        answer: T,
        testName: String = "",
        newInputFilePath: String = ""
    ) {
        testCounter += 1
        try {
            val result = part(readInput(pathFromSrc + '/' + newInputFilePath.ifBlank { inputFilePath }))
            val testPassed = (result == answer)
            if (!testPassed) {
                if (verbose) {
                    println("================================================")
                    println("Test #$testCounter failed! $testName ")
                    println("Expected:")
                    println(answer)
                    println("------------------------------------------------")
                    println("Got:")
                    println(result)
                }
                failedTests.add(testCounter)
                numFailedTests += 1
            }
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
    }

    fun summary() {
        println("************************************************")
        println("Num Tests: $testCounter")
        val numPassedTests = testCounter - numFailedTests - numExceptionTests
        println("Passed: $numPassedTests Failed: $numFailedTests Exceptions: $numExceptionTests")
        if (numFailedTests > 0) {
            println("Failed tests: $failedTests")
        }
        if (numExceptionTests > 0) {
            println("Tests with exceptions: $exceptionTests")
        }
        println("************************************************")
    }
}