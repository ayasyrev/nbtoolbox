"""Jupyter notebook types with protocol."""
import collections
from pathlib import Path, PosixPath
from typing import (
    Any,
    Dict,
    List,
    Literal,
    Optional,
    Protocol,
    Tuple,
    TypeVar,
    Union,
    runtime_checkable,
)

__all__ = [
    "PathOrStr",
    "Metadata",
    "Source",
    "Output",
    "ExecuteResult",
    "DisplayData",
    "Stream",
    "Error",
    "Cell",
    "CodeCell",
    "MarkdownCell",
    "RawCell",
    "Nb",
    "ResourcesDict",
    "NbAndResources",
    "CellAndResources",
    "TPreprocessor",
]
PathOrStr = TypeVar("PathOrStr", Path, PosixPath, str)

Metadata = Dict[str, Union[str, int, "Metadata"]]  # temp
Source = str  # at nbformat schema: multiline_string -> List[str]. But after read nb we got str.
# Output = TypeVar("Output")


# from nbconvert.exporters.exporter
class ResourcesDict(collections.defaultdict):
    """A default dict for resources."""

    def __missing__(self, key):
        """Handle missing value."""
        return ""


class Output(Protocol):
    """Default class for outputs. Dict like object."""
    output_type: str  # execute_result, display_data, stream, error

    def __getitem__(self, item: str) -> Any:  # pragma: no cover
        ...  # pragma: no cover


class ExecuteResult(Output, Protocol):
    output_type: str = "execute_result"
    data: str  # mimebundle - "A mime-type keyed dictionary of data"
    # "Mimetypes with JSON output, can be any type"
    metadata: Metadata
    execution_count: Optional[int]


class DisplayData(Output, Protocol):
    output_type: str = "display_data"
    data: str  # mimebundle
    metadata: Metadata


class Stream(Output, Protocol):
    output_type: str = "stream"
    name: str  # "The name of the stream (stdout, stderr)."
    text: str


class Error(Output, Protocol):
    output_type: str = "error"
    ename: str  # "The name of the error."
    evalue: str  # "The value, or message, of the error."
    traceback: List[str]


@runtime_checkable
class Cell(Protocol):
    """Notebook cell protocol."""

    id: int  # check
    cell_type: str
    metadata: Metadata
    source: Source


class CodeCell(Cell, Protocol):
    """Code_cell protocol."""

    cell_type: Literal["code"] = "code"
    outputs: List[Output]
    execution_count: Optional[int]


class MarkdownCell(Cell, Protocol):
    """Markdown_cell protocol."""

    cell_type: Literal["markdown"] = "markdown"


class RawCell(Cell, Protocol):
    """Raw_cell protocol."""

    cell_type: Literal["raw"] = "raw"


@runtime_checkable
class Nb(Protocol):
    """Notebook protocol."""

    nbformat: int
    nbformat_minor: int
    cells: List[Cell]
    metadata: Metadata


NbAndResources = Tuple[Nb, ResourcesDict]
CellAndResources = Tuple[Cell, ResourcesDict]


# TPreprocessor = Callable[[Nb, ResourcesDict], NbAndResources]
class TPreprocessor(Protocol):
    """Preprocessor protocol."""

    def __init__(self, **kw) -> None:
        pass  # pragma: no cover

    def __call__(self, nb: Nb, resources: ResourcesDict) -> NbAndResources:
        ...  # pragma: no cover

    def preprocess(self, nb: Nb, resources: ResourcesDict) -> NbAndResources:
        ...  # pragma: no cover

    def preprocess_cell(self, cell: Cell, resources: ResourcesDict, index: int) -> CellAndResources:
        ...  # pragma: no cover
