from typing import Any, Optional

from rdflib import Graph
from rdflib.exceptions import ParserError
from rdflib.parser import FileInputSource, InputSource, Parser

from ._type import RDFSerialization
from .utils.converter import to_ox


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
            raise ParserError("N3/Turtle files are always utf-8 encoded, I was passed: %s" % encoding)

        if type(source) not in [FileInputSource, InputSource]:
            raise ParserError("Source must be either io(bytes) or io(str) or str or pathlib.Path")

        base_iri = graph.absolutize(source.getPublicId() or source.getSystemId() or "")

        if kwargs.get("transactional", False):
            graph.store._store.load(
                source.file,
                format,
                base_iri=base_iri,
                to_graph=to_ox(graph.identifier),
            )
        else:
            graph.store._store.bulk_load(
                source.file,
                format,
                base_iri=base_iri,
                to_graph=to_ox(graph.identifier),
            )


class OxTurtleParser(OxParser):
    def parse(
        self,
        source: InputSource,
        graph: Graph,
        format: str = RDFSerialization.OxTurtle.value,
        encoding: Optional[str] = "utf-8",
        **kwargs: Any,
    ) -> None:
        super().parse(source, graph, format, encoding, **kwargs)


class OxNTripleParser(OxParser):
    def parse(
        self,
        source: InputSource,
        graph: Graph,
        format: str = RDFSerialization.OxNTriple.value,
        encoding: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        super().parse(source, graph, format, encoding, **kwargs)


class OxRDFXMLParser(OxParser):
    def parse(
        self,
        source: FileInputSource,
        graph: Graph,
        format: str = RDFSerialization.OxRDFXML.value,
        encoding: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        super().parse(source, graph, format, encoding, **kwargs)


class OxNQuadsParser(OxParser):
    def parse(
        self,
        source: InputSource,
        graph: Graph,
        format: str = RDFSerialization.OxNQuads.value,
        encoding: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        super().parse(source, graph, format, encoding, **kwargs)


class OxTriGParser(OxParser):
    def parse(
        self,
        source: InputSource,
        graph: Graph,
        format: str = RDFSerialization.OxTriG.value,
        encoding: Optional[str] = "utf-8",
        **kwargs: Any,
    ) -> None:
        super().parse(source, graph, format, encoding, **kwargs)
