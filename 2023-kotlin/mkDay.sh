#!/bin/bash

if [ -z "$1" ]; then
  echo "ERROR: Must pass in day as argument to script"
  exit 1
fi

mkdir "src/day$1"
touch "src/day$1/input.txt"
touch "src/day$1/input_test.txt"
cp dayTemplate.kt "src/day$1/day$1.kt"
sed -i "" "s/{DAY_REPLACE}/$1/g"  "src/day$1/day$1.kt"