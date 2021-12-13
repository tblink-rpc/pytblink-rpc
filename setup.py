
import os
from setuptools import setup

setup(
    name='pytblink-rpc',
    packages=['tblink'],
    package_dir={'' : 'src'},
    author = "Matthew Ballance",
    author_email = "matt.ballance@gmail.com",
    description = ("PyTBLink provides a procedure-based interface between Python and simulation environments such as SystemC and SystemVerilog"),
    license = "Apache 2.0",
    keywords = ["SystemVerilog", "Verilog", "RTL", "cocotb", "Python"],
    url = "https://github.com/fvutils/pytblink",
    setup_requires=[
        'setuptools_scm'
    ],    
    install_requires=[
        'tblink_rpc_core'
    ]
    )