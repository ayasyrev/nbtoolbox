import copy
from pathlib import Path

from nbtoolbox.core import read_nb, write_nb
from nbtoolbox.sign import check_author_exist, get_author, sign_nb, sign_nb_file

test_config = "tests/nbtoolbox_config.ini"
test_author = {"name": "Andrei", "github": "https://github.com/ayasyrev"}


def test_get_author() -> None:
    author = get_author(test_config)
    assert author == test_author


def test_sign_nb() -> None:
    test_nb = read_nb("tests/test_nbs/test_nb_1.ipynb")
    nb = copy.deepcopy(test_nb)
    nb["metadata"]["authors"] = []

    assert not check_author_exist(nb, test_author)

    result = sign_nb(nb, test_config)
    assert result
    assert nb["metadata"]["authors"] == [test_author]

    assert check_author_exist(nb, test_author)
    # try sign signed
    result = sign_nb(nb, test_config)
    assert not result

    # nb with other author
    nb["metadata"]["authors"] = [{"name": "Someone"}]
    assert not check_author_exist(nb, test_author)

    result = sign_nb(nb, test_config)
    assert result
    assert nb["metadata"]["authors"] == [{"name": "Someone"}, test_author]


def test_sign_nb_file(tmp_path: Path):
    """test sign notebook file"""
    file = Path("tests/test_nbs/test_nb_1.ipynb")
    nb = read_nb(file)
    nb_name = "test.ipynb"
    nb["metadata"]["authors"] = []
    write_nb(nb, tmp_path / nb_name)
    test_nb = read_nb(tmp_path / nb_name)
    assert not check_author_exist(test_nb, test_author)

    result = sign_nb_file(tmp_path / nb_name, test_config)
    assert result

    # try sign signed
    result = sign_nb_file(tmp_path / nb_name, test_config)
    assert not result
