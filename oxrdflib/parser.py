import warnings
from typing import Any, Optional, Union

from rdflib import ConjunctiveGraph, Graph
from rdflib.exceptions import ParserError
from rdflib.parser import FileInputSource, InputSource, Parser

from oxrdflib._converter import to_ox
from oxrdflib.store import OxigraphStore

__all__ = [
    "OxigraphTurtleParser",
    "OxigraphNTriplesParser",
    "OxigraphRdfXmlParser",
]


class OxigraphParser(Parser):
    def __init__(self):
        pass

    def parse(
        self,
        source: InputSource,
        sink: Graph,
        format: str,
        encoding: Optional[str] = "utf-8",
        **kwargs: Any,
    ) -> None:
        if encoding not in (None, "utf-8"):
            raise ParserError("N3/Turtle files are always utf-8 encoded, I was passed: %s" % encoding)

        if type(source) not in (FileInputSource, InputSource):
            raise ParserError("Source must be either io(bytes) or io(str) or str or pathlib.Path")

        if not isinstance(sink.store, OxigraphStore):
            warnings.warn(
                "Graph store should be an instance of OxigraphStore, "
                f"got {type(sink.store).__name__} store instead."
                " Attempting to parse using rdflib native parser.",
                stacklevel=2,
            )
            sink.parse(source, format=format)

        else:
            base_iri = sink.absolutize(source.getPublicId() or source.getSystemId() or "")
            input = source.file if isinstance(source, FileInputSource) else source.getByteStream()

            if kwargs.get("transactional", True):
                sink.store._inner.load(
                    input,
                    format,
                    base_iri=base_iri,
                    to_graph=to_ox(sink.identifier),
                )
            else:
                sink.store._inner.bulk_load(
                    input,
                    format,
                    base_iri=base_iri,
                    to_graph=to_ox(sink.identifier),
                )


class OxigraphTurtleParser(OxigraphParser):
    def parse(
        self,
        source: InputSource,
        sink: Graph,
        format: str = "text/turtle",
        encoding: Optional[str] = "utf-8",
        **kwargs: Any,
    ) -> None:
        super().parse(source, sink, format, encoding, **kwargs)


class OxigraphNTriplesParser(OxigraphParser):
    def parse(
        self,
        source: InputSource,
        sink: Graph,
        format: str = "application/n-triples",
        encoding: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        super().parse(source, sink, format, encoding, **kwargs)


class OxigraphRdfXmlParser(OxigraphParser):
    def parse(
        self,
        source: FileInputSource,
        sink: Graph,
        format: str = "application/rdf+xml",
        encoding: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        super().parse(source, sink, format, encoding, **kwargs)


class OxigraphNQuadsParser(OxigraphParser):
    def parse(
        self,
        source: InputSource,
        sink: ConjunctiveGraph,
        format: str = "application/n-quads",
        encoding: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        raise NotImplementedError("N-Quads is not supported yet")


class OxigraphTriGParser(OxigraphParser):
    def parse(
        self,
        source: InputSource,
        sink: Graph,
        format: str = "application/trig",
        encoding: Optional[str] = "utf-8",
        **kwargs: Any,
    ) -> None:
        raise NotImplementedError("TriG parser is not supported yet")
