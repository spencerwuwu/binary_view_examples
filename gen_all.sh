#!/bin/bash

targets=(
    simple_add/simple_debug
    simple_add/simple_stripped
    loops_recursive/fibonacci_debug
    loops_recursive/fibonacci_stripped
    indirect_jumps/function_pointer_debug
    indirect_jumps/function_pointer_stripped
)

for target in "${targets[@]}"; do
	./export_angr_graph.py $target
done
