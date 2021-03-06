
import abc
import os

from ...config import *
from ...config.language import *

from ...fileman import *

class BaseLanguage(metaclass=abc.ABCMeta):
    """Base language object."""
    
    # madz fileman interface
    @classmethod
    def madz_folder_name(self):
        return ".output"

    @property
    def name(self):
        return self.get_language_name()

    @abc.abstractmethod
    def get_language_name(self):
        """Returns the string name of language."""
        pass

    def __init__(self, plugin_stub):
        self.plugin_stub = plugin_stub

    def get_compiler_name(self, default):
        """Returns the compiler name of the object."""
        return config.get(OptionCompilerPreference, default)

    def get_compiler(self):
        """Returns the compiler object being used on the language."""
        compiler_name = self.get_compiler_name(self.default_compiler)
        with config.and_merge(config.get_option(CompilerConfig.make_key(compiler_name))):
            return self.compilers[compiler_name](self)

    @abc.abstractmethod
    def make_cleaner(self):
        pass

    @abc.abstractmethod
    def make_builder(self):
        pass

    @abc.abstractmethod
    def make_wrapper(self):
        pass

    def supported_extensions(self):
        return []

    def get_plugin_description_files(self):
        """Returns the names of the plugin description files attached to the language."""
        foo = self.plugin_stub.description.ast
        return self.plugin_stub._plugin_loader_files

    @property
    def output_directory(self):
        """Returns the path of the output directory."""
        return self.plugin_stub.directory.madz().dir(".output")

    def get_output_file(self):
        """Retruns the path of the output file."""
        return self.output_directory.file("{}.madz".format(self.plugin_stub.id.namespace))

