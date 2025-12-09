pub mod day2 {
    static DEBUG_ENABLED: bool = true;
    macro_rules! log {
      ($($rest:tt)*) => {
          if DEBUG_ENABLED {
              std::println!($($rest)*)
          }
      }
  }

    use std::{env, fs::read_to_string, ops::ShrAssign};

    fn read_lines(filename: &str) -> Vec<String> {
        read_to_string(filename)
            .unwrap() // panic on possible file-reading errors
            .lines() // split the string into an iterator of string slices
            .map(String::from) // make each slice into a string
            .collect() // gather them together into a vector
    }

    fn process_input(lines: &Vec<String>) -> Vec<(u128, u128)> {
        let input = &lines[0];
        let ranges: Vec<String> = input.split(',').map(String::from).collect();
        let mut id_pairs: Vec<(u128, u128)> = Vec::new();
        for item in ranges {
            let ids: Vec<String> = item.split('-').map(String::from).collect();
            let left: u128 = ids[0].parse().unwrap();
            let right: u128 = ids[1].parse().unwrap();
            log!("(left: {left}, right {right})");
            id_pairs.push((left, right));
        }

        return id_pairs;
    }

    // ID = 123123
    // CO = 123123
    // Remove left half of CO,  CO = 000123
    // Remove right half of ID, ID = 123000
    // Right shift ID, ID = 000123

    trait LongExt {
        fn count_digits(&self) -> i32;
        fn dec_shift_right(&self, amount: i32) -> u128;
        fn dec_shift_left(&self, amount: i32) -> u128;
    }
    impl LongExt for u128 {
        // Compare ID and CO by subtraction, if result is 0, id is valid
        fn count_digits(&self) -> i32 {
            // You could totally add caching here, num digit counts DO NOT CHANGE
            let mut rem = self.clone();
            let mut count = 0;
            while rem > 0 {
                rem /= 10;
                count += 1;
            }
            return count;
        }

        fn dec_shift_right(&self, amount: i32) -> u128 {
            // You could totally add caching here, num digit counts DO NOT CHANGE
            let mut rem = self.clone();
            let mut count = 0;
            while rem > 0 && count < amount {
                rem /= 10;
                count += 1;
            }
            return rem;
        }

        fn dec_shift_left(&self, amount: i32) -> u128 {
            // You could totally add caching here, num digit counts DO NOT CHANGE
            let mut rem = self.clone();
            let mut count = 0;
            while count < amount {
                rem *= 10;
                count += 1;
            }
            return rem;
        }
    }

    fn id_is_invalid(id: u128) -> bool {
        // Make a copy 123123
        let id_copy = id.clone();

        // decimal shift copy right by half
        let id_digits = id.count_digits();
        let left_chunk_shifted_right = id_copy.dec_shift_right(id_digits / 2); // 123123 => 123 (left chunk)
        log!("Id {id}, digits in id: {id_digits}");
        log!("\tleft chunk {left_chunk_shifted_right}");

        // Zero out left side of id
        // make another copy, and zero out right side
        let mask_to_get_other_mask: u128 = left_chunk_shifted_right.dec_shift_left(id_digits / 2); // 123 => 123000
        log!("\tMask to get other mask {mask_to_get_other_mask}");
        let right_chunk_mask: u128 = id - mask_to_get_other_mask; // 123123 - 123000 => 123 (right chunk)
        log!("\tRight chunk mask is {right_chunk_mask}");
        let right_chunk = id - right_chunk_mask; // 
        log!("\tRight chunk {right_chunk}");
        let result = left_chunk_shifted_right - right_chunk == 0;
        log!("\tIs valid invalid id? {result}");
        return result;
    }

    /// Walk a range and thu sum of invalid ids contained in it
    fn walk_range(pair: &(u128, u128)) -> u128 {
        assert!(pair.0 < pair.1);
        let mut invalid_id_sum = 0;
        let mut i = pair.0;
        while i <= pair.1 {
            if id_is_invalid(i) {
                invalid_id_sum += i;
            }
            i += 1;
        }
        return invalid_id_sum;
    }

    pub fn part_one(id_pairs: &Vec<(u128, u128)>) -> u128 {
        let mut sum = 0;
        for range in id_pairs {
            let sub_sum = walk_range(range);
            log!("Range is {range:?} sub_sum is {sub_sum}");
            sum += sub_sum;
        }
        return sum;
    }
    pub fn part_two(id_pairs: &Vec<(u128, u128)>) {}

    pub fn day_2_main() {
        log!("Hello day 2");
        let lines = read_lines("src\\day2\\day2_ex.txt");
        // let lines = read_lines("src\\day1\\day1_ex.txt");
        // let lines = read_lines("src\\day1\\day1_ex2.txt");
        let input = process_input(&lines);
        // let part1 = part_one(&input);
        // assert!(part1 == 1071);

        id_is_invalid(123123);
        id_is_invalid(22);
        id_is_invalid(23);
        id_is_invalid(6868);
        id_is_invalid(1234);
        // let part2 = part_two(&lines);
        // assert!(part2 == 6700)
    }
}

// Duh obvious route
// Walk each range, for each range
// for each id in range
// check if id is valid
// convert to string, if is even length, put pointer at halfway mark
// walk first half and second half at same time, comparing as you go

// This approach is obviously a bit slow...
// AND, if we have ranges that are contained inside other ranges, we are actually
// duplicating work

// there is the opportunity to memoize here...
// Let's try the brute force solution first, see if it runs quick enough.
// If not..... Then we can try memoizing, or coming up with a diff solution that's more clever
