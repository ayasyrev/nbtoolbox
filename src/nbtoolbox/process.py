from .typing import Nb, CodeCell, MarkdownCell, RawCell, Metadata


def process_nb_metadata(metadata: Metadata) -> Metadata:
    """Process notebook metadata"""
    return metadata


def process_md_cell(cell: MarkdownCell) -> MarkdownCell:
    pass


def process_code_cell(cell: CodeCell) -> CodeCell:
    pass


def process_raw_cell(cell: RawCell) -> RawCell:
    pass


cell_processors = {
    "markdown": process_md_cell,
    "code": process_code_cell,
    "raw": process_raw_cell
}


def process_nb(nb: Nb) -> Nb:
    """Process notebook"""
    process_nb_metadata(nb["metadata"])
    for cell in nb["cells"]:
        cell_processors[cell["cell_type"]](cell)
    return nb
