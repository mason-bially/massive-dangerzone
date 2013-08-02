"""language.py
@OffbyoneStudios 2013
languages/python
The language object pulling togeather all of the pieces needed for a plugin of this language.
"""

import os
import glob

from . import clean
from . import load
from . import compiler_gcc, compiler_mingw, compiler_clang, compiler_cl
from . import wrapgen

class LanguagePy(object):
    def __init__(self, plugin_stub):
        self.plugin_stub = plugin_stub

    compilers = {
        "gcc": compiler_gcc.GCCCompiler,
        "mingw": compiler_mingw.MinGWCompiler,
        "clang": compiler_clang.ClangCompiler,
        "cl": compiler_cl.MSCLCompiler,
    }

    def get_language_path(self):
        return os.path.dirname(__file__)

    def get_compiler(self):
        compiler_config_list = self.plugin_stub.language_config.get_config_list("compiler")
        return self.compilers[compiler_config_list[0]](self, {})

    def make_cleaner(self):
        return clean.Cleaner(self)

    def make_loader(self):
        return load.Loader(self)

    def make_builder(self):
        return self.get_compiler()

    def make_wraper(self):
        return wrapgen.WrapperGenerator(self)

    def supported_extensions(self):
        return []

    def get_default_language_config(self):
        return {
            "compiler": "gcc",
            "compiler+unix": "gcc",
            "compiler+windows": "mingw",
        }

    def get_root_directory(self):
        return self.plugin_stub.abs_directory

    def get_plugin_init(self):
        return os.path.join(self.plugin_stub.abs_directory, "__init__.py")

    def get_wrap_directory(self):
        return os.path.join(self.plugin_stub.abs_directory, ".wrap-c")

    def get_build_directory(self):
        return os.path.join(self.plugin_stub.abs_directory, ".build-c")

    def get_output_directory(self):
        return os.path.join(self.plugin_stub.abs_directory, ".output")

    def get_c_header_filename(self):
        return os.path.join(self.get_wrap_directory(), "madz.h")

    def get_c_code_filename(self):
        return os.path.join(self.get_wrap_directory(), "_madz.c")

    def get_internal_source_files(self):
        return [self.get_c_code_filename()]

    def get_python_code_filename(self):
        return os.path.join(self.get_wrap_directory(), "_madz.py")

    def get_python_outgoing_module(self):
        return os.path.join(self.get_wrap_directory(), "madz.py")

    def get_source_files(self):
        return glob.glob(os.path.join(self.plugin_stub.abs_directory, "*.c"))

    def get_output_file(self):
        return os.path.join(self.get_output_directory(), self.plugin_stub.id.namespace + ".madz")
