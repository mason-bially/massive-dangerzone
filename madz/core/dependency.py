"""dependency.py
@OffbyOneStudios 2013
Code to create and traverse dependency graphs of plugins.
"""

import logging
import os.path, time

from ..fileman import *

logger = logging.getLogger(__name__)

class Dependency(object):
    """Generates a dependency graph of plugins allowing for generation in the correct order.
    
    Attributes:
        dependencies: A list of strings, naming files for which there is a dependency.
        targets: A list of strings, naming files for which are dependent on the dependencies.
    """

    def __init__(self, dependencies, targets):
        self.dependencies = dependencies
        self.targets = targets
        self._has_checked = False

    def check(self):
        """Checks that there are no targets which are older than the dependencies."""
        newest_dependency = 0

        #Find the newest dependency
        for d in self.dependencies:
            if isinstance(d,File):
                temp = d.modify_date
                if not temp is None and temp > newest_dependency:
                    newest_dependency = temp

        unsatisfied_targets = []

        #Verify each target is newer than the newest dependency, add targets
        #which are older than their dependences to the unsatisfied_targets list
        for t in self.targets:
            if isinstance(t, File) and t.exists():
                if t.modify_date <= newest_dependency:
                    unsatisfied_targets.append(t)
            else:
                unsatisfied_targets.append(t)
        self._unsatisfied_targets = unsatisfied_targets

        self._has_checked = True

    def __bool__(self):
        """Returns true if there are 0 unsatisfied targets in the Dependency."""
        if not self._has_checked:
            self.check()
        if len(self._unsatisfied_targets) == 0:
            return True
        else:
            logger.debug("Dependency failed: {}".format(self._unsatisfied_targets))
            return False

    __nonzero__ = __bool__

    def get_unsatisfied_targets(self):
        """Returns the list of all targets which are older than one of the dependencies."""
        if not self._has_checked:
            self.check()
        return self._unsatisfied_targets

"""
#Example Usage of Dependency

Dep = Dependency(["loader.py"],["builder.py"])

print(Dep.get_unsatisfied_targets())

if Dep:
    print("hi")
"""
