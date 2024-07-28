import warnings
from typing import Any, Optional

from rdflib import ConjunctiveGraph, Graph
from rdflib.exceptions import ParserError
from rdflib.parser import (
    FileInputSource,
    InputSource,
    Parser,
    URLInputSource,
    create_input_source,
)

from oxrdflib._converter import ox_to_rdflib_type, rdflib_to_mime_type, to_ox
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

        if not isinstance(sink.store, OxigraphStore):
            warnings.warn(
                "Graph store should be an instance of OxigraphStore, "
                f"got {type(sink.store).__name__} store instead."
                " Attempting to parse using rdflib native parser.",
                stacklevel=2,
            )
            sink.parse(source, format=ox_to_rdflib_type(format))

        else:
            base_iri = sink.absolutize(source.getPublicId() or source.getSystemId() or "")

            if isinstance(source, FileInputSource):
                input = source.file
            elif isinstance(source, URLInputSource):
                input = create_input_source(source.url, format=ox_to_rdflib_type(format)).getByteStream()
            else:
                input = source.getByteStream()

            if kwargs.get("transactional", True):
                sink.store._inner.load(
                    input,
                    rdflib_to_mime_type(ox_to_rdflib_type(format)),
                    base_iri=base_iri,
                    to_graph=to_ox(sink.identifier),
                )
            else:
                sink.store._inner.bulk_load(
                    input,
                    rdflib_to_mime_type(ox_to_rdflib_type(format)),
                    base_iri=base_iri,
                    to_graph=to_ox(sink.identifier),
                )


class OxigraphTurtleParser(OxigraphParser):
    def parse(
        self,
        source: InputSource,
        sink: Graph,
        format: str = "ox-turtle",
        encoding: Optional[str] = "utf-8",
        **kwargs: Any,
    ) -> None:
        super().parse(source, sink, format, encoding, **kwargs)


class OxigraphNTriplesParser(OxigraphParser):
    def parse(
        self,
        source: InputSource,
        sink: Graph,
        format: str = "ox-n3",
        encoding: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        super().parse(source, sink, format, encoding, **kwargs)


class OxigraphRdfXmlParser(OxigraphParser):
    def parse(
        self,
        source: FileInputSource,
        sink: Graph,
        format: str = "ox-xml",
        encoding: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        super().parse(source, sink, format, encoding, **kwargs)


class OxigraphNQuadsParser(OxigraphParser):
    def parse(
        self,
        source: InputSource,
        sink: ConjunctiveGraph,
        format: str,
        encoding: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        raise NotImplementedError("N-Quads is not supported yet")


class OxigraphTriGParser(OxigraphParser):
    def parse(
        self,
        source: InputSource,
        sink: Graph,
        format: str,
        encoding: Optional[str] = "utf-8",
        **kwargs: Any,
    ) -> None:
        raise NotImplementedError("TriG parser is not supported yet")
