import warnings
from abc import ABC, abstractmethod
from typing import Optional

from pyoxigraph import RdfFormat
from rdflib import Graph
from rdflib.exceptions import ParserError
from rdflib.parser import (
    FileInputSource,
    InputSource,
    Parser,
    URLInputSource,
    create_input_source,
)

from oxrdflib._converter import to_ox
from oxrdflib.store import OxigraphStore

__all__ = [
    "OxigraphN3Parser",
    "OxigraphTurtleParser",
    "OxigraphNTriplesParser",
    "OxigraphRdfXmlParser",
    "OxigraphTriGParser",
    "OxigraphNQuadsParser",
]


class _OxigraphParser(Parser, ABC):
    def parse(
        self,
        source: InputSource,
        sink: Graph,
        *,
        encoding: Optional[str] = "utf-8",
        transactional: bool = True,
    ) -> None:
        if encoding not in (None, "utf-8"):
            raise ParserError(f"Only the 'utf-8' encoding is supported, '{encoding}' given")
        base_iri = sink.absolutize(source.getPublicId() or source.getSystemId() or "")
        args = {
            "format": self._format,
            "base_iri": base_iri,
            "to_graph": to_ox(sink.identifier),
        }
        if isinstance(source, URLInputSource):
            source = create_input_source(source.url, format=self._format.file_extension)
        if isinstance(source, FileInputSource):
            args["path"] = source.file.name
        else:
            args["input"] = source.getByteStream()

        if isinstance(sink.store, OxigraphStore):
            if transactional:
                sink.store._inner.load(**args)
            else:
                sink.store._inner.bulk_load(**args)
        else:
            warnings.warn(
                "Graph store should be an instance of OxigraphStore, "
                f"got {type(sink.store).__name__} store instead."
                " Attempting to parse using rdflib native parser.",
                stacklevel=2,
            )
            sink.parse(source)

    @property
    @abstractmethod
    def _format(self) -> RdfFormat:
        pass


class OxigraphTurtleParser(_OxigraphParser):
    _format = RdfFormat.TURTLE


class OxigraphNTriplesParser(_OxigraphParser):
    _format = RdfFormat.N_TRIPLES


class OxigraphRdfXmlParser(_OxigraphParser):
    _format = RdfFormat.RDF_XML


class OxigraphN3Parser(_OxigraphParser):
    _format = RdfFormat.N3


class OxigraphNQuadsParser(_OxigraphParser):
    _format = RdfFormat.N_QUADS


class OxigraphTriGParser(_OxigraphParser):
    _format = RdfFormat.TRIG
