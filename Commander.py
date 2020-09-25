#  Copyright (c) 2020.
from treelib import Node, Tree
from typing import Optional

import logging
import shlex


class Commander(object):
    def __init__(
            self,
            caller: Optional[str] = "",
            ignore_command_not_found: Optional[bool] = False
    ):
        """
        Commander
        :param caller: Prefix
        :param ignore_command_not_found:
        """
        self.tree = Tree()
        self.caller = caller
        self.tree.create_node(self.caller, self.caller)
        self.ignore_command_not_found = ignore_command_not_found
        self.command = []

    class Command(object):
        def __init__(
                self,
                func,
                name: Optional[str] = None,
                names: Optional[list] = None,
        ):
            """
            Command Object. Please use Commander.register() or decorator @Commander()
            :param func: Function to be called.
            :param name: Function name
            :param names: Function names
            """
            self.name = [func.__name__]
            if name is not None and names is not None:
                self.name.append(str) if type(name) == str else self.name.extend(name)
            self.func = func

    def __call__(
            self,
            name: str = None,
            names: list = None
    ):
        """
        Decorator that register function to command.
        :param name: Name.
        :param names: Name list.
        :return: Decorator.
        """
        def decorator(func):
            c = self.Command(func, name, names)
            self.command.append(c)
            self.tree.create_node(c.name[0], c.name[0], parent=self.caller)

        return decorator

    def register(
            self,
            func: function,
            name: str = None,
            names: list = None
        ):
        """
        Register function to command. Same usage as
        :param func: Function to be registered.
        :param name: Function Name.
        :param names: Function Names.
        :return: None
        """
        c = self.Command(func, name, names)
        self.command.append(c)
        self.tree.create_node(c.name[0], c.name[0], parent=self.caller)

    class CommandNotFoundException(Exception):
        pass

    def _run(self, cmd: list, c: Command):
        """
        Please use Commander.run() instead of this function.
        :param cmd: Command list (Split)
        :param c: Command Object
        :return: None
        """
        try:
            c.func(*cmd[1:]) if len(cmd) != 1 else c.func()
        except Exception as err:
            print(logging.warning(
                f"Ignoring the following exception {err.__class__.__name__} in command {c.name}:\n"
                f"{err}"
            ))

    def run(
        self,
        cmd: str
    ):
        """
        Split the command and call it.
        :param cmd: Command to be run.
        :return: None
        """
        if cmd.startswith(self.caller):
            cmd = shlex.split(cmd)
            for c in self.command:
                if cmd[0].replace(self.caller, "") in c.name:
                    self._run(cmd, c)

        print(logging.warning(
            f"Command {cmd[0].replace(self.caller, '')} not found.")) if self.ignore_command_not_found else None
