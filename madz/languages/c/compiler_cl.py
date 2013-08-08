
import os
import logging

from .._base import subproc_compiler as base

logger = logging.getLogger(__name__)

class MSCLCompiler(base.SubprocCompilerBase):
    def __init__(self, language, compiler_config):
        base.SubprocCompilerBase.__init__(self, language, compiler_config)

    def file_extension_binary_object(self):
        return ".obj"

    def binary_name_binary_compiler(self):
        return "cl"

    def binary_name_shared_linker(self):
        return "LINK"

    def args_binary_compile(self, source_files):
        return [self.binary_name_compiler(), "/c", "/I"+self.language.get_wrap_directory(),] + list(source_files)

    def args_shared_link(self, object_files):
        return [self.binary_name_shared_linker(), "/DLL ", "/OUT:"+self.language.get_output_file()] + list(object_files)

    def log_output(self, retcode, output, errput, foutput, ferrput):

        if output.find("error") != -1:
            logger.error(foutput)
        if errput.find("cl : Command line warning") != -1:
            logger.warning(ferrput)


