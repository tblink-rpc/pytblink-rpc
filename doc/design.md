
# Overview
PyTBLink is a Python library designed to enable procedural-level
interaction between a Python environment and a testbench environment.

A testbench environment could be any of the following:
- SystemVerilog/UVM testbench
- A SystemC environment
- A Verilog testbench
- A VHDL testbench (?)
- Embedded software (?)

- tblink front-end library is pure python
  - Uses 'backend' abstraction to
    - Get simulation time and timescale information
    - Register timed callbacks
    - Discover and call methods
    
- Most Python-side scheduling is handled by asyncio, which 
  is not available at the C level.
- tblink exposes APIs to interact with Python interpreter
  - SV abstraction for packing arguments and calling methods
    - Refcounts must be managed by the user
  - C/C++ abstraction for calling methods
- tblink provides an implementation of an hvl-rpc endpoint,
  with bindings on the HVL side (?)
  
  
- Priorities
  - Python launcher
  - Event-loop basics -- do we need anything more involved than asyncio?
  - 

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
  
- Note: tasks are a bit tricky. 
  - Need to invoke from different thread, provided by env
  - Need to pack arguments -- ideally without directly using libffi
  - 
  
- Invoking 'task' from env
  - Create task in which to call function
  - Need to have event on 'env' side for synchronization
  - 

# Interface
- Launcher library/libraries
  - May be simulator-specific
  - 
# Packaging
- Data types


# Simulator differences
- Commercial simulators require time-management to be in SV
  - Require an extra top-level module to host initial block
  - Package only used for SV->Py API
  - Initialization code is in the module
- Verilator doesn't support SV-based time management
  - Only supports a single top-level module
  - Package used for both SV->Py API and initialization code
- 
