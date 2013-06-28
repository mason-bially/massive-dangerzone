"""plugin.py
@OffbyOne Studios 2013
Code for plugin description objects
"""

import re
import nodes, base_types

class Plugin(object):
    """Object Containing description of Plugins.

    Associated with __plugin__.py files, which describe plugins.

    Attributes:
        name: String name of plugin
        version: Version of plugin
        implementation_name: String name of particular implementation of plugin interface
        language: langauge that implementation is written in
        imports: Plugins that this plugin makes use of
        depends: Plugins that this plugin require, usually providing some functionality on said plugins
        declarations: Dict of Type and Function declarations associated with this plugin
        variables: Dict Variable delcarations which require space to be allocated.
    """
    def __init__(self, **kwargs):
        self._args = kwargs

        def init_get(key, default=None):
            return self._args.get(key, default)

        self.name = init_get("name")
        self.version = init_get("version")
        self.implementation_name = init_get("implementation_name")

        self.language = init_get("language")

        self.imports = init_get("imports",[])
        self.depends = init_get("depends",[])

        self.description = init_get("description",[])


class PluginDescription(object):
    """Data Structure for Declarations and Variables."""

    def __init__(self, ast, dependencies):
        """Constructor for PluginDescription helper class.

        Args:
            ast: A list of nodes which build a description of the plugin.
            dependencies: Dict which maps namespaces to other plugin description objects.
        """
        self.ast = ast
        self.dependencies = dependencies

        def str_to_named(node, name=""):
            ret_node = node
            if isinstance(node, basestring):
                ret_node = base_types.NamedType(node)
            if name:
                return [(name, ret_node)]
            return [ret_node]

        self.ast = self.map_over(str_to_named)


    @staticmethod
    def split_namespace(stringname):
        """Splits stringname into namespace,symbol pair
        args:
            stringname: fully qualified name of symbol

        returns: (namespace, syombol) string pair.

        """
        split_name = stringname.split(".")
        end_name = split_name[-1]
        namespace = ".".join(split_name[:-1])
        return (namespace, end_name)

    def declarations(self):
        """Filters the root AST for nodes declaring new types or other information that arn't variables."""
        return filter(lambda n: isinstance(n, nodes.Declaration), self.ast)

    def definitions(self):
        """Filters the root AST for nodes defining new variables or other information that arn't declarations."""
        return filter(lambda n: isinstance(n, nodes.Definition), self.ast)

    def get_context(self, namespace):
        if namespace == "":
            return self
        return self.dependencies[namespace]

    def get_types_of(self, the_type):
        """Returns dict of all declarations matching given type.

            Args:
                the_type: plugin_type.TypeType or a subclass

            Returns:
                List of TypeDeclarations which match the type.
        """
        return filter(lambda n: isinstance(n, nodes.TypeDeclaration) and n.type == the_type, self.ast)

    def get_root_node(self, namespace, test_func):
        """Getter for type declarations.

        Args:
            stringname: string containing name of declaration.
        """
        if namespace == "":
            for n in self.ast:
                if test_func(n):
                    return n
        else:
            # TODO Exception Checking
            return self.dependencies[namespace].get_root_node("", test_func)

    _symbol_regex = re.compile("^[A-Za-z][A-Za-z_0-9]*$")

    @classmethod
    def is_valid_symbol(cls, symbol):
        return not (cls._symbol_regex.search(symbol) is None)

    def validate(self):
        """Checks for valid declarations."""
        namespaces = {}
        for node in self.ast:
            if not (isinstance(node, nodes.Declaration) or isinstance(node, nodes.Definition)):
                print "VALIDATION: Root node is not declaration or definition."
                return False

            namespacekey = node.get_namespace_key()
            if not (namespacekey in namespaces):
                namespaces[namespacekey] = set()
            
            if node.name in namespaces[namespacekey]:
                print "VALIDATION: Multiple names in namespace."
                return False
            namespaces[namespacekey].add(node.name)

            if not (node.validate(self)):
                return "VALIDATION: Node is not validated."
                return False

        return True

    def map_over(self, map_func):
        new_ast = []
        for node in self.ast:
            new_subs = map_func(node)
            for new_sub_node in new_subs:
                new_ast.append(new_sub_node.map_over(map_func))
        return new_ast


