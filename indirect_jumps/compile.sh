#!/bin/bash

clang -g -O0 -gdwarf-3 function_pointer.c -o function_pointer_debug
clang  -O0  function_pointer.c -o function_pointer_stripped
strip function_pointer_stripped
objdump -df --source function_pointer_debug > function_pointer_debug__objdump.txt
