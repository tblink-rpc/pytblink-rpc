
# Overview
PyTBLink is a Python library designed to enable procedural-level
interaction between a Python environment and a testbench environment.

A testbench environment could be any of the following:
- SystemVerilog/UVM testbench
- A SystemC environment
- A Verilog testbench
- A VHDL testbench (?)
- Embedded software (?)

# Requirements
- Interaction should be bi-directional
  - TB creating and calling classes on the Python side
  - Python creating and calling classes on the TB side
  - Python calling structural elements defined on the TB side

- Not all environments (eg VHDL) will support 
  bi-directional interaction, but the library should be
  designed to support
  
- Support building libraries -- ie don't require
  source generation that is testbench-specific 
  in all cases.

# Packaging
- Data types
- 
