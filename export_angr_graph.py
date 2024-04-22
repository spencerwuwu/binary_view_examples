#!/usr/bin/env python3
import os
import sys
import angr
import json
from loguru import logger

from bingraphvis import DotOutput
from bingraphvis.angr import *
from bingraphvis.angr.x86 import *

logger.remove()
logger.add(sys.stdout, level="DEBUG") 


def export_cfg_to_json(cfg, output_file):
    all_nodes = {}
    for node in cfg.graph.nodes():
        if node.block is None:
            node_instructions = []
        else:
            node_instructions = {i.address: i.op_str for i in node.block.capstone.insns}
        successors = [(dest.addr, jump_type) for dest, jump_type in node.successors_and_jumpkinds()]
        predecessors = [(src.addr, jump_type) for src, jump_type in node.predecessors_and_jumpkinds()]
        all_nodes[node.addr] = {
            'addr': node.addr,
            'size': node.size,
            'name': node.name,
            'function_address': node.function_address,
            'instructions': node_instructions,
            'successors': successors,
            'predecessors': predecessors,
        }
    call_graph = cfg.functions.callgraph
    call_graph_edges = []
    for edge, edge_info in call_graph.edges.items():
        call_graph_edges.append((edge[0], edge[1], edge_info['type']))

    with open(output_file, 'w') as f:
        json.dump({'all_nodes': all_nodes, 'call_graph_edges': call_graph_edges}, f, indent=2)


def dump_cfg(binary, cfg, cfg_type, no_call=False, no_png=True):
    logger.info(f"Exporting info to {binary}__{cfg_type}.json")
    export_cfg_to_json(cfg, f'{binary}__{cfg_type}.json')

    if no_png:
        return

    logger.info(f"Plotting {cfg_type} to {binary}__{cfg_type}.png")
    vis = AngrVisFactory().default_cfg_pipeline(cfg, asminst=True, vexinst=False)
    vis.set_output(DotOutput(f'{binary}__{cfg_type}', format="png"))
    vis.process(cfg.graph)

    if no_call:
        logger.info(f"Plotting {cfg_type}_nocall to {binary}__{cfg_type}_nocall.png")
        vis = AngrVisFactory().default_cfg_pipeline(cfg, asminst=True, vexinst=False)
        vis.set_output(DotOutput(f'{binary}__{cfg_type}_nocall', format="png"))
        vis.process(cfg.graph, no_call=True)


def main(binary):
    # Load the binary
    logger.info(f"Creating angr project for {binary}")
    proj = angr.Project(binary, load_options={'auto_load_libs': False, 'main_opts': {'base_addr': 0x0}})

    logger.info(f"Computing CFGs for {binary}")
    # Fast CFG
    cfg = proj.analyses.CFGFast(fail_fast=False, normalize=True,
                                symbols=True, function_prologues=True, 
                                force_smart_scan=True, show_progressbar=True,
                                data_references=True, resolve_indirect_jumps=True)
    dump_cfg(binary, cfg, 'fast', no_call=True)

    # Emulated CFG, no trace down function call
    e_cfg = proj.analyses.CFGEmulated(call_depth=0, starts=list(cfg.functions.callgraph.nodes))
    dump_cfg(binary, e_cfg, 'emulated-calldepth0', no_call=True)

    # Emulated CFG with different context sensitivity levels
    e_cfg = proj.analyses.CFGEmulated(context_sensitivity_level=0)
    dump_cfg(binary, e_cfg, 'emulated-cs0')

    e_cfg = proj.analyses.CFGEmulated(context_sensitivity_level=1)
    dump_cfg(binary, e_cfg, 'emulated-cs1')

    e_cfg = proj.analyses.CFGEmulated(context_sensitivity_level=2)
    dump_cfg(binary, e_cfg, 'emulated-cs2')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: {} <binary>".format(sys.argv[0]))
        sys.exit(1)
    if not os.path.isfile(sys.argv[1]):
        print("Error: file not found: {}".format(sys.argv[1]))
        sys.exit(1)
    main(sys.argv[1])
