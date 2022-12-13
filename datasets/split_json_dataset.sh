#!/bin/bash
# splits the dataset Movies_and_TV_5.json in 9 files.
# each filename is  starting with Movies_and_TV + a increasing number f.ex Movies_TV_07.json
total_number_of_lines=$(<Movies_and_TV_5.json wc -l)
number_of_lines=$((total_number_of_lines/9)) 
split -d -l $number_of_lines --additional-suffix=".json"  Movies_and_TV_5.json Movies_and_TV
