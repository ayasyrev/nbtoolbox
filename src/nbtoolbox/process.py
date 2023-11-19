import copy
from typing import Optional

from .typing import Cell, CodeCell, Metadata, MultilineText, Nb, Output


def process_nb_metadata(metadata: Metadata) -> Metadata:
    """Process notebook metadata"""
    return metadata


def process_md_cell(cell: Cell) -> Cell:
    return cell


def process_source(source: MultilineText) -> str:
    if isinstance(source, str):
        return source
    else:
        return "\n".join(source)


def process_output(output: Output) -> Output:
    return output


def process_code_cell(cell: CodeCell) -> CodeCell:
    cell["source"] = process_source(cell["source"])
    cell["outputs"] = [process_output(output) for output in cell["outputs"]]
    return cell


class Processor:
    _nb: Nb  # place to store copy of last processed Nb

    def __init__(
        self,
        cfg: Optional[dict] = None,
    ):
        self.cfg = cfg or {}
        self.cell_processors = {
            "markdown": process_md_cell,
            "code": process_code_cell,
            "raw": process_md_cell,
        }

    def run(self, nb: Nb) -> Nb:
        """Process notebook"""
        self._nb = copy.deepcopy(nb)
        process_nb_metadata(nb["metadata"])  # to do: class method or plugin
        for cell in nb["cells"]:
            self.cell_processors[cell["cell_type"]](cell)
        return nb
