from nbtoolbox.commands import Command, get_commands, parse_command

source_command = "#! source: hide"
cell_command = "#! cell: hide"
cell_command_simple = "#! collapse"
# two_commands = "#! source: hide output: collapse"


def test_parse_command():
    """test parse_command"""
    command = parse_command(source_command)
    assert command == Command("source", ["hide"])
    command = parse_command(cell_command)
    assert command == Command("cell", ["hide"])
    command = parse_command(cell_command_simple)
    assert command == Command("cell", ["collapse"])
    command = parse_command("#! ")
    assert command is None
    command = parse_command("#! wrong_cell_command")
    assert command is None
    command = parse_command("#! source hide")  # wrong level - need `:`
    assert command is None
    command = parse_command("#! wrong_level: source")
    assert command is None

    # test get_commands
    code, commands = get_commands(source_command)
    assert len(commands) == 1
    assert code == ""
    assert commands[0] == Command("source", ["hide"])

    code, commands = get_commands([source_command, "#! "])
    assert len(commands) == 1
    assert code == ""
    assert commands[0] == Command("source", ["hide"])

    code, commands = get_commands("\n".join([source_command, cell_command]))
    assert len(commands) == 2
    assert code == ""
    assert commands[0] == Command("cell", ["hide"])
    assert commands[1] == Command("source", ["hide"])

    code, commands = get_commands(
        "\n".join([source_command, cell_command, cell_command_simple])
    )
    assert len(commands) == 2
    assert commands[0] == Command("cell", ["hide", "collapse"])
    assert commands[1] == Command("source", ["hide"])

    code, commands = get_commands(source_command + "\nsome code\n")
    assert len(commands) == 1
    assert code == "some code"
    assert commands[0] == Command("source", ["hide"])
