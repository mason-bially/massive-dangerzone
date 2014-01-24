"""language.py
@OffbyoneStudios 2013
languages/python
The language object pulling togeather all of the pieces needed for a plugin of this language.
"""

import os
import glob

from ...compiler import mingw_compiler
from ...config import *
from .._base import language
from .._base.compiler import NewCompilerWrapper
from . import clean
from . import load
from . import compiler_gcc, compiler_mingw, compiler_clang, compiler_cl
from . import wrapgen

class LanguagePy(language.BaseLanguage):
    """Python language object."""

    compilers = {
        "gcc": compiler_gcc.GCCCompiler,
        "mingw": NewCompilerWrapper(mingw_compiler.MingwCompiler),
        "clang": compiler_clang.ClangCompiler,
        "cl": compiler_cl.MSCLCompiler,
    }
    default_compiler = "gcc"

    @property
    def name(self):
        return "c"

    def get_language_name(self):
        """Returns the language name."""
        return "python"

    def get_language_path(self):
        """Returns the path to the language libararies."""
        return os.path.dirname(__file__)

    def make_cleaner(self):
        """Creates the cleaner."""
        return clean.Cleaner(self)

    def make_loader(self):
        """Creates the loader."""
        return load.Loader(self)

    def make_builder(self):
        """Creates the builder."""
        return self.get_compiler()

    def make_wrapper(self):
        """Creates the wrapper."""
        return wrapgen.WrapperGenerator(self)

    def get_root_directory(self):
        """Returns the path to the root directory of the plugin."""
        return self.plugin_stub.directory

    def get_plugin_init(self):
        """Returns the path to the init file of the plugin."""
        return os.path.join(self.plugin_stub.directory, "__init__.py")

    def get_wrap_directory(self):
        """Returns the path to the directory of the wrapper."""
        return os.path.join(self.plugin_stub.directory, ".wrap-c")

    def get_build_directory(self):
        """Returns the path to the directory of the builder."""
        return os.path.join(self.plugin_stub.directory, ".build-c")

    def get_c_header_filename(self):
        """Returns the path to the madz c header file."""
        return os.path.join(self.get_wrap_directory(), "madz.h")

    def get_c_code_filename(self):
        """Returns the path to the madz c code file."""
        return os.path.join(self.get_wrap_directory(), "_madz.c")

    def get_internal_source_files(self):
        """Returns a list of the internal source files."""
        return [self.get_c_code_filename()]

    def get_python_code_filename(self):
        """Returns the path to the madz pythong code file."""
        return os.path.join(self.get_wrap_directory(), "_madz.py")

    def get_python_autogenerated_module(self):
        """Returns the path to the madz autogenerated module."""
        return os.path.join(self.get_wrap_directory(), "madz.py")

    def get_source_files(self):
        """"Returns a list of the source files."""
        return glob.glob(os.path.join(self.plugin_stub.directory, "*.c"))

