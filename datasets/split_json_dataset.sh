#!/bin/bash
# splits the dataset Movies_and_TV_5.json in 9 files.
# each filename is  starting with Movies_and_TV + a increasing number f.ex Movies_TV_07.json
split -d  -nl/9 --additional-suffix=.json  Movies_and_TV_5.json Movies_and_TV