pub mod day1 {

    static DEBUG_ENABLED: bool = true;
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
            let quotient = unclamped_delta / 100;
            let delta = unclamped_delta % 100;

            log!("Dial: {dial_pos}");
            log!("\tDirection: {direction}, Delta: {delta}");
            log!("\tQuotient: {quotient}");

            // From my cur pos, will my delta move me past 0?
            // If so inc count
            //  BUT, will it move me past 0 more than once?

            // POS = 0
            // R 201 (100 + 100 + 1)
            // 0 + 100 1 = 0 count 1
            // 0 + 100 = 0 count 2
            // 0 + 1 = 1 count 2

            // 201 / 100 = 2 (floor divide)
            // 201 % 100 = 1

            // Move dial
            let prev_dial_pos = dial_pos;
            if direction == 'L' {
                dial_pos -= delta;
            } else {
                dial_pos += delta;
            }
            log!("\tAfter moving dial: {dial_pos}");

            log!("\tPrev dial pos {prev_dial_pos}");
            if (direction == 'L' && dial_pos < 0) || (direction == 'R' && dial_pos > 99) {
                log!("\t\tWent past 0, increasing count!");
                count += 1;
            }

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
        let lines = read_lines("src\\day1\\day1_ex.txt");
        // let part1 = part_one(&lines);
        // assert!(part1 == 1071);

        let part2 = part_two(&lines);
        println!("Part 2 result: {part2}")
        // assert!()
    }
}

// If delta puts us past 100, calculate amount needed to get to 100 from cur pos
// subtrac that amount from the delta
// Inc count by 1
// Then calculate quotient + remainder from remaning delta
// Inc count by quotient, set dial pos to remainder
