from typing import Any, Optional, Union

from rdflib import ConjunctiveGraph, Graph
from rdflib.exceptions import ParserError
from rdflib.parser import FileInputSource, InputSource, Parser

from oxrdflib._type import get_mime_type
from oxrdflib.store import OxigraphStore
from oxrdflib.utils.converter import to_ox

__all__ = [
    "OxTurtleParser",
    "OxNTriplesParser",
    "OxRdfXmlParser",
]


class OxParser(Parser):
    def __init__(self):
        pass

    def parse(
        self,
        source: InputSource,
        sink: Union[Graph, ConjunctiveGraph],
        format: str,
        encoding: Optional[str] = "utf-8",
        **kwargs: Any,
    ) -> None:
        if encoding not in [None, "utf-8"]:
            raise ParserError("N3/Turtle files are always utf-8 encoded, I was passed: %s" % encoding)

        if type(source) not in [FileInputSource, InputSource]:
            raise ParserError("Source must be either io(bytes) or io(str) or str or pathlib.Path")

        if not isinstance(sink.store, OxigraphStore):
            raise ParserError(
                "Sink store must be instance of OxigraphStore, " f"got {sink.store.__class__.__name__} store instead"
            )

        base_iri = sink.absolutize(source.getPublicId() or source.getSystemId() or "")

        if kwargs.get("transactional", False):
            sink.store._inner.load(
                source.file,
                format,
                base_iri=base_iri,
                to_graph=to_ox(sink.identifier),
            )
        else:
            sink.store._inner.bulk_load(
                source.file,
                format,
                base_iri=base_iri,
                to_graph=to_ox(sink.identifier),
            )


class OxTurtleParser(OxParser):
    def parse(
        self,
        source: InputSource,
        sink: Graph,
        format: str = get_mime_type("oxTurtle"),
        encoding: Optional[str] = "utf-8",
        **kwargs: Any,
    ) -> None:
        super().parse(source, sink, format, encoding, **kwargs)


class OxNTriplesParser(OxParser):
    def parse(
        self,
        source: InputSource,
        sink: Graph,
        format: str = get_mime_type("oxNTriples"),
        encoding: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        super().parse(source, sink, format, encoding, **kwargs)


class OxRdfXmlParser(OxParser):
    def parse(
        self,
        source: FileInputSource,
        sink: Graph,
        format: str = get_mime_type("oxRdfXml"),
        encoding: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        super().parse(source, sink, format, encoding, **kwargs)


class OxNQuadsParser(OxParser):
    def parse(
        self,
        source: InputSource,
        sink: ConjunctiveGraph,
        format: str = get_mime_type("oxNQuads"),
        encoding: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        raise NotImplementedError("N-Quads is not supported yet")


class OxTriGParser(OxParser):
    def parse(
        self,
        source: InputSource,
        sink: Graph,
        format: str = get_mime_type("oxTriG"),
        encoding: Optional[str] = "utf-8",
        **kwargs: Any,
    ) -> None:
        raise NotImplementedError("TriG parser is not supported yet")
