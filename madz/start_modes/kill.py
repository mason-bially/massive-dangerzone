"""madz/start_mode/kill.py
@OffbyOne Studios 2014
Startmode for killing an active daemon.
"""

import sys, os

from ..daemon import Client

def start(argv, system, user_config):
    # TODO: Replace
    res = Client().invoke_daemon("banish")

    print(res)

    if not (len(argv) > 2 and argv[1] == "-r"):
        return
    print()

    print("TODO: Some restart code")
