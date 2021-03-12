'''
Created on Jul 8, 2020

@author: ballance
'''
import argparse
import os
import sys

tblink_dir = os.path.dirname(os.path.abspath(__file__))
hvl_dir = os.path.join(tblink_dir, "hvl")

def files(args):
    sv_dpi_files = [
        os.path.join(hvl_dir, "tblink.sv")
        ]

    files = None    
    if args.language == "sv-dpi":
        files = sv_dpi_files
    else:
        pass

    result = ""
    for i,file in enumerate(files):
        if i > 0:
            result += " "
        result += file
        
    print(result)
    
def lib(args):
    libpath = None
    for p in sys.path:
        if os.path.exists(os.path.join(p, "libtblink-launcher.so")):
            libpath = os.path.join(p, "libtblink-launcher.so")
            break
        
    print(libpath)

def getparser():
    parser = argparse.ArgumentParser()
    
    subparser = parser.add_subparsers()
    subparser.required = True
    subparser.dest = 'command'
    
    files_cmd = subparser.add_parser("files",
        help="Provides files that need to be compiled")
    files_cmd.set_defaults(func=files)
    files_cmd.add_argument("-language", default="sv-dpi",
                           choices=["sv-dpi", "vlog-vpi"])
    
    lib_cmd = subparser.add_parser("lib",
        help="Get library path")
    lib_cmd.set_defaults(func=lib)
    
    return parser
    

def main():
    parser = getparser()
    
    args = parser.parse_args()
    
    args.func(args)
    
    pass

if __name__ == "__main__":
    main()