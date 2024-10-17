from abc import ABC, abstractmethod
from typing import Optional

from pyoxigraph import DefaultGraph, RdfFormat, parse
from rdflib import Graph
from rdflib.exceptions import ParserError
from rdflib.parser import (
    FileInputSource,
    InputSource,
    Parser,
    URLInputSource,
    create_input_source,
)

from oxrdflib._converter import from_ox, from_ox_graph_name, to_ox
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
        }

        if isinstance(source, URLInputSource):
            source = create_input_source(source.url, format=self._format.file_extension)
        if isinstance(source, FileInputSource):
            args["path"] = source.file.name
        else:
            args["input"] = source.getByteStream()

        if isinstance(sink.store, OxigraphStore):
            if transactional:
                sink.store._inner.load(**args, to_graph=to_ox(sink.identifier))
            else:
                sink.store._inner.bulk_load(**args, to_graph=to_ox(sink.identifier))
        else:
            sink.store.addN(
                (
                    from_ox(quad.subject),
                    from_ox(quad.predicate),
                    from_ox(quad.object),
                    sink
                    if isinstance(quad.graph_name, DefaultGraph)
                    else from_ox_graph_name(quad.graph_name, sink.store),
                )
                for quad in parse(**args)
            )

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
