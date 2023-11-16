# Commands for process cells.
# Expecting commands at line starts with #!
# Lines started with ## processed as hidden comments.

# First version - one command per line.
# cell command may start from `code:` or just cell command.
from __future__ import annotations

from collections import defaultdict
from enum import Enum
from typing import NamedTuple, Optional


class CommandLevel(Enum):
    CELL = "cell"
    SOURCE = "source"
    OUTPUT = "output"


COMMAND_LEVEL_VALUES = tuple(command_level.value for command_level in CommandLevel)


class CellCommand(Enum):
    HIDE = "hide"
    COLLAPSE = "collapse"
    COLLAPSIBLE = "collapsible"


CELL_COMMAND_VALUES = tuple(cell_command.value for cell_command in CellCommand)


class Command(NamedTuple):
    level: CommandLevel
    commands: list[str]


def get_commands(text: str) -> list[Command]:
    """Parse text for commands.
    return list of commands"""
    command_lines = []
    text_lines = text.splitlines()
    for line in text_lines:
        if line.startswith("#!"):
            command_lines.append(line)
    commands = defaultdict(list)
    for line in command_lines:
        command = parse_command(line)
        if command is not None:
            commands[command.level].append(command)

    return list(
        Command(level.value, [cmd.commands[0] for cmd in commands[level.value]])
        for level in CommandLevel
        if level.value in commands
    )


def parse_command(line: str) -> Optional[Command]:
    """Parse line with command"""
    if ":" in line:
        level, command = line[2:].split(":")
        level = level.strip()
        if level in COMMAND_LEVEL_VALUES:
            return Command(level=level, commands=[command.strip()])
    else:
        command = line[2:].strip()
        if command in CELL_COMMAND_VALUES:
            return Command(level="cell", commands=[command])
    return None
