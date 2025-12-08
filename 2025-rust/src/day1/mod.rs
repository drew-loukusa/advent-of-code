pub mod day1 {

    static DEBUG_ENABLED: bool = false;
    macro_rules! log {
        ($($rest:tt)*) => {
            if DEBUG_ENABLED {
                std::println!($($rest)*)
            }
        }
    }

    use std::{env, fs::read_to_string};

    fn read_lines(filename: &str) -> Vec<String> {
        read_to_string(filename)
            .unwrap() // panic on possible file-reading errors
            .lines() // split the string into an iterator of string slices
            .map(String::from) // make each slice into a string
            .collect() // gather them together into a vector
    }

    fn part_one(lines: &Vec<String>) -> i32 {
        let mut count = 0;

        let mut dial_pos = 50;
        for instruction in lines {
            // Get direction
            let direction = instruction.chars().nth(0).unwrap();
            let unclamped_delta: i32 = instruction[1..].parse().unwrap();
            let delta = unclamped_delta % 100;

            log!("Dial: {dial_pos}");
            log!("\tDirection: {direction}, Delta: {delta}");

            // Move dial
            if direction == 'L' {
                dial_pos -= delta;
            } else {
                dial_pos += delta;
            }
            log!("\tAfter moving dial: {dial_pos}");

            if dial_pos < 0 {
                dial_pos = 99 + (dial_pos + 1);
            } else if dial_pos > 99 {
                dial_pos = dial_pos - (99 + 1);
            }
            log!("\tAfter clamping dial: {dial_pos}");

            if dial_pos == 0 {
                count += 1;
            }
        }

        if dial_pos == 0 {
            count += 1
        }

        return count;
    }

    fn part_two(lines: &Vec<String>) -> i32 {
        let mut count = 0;

        let mut dial_pos = 50;
        for instruction in lines {
            // Get direction
            let direction = instruction.chars().nth(0).unwrap();
            let unclamped_delta: i32 = instruction[1..].parse().unwrap();

            log!("Dial: {dial_pos}");
            log!("\tUnclamped delta: {unclamped_delta}, Direction: {direction}");

            // IA = instruction amount
            // DTZ == diff to zero
            // 1. Calc diff to 0
            //      R : 100 - dial pos
            //      L : is just dial pos
            let mut diff_to_zero: i32;
            if direction == 'L' {
                diff_to_zero = dial_pos;
            } else {
                diff_to_zero = 100 - dial_pos;
            }
            if diff_to_zero == 0 {
                diff_to_zero = 100;
            }
            log!("\tDiff to zero is {diff_to_zero}");

            // 2. Subtract diff from instr amount , IA - DTZ
            let mut adjusted_unclamped_delta = unclamped_delta - diff_to_zero;
            log!("\tAdjusted, unclamped delta: {adjusted_unclamped_delta}");

            // Put dial at zero, and inc count
            if adjusted_unclamped_delta >= 0 {
                dial_pos = 0;
                count += 1;
                log!("\t\tDial pos set to 0, count inc'd to: {count}")
            } else {
                log!("\t\tAUD was < 0, setting it to unclamped_delta which is: {unclamped_delta}");
                adjusted_unclamped_delta = unclamped_delta;
            }

            // 3. Calculate quotient and remainder from IA (IA / 100 = Q, IA % 100 = R)
            let quotient = adjusted_unclamped_delta / 100;
            let remainder = adjusted_unclamped_delta % 100;
            log!("\tRemainder: {remainder}");
            log!("\tQuotient: {quotient}");

            // 4. Inc count by Q
            // 5. Set dial pos to remainder
            //      R: Set to remainder
            //      L: Set to 100 - remainder
            count += quotient;

            // Move dial
            if direction == 'L' {
                dial_pos -= remainder;
            } else {
                dial_pos += remainder;
            }
            log!("\tAfter moving dial: {dial_pos}");

            // Corect dial position to be within 0 - 99
            if dial_pos < 0 {
                dial_pos = 99 + (dial_pos + 1);
            } else if dial_pos > 99 {
                dial_pos = dial_pos - (99 + 1);
            }
            log!("\tAfter clamping dial: {dial_pos}");
            log!("\tCount: {count}");
        }

        if dial_pos == 0 {
            count += 1
        }

        return count;
    }

    pub fn day_1_main() {
        let path = env::current_dir().unwrap();
        log!("The current directory is {}", path.display());

        log!("Hello day 1");
        let lines = read_lines("src\\day1\\day1.txt");
        // let lines = read_lines("src\\day1\\day1_ex.txt");
        // let lines = read_lines("src\\day1\\day1_ex2.txt");
        let part1 = part_one(&lines);
        assert!(part1 == 1071);

        let part2 = part_two(&lines);
        assert!(part2 == 6700)
    }
}

// part 2 answers:
// 2662 => Wrong, too low

// If delta puts us past 100, calculate amount needed to get to 100 from cur pos
// subtrac that amount from the delta
// Inc count by 1
// Then calculate quotient + remainder from remaning delta
// Inc count by quotient, set dial pos to remainder

// If delta puts us under 0, calc amount needed to get to zero from cur pos
// subtract that amount from delta
// Inc count by 1
// Calculate quotient + remainder
// inc count by quotient, set dial to remainder

// At 50, next instr is R275
// Need 50 to get to 100, so 275 - 50 = 225
// Move dial to 0 (INC COUNT BY 1)
// 225 / 100 = 2, r25
// Inc count by 2, set dial to 0 + 25
// count is now 3

// At 50, instr is L275
// 50 to 0, 275 - 50 = 225
// Move dial to 0
// 225 / 100 = 2 r 25
// Set dial to 0 - 25 = 75

// 2 cases still need to handle
// 1. intr amount will take us past 0, but quotient will be < 100, so it won't inc count at all
// 2. instr amount won't take us past 0

// At 50, instr is R55

// At 75, R50
// 25 to 0, AUD = 50 - 25 = 25
// move dial to 0  (inc count by 1) (AUD is positive)
// 25 / 100 = 0, r25
