from pathlib import Path, PosixPath
from typing import Any, Dict, List, Literal, Optional, Protocol, TypeVar, Union, runtime_checkable

PathOrStr = TypeVar("PathOrStr", Path, PosixPath, str)

NbNode = Dict[str, Union[str, int, "NbNode"]]
Metadata = Dict[str, Union[str, int, "Metadata"]]
MultilineText = Union[str, List[str]]


class Output(Protocol):
    output_type: str  # execute_result, display_data, stream, error

    def __getitem__(self, item: str) -> Any:  # pragma: no cover
        ...  # pragma: no cover


class ExecuteResult(Output, Protocol):
    output_type: str = "execute_result"
    data: Dict[str, MultilineText]  # mimebundle - "A mime-type keyed dictionary of data"
    # "Mimetypes with JSON output, can be any type"
    metadata: Metadata
    execution_count: Optional[int]


class DisplayData(Output, Protocol):
    output_type: str = "display_data"
    data: Dict[str, MultilineText]  # fix it - mimebundle
    metadata: Metadata


class Stream(Output, Protocol):
    output_type: str = "stream"
    name: Literal["stdout", "stderr"]  # "The name of the stream (stdout, stderr)."
    text: MultilineText


class Error(Output, Protocol):
    output_type: str = "error"
    ename: str  # "The name of the error."
    evalue: str  # "The value, or message, of the error."
    traceback: List[str]


@runtime_checkable
class Cell(Protocol):
    """Notebook cell protocol."""

    id: int  # from nbformat 4.5
    cell_type: str
    metadata: Metadata
    source: MultilineText
    # attachments: Optional[Dict[str, MultilineText]]


class CodeCell(Cell, Protocol):
    """Code_cell protocol."""

    cell_type = "code"
    outputs: List[Output]
    execution_count: Optional[int]


class MarkdownCell(Cell, Protocol):
    """Markdown_cell protocol."""

    cell_type = "markdown"


class RawCell(Cell, Protocol):
    """Raw_cell protocol."""

    cell_type = "raw"


@runtime_checkable
class Nb(Protocol):
    """Notebook protocol."""

    nbformat: int
    nbformat_minor: int
    cells: List[Cell]
    metadata: Metadata
