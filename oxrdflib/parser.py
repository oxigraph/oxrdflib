import warnings
from typing import Any, Optional

from rdflib import Graph
from rdflib.exceptions import ParserError
from rdflib.parser import (
    FileInputSource,
    InputSource,
    Parser,
    URLInputSource,
    create_input_source,
)

from oxrdflib._converter import guess_rdf_format, ox_to_rdflib_type, to_ox
from oxrdflib.store import OxigraphStore

__all__ = [
    "OxigraphTurtleParser",
    "OxigraphNTriplesParser",
    "OxigraphRdfXmlParser",
]


class OxigraphParser(Parser):
    def parse(
        self,
        source: InputSource,
        sink: Graph,
        format: str,
        encoding: Optional[str] = "utf-8",
        **kwargs: Any,
    ) -> None:
        if encoding not in (None, "utf-8"):
            raise ParserError("N3/Turtle files are always utf-8 encoded, I was passed: {encoding}")

        if not isinstance(sink.store, OxigraphStore):
            warnings.warn(
                "Graph store should be an instance of OxigraphStore, "
                f"got {type(sink.store).__name__} store instead."
                " Attempting to parse using rdflib native parser.",
                stacklevel=2,
            )
            sink.parse(source, format=ox_to_rdflib_type(format))
            return

        base_iri = sink.absolutize(source.getPublicId() or source.getSystemId() or "")

        args = {
            "format": guess_rdf_format(format),
            "base_iri": base_iri,
            "to_graph": to_ox(sink.identifier),
        }
        if isinstance(source, URLInputSource):
            source = create_input_source(source.url, format=ox_to_rdflib_type(format))
        if isinstance(source, FileInputSource):
            args["path"] = source.file.name
        else:
            args["input"] = source.getByteStream()

        if kwargs.get("transactional", True):
            sink.store._inner.load(**args)
        else:
            sink.store._inner.bulk_load(**args)


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
        format: str = "ox-nt",
        encoding: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        super().parse(source, sink, format, encoding, **kwargs)


class OxigraphRdfXmlParser(OxigraphParser):
    def parse(
        self,
        source: InputSource,
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
        sink: Graph,
        format: str = "ox-nquads",
        encoding: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        super().parse(source, sink, format, encoding, **kwargs)


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
