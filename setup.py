
import os
from setuptools import setup
from Cython.Build import cythonize
from distutils.extension import Extension
from Cython.Distutils import build_ext
from distutils.command.build_clib import build_clib
from distutils.ccompiler import new_compiler
from distutils.spawn import find_executable
#from setuptools.command.build_ext import build_ext as _build_ext
from Cython.Distutils import build_ext as _build_ext
from distutils.file_util import copy_file

def find_source(bases):
    ret = []
    for base in bases:
        for file in os.listdir(base):
            if os.path.splitext(file)[1] in (".cpp", ".c"):
                ret.append(os.path.join(base, file))
            
    print("find_source: " + str(ret))
    return ret

pybfms_root  = os.path.dirname(os.path.abspath(__file__))
tblink_dir   = os.path.dirname(os.path.abspath(__file__))
packages_dir = os.path.join(tblink_dir, "packages")

def _get_lib_ext_name():
    """ Get name of default library file extension on given OS. """

    if os.name == "nt":
        ext_name = "dll"
    else:
        ext_name = "so"

    return ext_name

class build_ext(_build_ext):
    def run(self):

        # TODO:
#        def_dir = os.path.join(cocotb_share_dir, "def")
#        self._gen_import_libs(def_dir)

        super().run()

    # Needed for Windows to not assume python module (generate interface in def file)
    def get_export_symbols(self, ext):
        return None

    # For proper cocotb library naming, based on https://github.com/cython/cython/issues/1740
    def get_ext_filename(self, ext_name):
        """
        Like the base class method, but for libraries that are not python extension:
         - removes the ``.cpython-36m-x86_64-linux-gnu.`` part before the extension
         - replaces ``.pyd`` with ``.dll`` on windows.
        """

        print("ext_name: " + str(ext_name))

        filename = _build_ext.get_ext_filename(self, ext_name)

        # for the simulator python extension library, leaving suffix in place
        # TODO:
#        if "simulator" == os.path.split(ext_name)[-1]:
#            return filename

        head, tail = os.path.split(filename)
        tail_split = tail.split(".")

        filename_short = os.path.join(head, tail_split[0] + "." + _get_lib_ext_name())

        # icarus requires vpl extension, gpivpi is default in Makefiles
        # TODO:
#        if "icarus" in filename:
#            filename_short = filename_short.replace("libvpi.so", "gpivpi.vpl")
#            filename_short = filename_short.replace("libvpi.dll", "gpivpi.vpl")

        return filename_short

    def finalize_options(self):
        """ Like the base class method,but add extra library_dirs path. """
        super().finalize_options()

    def copy_extensions_to_source(self):
        """ Like the base class method, but copy libs into proper directory in develop. """

        build_py = self.get_finalized_command("build_py")
        for ext in self.extensions:
            fullname = self.get_ext_fullname(ext.name)
            filename = self.get_ext_filename(fullname)
            modpath = fullname.split(".")
            package = ".".join(modpath[:-1])
            package_dir = build_py.get_package_dir(package)
            # unlike the method from `setuptools`, we do not call `os.path.basename` here
            dest_filename = os.path.join(package_dir, filename)
            src_filename = os.path.join(self.build_lib, filename)

            os.makedirs(os.path.dirname(dest_filename), exist_ok=True)

            copy_file(
                src_filename, dest_filename, verbose=self.verbose, dry_run=self.dry_run
            )
            if ext._needs_stub:
                self.write_stub(package_dir or os.curdir, ext, True)

    def _gen_import_libs(self, def_dir):
        """
        On Windows generate import libraries that contains the code required to
        load the DLL (.a) based on module definition files (.def)
        """

        # TODO:
        if os.name == "nt":
            for sim in ["icarus", "modelsim", "aldec"]:
                subprocess.run(
                    [
                        "dlltool",
                        "-d",
                        os.path.join(def_dir, sim + ".def"),
                        "-l",
                        os.path.join(def_dir, "lib" + sim + ".a"),
                    ]
                )


setup(
  name = "pytblink",
  packages=['tblink'],
  package_dir = {'' : 'src'},
  author = "Matthew Ballance",
  author_email = "matt.ballance@gmail.com",
  description = ("PyTBLink provides a procedure-based interface between Python and simulation environments such as SystemC and SystemVerilog"),
  license = "Apache 2.0",
  keywords = ["SystemVerilog", "Verilog", "RTL", "cocotb", "Python"],
  url = "https://github.com/fvutils/pytblink",
  entry_points={
    'console_scripts': [
      'tblink = tblink.__main__:main'
    ],
    'hvlrpc.generators' : 'sv=tblink.generators.systemverilog'
  },
  setup_requires=[
    'setuptools_scm'
  ],
  cmdclass={'build_ext': build_ext},
  ext_modules=[
        Extension("libtblink-launcher",
            include_dirs=[
                os.path.join(pybfms_root, 'ext/launcher'), 
                os.path.join(pybfms_root, 'src/tblink/share/include'), 
                os.path.join(packages_dir, "json", "include")
                ],
            sources=find_source([
                os.path.join(pybfms_root, 'ext/launcher')
            ])
        ),
        Extension('tblink_core', 
            sources=['ext/tblink_core.pyx'],
            include_dirs=[
                'ext/launcher',
                os.path.join(packages_dir, "json", "include")
                ],
            language="c++")
    ]
)

