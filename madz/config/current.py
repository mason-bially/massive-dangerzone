"""config/current.py
@OffbyOneStudios 2013
A system for managing current config information.
"""

import contextlib

from .base import *

class ConfigWorld(object):
    def __init__(self, config_list=[]):
        self.config_list = config_list

    def copy_state(self):
        return list(self.config_list)

    def set_state(self, state_list):
        self.config_list = state_list

    def save(self):
        return self.get_merged_config()

    def get_merged_config(self):
        return merge(MergedConfig(), *self.config_list)

    def get_option(self, key):
        return self.get_merged_config().get_option(key)

    def get(self, key, default=None):
        option = self.get_option(key)
        return option.get_value() if not (option is None) else default

    def add(self, config):
        self.config_list.append(config)

    def pop(self):
        return self.config_list.pop()

    def remove(self, config_key):
        self.config_list = list(filter(lambda c: c.get_key() != config_key, self.config_list))

    @contextlib.contextmanager
    def and_merge(self, config):
        old_state = self.copy_state()
        self.add(config)
        try:
            yield
        finally:
            self.set_state(old_state)


config = ConfigWorld()