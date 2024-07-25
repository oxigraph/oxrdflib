from typing import Any, Optional
from rdflib import Graph
from rdflib.parser import FileInputSource, InputSource, Parser
from rdflib.exceptions import ParserError

from .utils.converters import to_ox

from ._types import RDFSerialization


class OxParser(Parser):
    def __init__(self):
        pass

    def parse(
        self,
        source: InputSource,
        graph: Graph,
        format: str,
        encoding: Optional[str] = "utf-8",
        **kwargs: Any,
    ) -> None:
        if encoding not in [None, "utf-8"]:
            raise ParserError(
                "N3/Turtle files are always utf-8 encoded, I was passed: %s" % encoding
            )

        baseURI = graph.absolutize(source.getPublicId() or source.getSystemId() or "")

        if kwargs.get("transactional", False):
            graph.store._store.load(
                source.file,
                format,
                base_iri=baseURI,
                to_graph=to_ox(graph.identifier),
            )
        else:
            graph.store._store.bulk_load(
                source.file,
                format,
                base_iri=baseURI,
                to_graph=to_ox(graph.identifier),
            )


class OxTurtleParser(OxParser):
    def parse(
        self,
        source: InputSource,
        graph: Graph,
        format: Optional[str] = RDFSerialization.oxTurtle.value,
        encoding: Optional[str] = "utf-8",
        **kwargs: Any,
    ) -> None:
        super().parse(source, graph, format, encoding, **kwargs)


class OxNTripleParser(OxParser):
    def parse(
        self,
        source: InputSource,
        graph: Graph,
        format: Optional[str] = RDFSerialization.oxNTriple.value,
        encoding: Optional[str] = "utf-8",
        **kwargs: Any,
    ) -> None:
        super().parse(source, graph, format, encoding, **kwargs)


class OxNQuadsParser(OxParser):
    def parse(
        self,
        source: InputSource,
        graph: Graph,
        format: Optional[str] = RDFSerialization.oxNQuads.value,
        encoding: Optional[str] = "utf-8",
        **kwargs: Any,
    ) -> None:
        super().parse(source, graph, format, encoding, **kwargs)


class OxTriGParser(OxParser):
    def parse(
        self,
        source: InputSource,
        graph: Graph,
        format: Optional[str] = RDFSerialization.oxTriG.value,
        encoding: Optional[str] = "utf-8",
        **kwargs: Any,
    ) -> None:
        super().parse(source, graph, format, encoding, **kwargs)


class OxRDF_XMLParser(OxParser):
    def parse(
        self,
        source: FileInputSource,
        graph: Graph,
        format: Optional[str] = RDFSerialization.oxRDF_XML.value,
        encoding: Optional[str] = "utf-8",
        **kwargs: Any,
    ) -> None:
        super().parse(source, graph, format, encoding, **kwargs)
