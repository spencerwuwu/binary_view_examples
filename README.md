# Binary Visualization Toy Examples

This repository contains the toy examples of various C programs to start visualizing with.
`png_parser` is a relatively large program demonstrated previously, 
the rest are simple small C code with different control flow structures.

Each directory contains the following files:

- The source code of the program.
- The compiled binary files with and without debug information.
- A `*__objdump.txt` that contains the output of simple disassembly of the binary file, along with each block's corresponding source code.
- `*.json` contains the graph information of the corresponding binary to start visualizing with (generated with [angr](https://github.com/angr/angr). 
- `*.png` is the existing visual representation generated with [bingraphvis](https://github.com/spencerwuwu/bingraphvis)
- `*_nocall.png`, if presented, is the same graph above but remove call and return edges for simplicity (by ignoring *Ijk_Call*, *Ijk_Ret*, *Ijk_FakeRet* when rendering)
- A `compile.sh` to compile the program (`png_paser` uses a Makefile)

## Format of the JSON file
```
{
    "all_nodes": {
        "<node address>": {
            "name": xx,
            "address": xx,
            "size": xx,
            "function_address": <the function address of this block belongs to>,
            "instructions": {
                instr_addr: "<assembly instruction>",
                ...
            {,
            "successors": [
                (<the address of this node may jumps to>, <type of the jump>),
                (<the address of this node may jumps to>, <type of the jump>),
                ...
            ],
            "predecessors": [
                (<the address of this node is jumped from>, <type of the jump>),
                (<the address of this node is jumped from>, <type of the jump>),
                ...
            ]
        },
        ...
    },
    "call_graph_edges": [
        (<the address of the caller>, <the address of the callee>, <type of the connection>),
        (<the address of the caller>, <the address of the callee>, <type of the connection>),
        ...
    ]
}
```

## Variations
I provided several versions of Control-Flow Graphs (CFG) for the same binary,
created by setting different options in angr.
- `__fast` 
    - this is created by sweeping through the binary file, 
    and create CFGs from any potential points.
- `__emulated-*`: 
    - these CFGs are created by emulating the binary with different options. 
    In other words, angr pretends to execute the binary and create the CFG based on the execution result. By default angr starts with the `_start` function.
    - `-cs*` stands for context sensitivity, you can read more about it 
    [here](https://docs.angr.io/en/latest/analyses/cfg.html#context-sensitivity-level).
    - `-calldepth0` means during emulation, angr will not further trace down any function call. 
    It is good to get a CFG for single functions, but by default it won't even go further after `_start`.
    Instead, I provided angr with a list of function entry to start creating CFGs with based on the result from `__fast`. 
    You should able to see a lot of garbage here for multiple reasons. This is essentially what we would like to see and try to fix for research.


## Installation
If you're insterested in running the angr scripts, you need to install the required packages.
```bash
pip install -r requirements.txt
git clone https://github.com/spencerwuwu/bingraphvis
pushd bingraphvis
pip install -r requirements-dev.txt
popd
```
Then run
```bash
python3 export_angr_graph.py <binary_file>
```
