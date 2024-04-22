#!/bin/bash

clang -g -O0 -gdwarf-3 fibonacci.c -o fibonacci_debug
clang  -O0  fibonacci.c -o fibonacci_stripped
strip fibonacci_stripped
objdump -df --source fibonacci_debug > fibonacci_debug__objdump.txt
