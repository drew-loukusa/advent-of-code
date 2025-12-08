pub mod day2 {
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

    pub fn part_one(lines: &Vec<String>) {}
    pub fn part_two(lines: &Vec<String>) {}

    pub fn day_2_main() {
        log!("Hello day 2");
        let lines = read_lines("src\\day2\\day2.txt");
        // let lines = read_lines("src\\day1\\day1_ex.txt");
        // let lines = read_lines("src\\day1\\day1_ex2.txt");
        let part1 = part_one(&lines);
        // assert!(part1 == 1071);

        // let part2 = part_two(&lines);
        // assert!(part2 == 6700)
    }
}
