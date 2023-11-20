"""Sign notebook."""
import configparser
from pathlib import Path
from typing import Optional

from .core import read_nb, write_nb
from .typing import Author, Nb, PathOrStr


def read_config(path: Optional[PathOrStr] = None) -> configparser.ConfigParser:
    """Read name config."""

    config_path = (
        Path("~/.config/nbtoolbox.ini").expanduser() if path is None else Path(path)
    )
    assert config_path.exists(), f"{config_path} not exists!"
    config = configparser.ConfigParser()
    config.read(config_path)
    return config


def get_author(path: Optional[PathOrStr] = None) -> Author:
    """Return author from config."""
    config = read_config(path)
    return dict(config["author"].items())  # type: ignore  # Expecting Author but may be any str.


def check_author_exist(nb: Nb, author: Author) -> bool:
    """Check if author exist."""
    authors = nb["metadata"].get("authors")
    if not authors:
        return False
    return author in authors  # todo: check all keys, values


def sign_nb(nb: Nb, config_path: Optional[PathOrStr] = None) -> bool:
    """Sign notebook."""
    author = get_author(config_path)
    if not nb["metadata"].get("authors"):
        nb["metadata"]["authors"] = [author]
        return True
    if not check_author_exist(nb, author):
        nb["metadata"]["authors"].append(author)
        return True
    return False


def sign_nb_file(path: str, config_path: Optional[PathOrStr] = None) -> bool:
    """Sign notebook file."""
    nb = read_nb(path)
    result = sign_nb(nb, config_path)
    if result:
        write_nb(nb, path)
    return result
