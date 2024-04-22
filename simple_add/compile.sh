#!/bin/bash

clang -g -O0 -gdwarf-3 simple.c -o simple_debug
clang  -O0  simple.c -o simple_stripped
strip simple_stripped
objdump -df --source simple_debug > simple_debug__objdump.txt
