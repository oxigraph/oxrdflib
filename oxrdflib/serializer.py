from abc import ABC, abstractmethod
from typing import IO, Any, Optional

from pyoxigraph import RdfFormat, serialize
from rdflib import Dataset
from rdflib.serializer import Serializer

from oxrdflib._converter import to_ox
from oxrdflib.store import OxigraphStore

__all__ = [
    "OxigraphN3Serializer",
    "OxigraphTurtleSerializer",
    "OxigraphNTriplesSerializer",
    "OxigraphRdfXmlSerializer",
    "OxigraphTriGSerializer",
    "OxigraphNQuadsSerializer",
]


class _OxigraphSerializer(Serializer, ABC):
    def serialize(
        self,
        stream: IO[bytes],
        base: Optional[str] = None,
        encoding: Optional[str] = None,
        **kwargs: Any,  # noqa: ARG002
    ) -> None:
        if encoding not in (None, "utf-8"):
            raise ValueError(f"RDF files are always utf-8 encoded, I was passed: {encoding}")
        base_iri = base or self.store.base
        prefixes = dict(self.store.namespaces())
        if isinstance(self.store.store, OxigraphStore):
            self.store.store._inner.dump(
                stream,
                format=self._format,
                from_graph=None if isinstance(self.store, Dataset) else to_ox(self.store.identifier),
                base_iri=base_iri,
                prefixes=prefixes,
            )
        else:
            serialize((to_ox(q) for q in self.store), stream, format=self._format, base_iri=base_iri, prefixes=prefixes)

    @property
    @abstractmethod
    def _format(self) -> RdfFormat:
        pass


class OxigraphN3Serializer(_OxigraphSerializer):
    _format = RdfFormat.N3


class OxigraphTurtleSerializer(_OxigraphSerializer):
    _format = RdfFormat.TURTLE


class OxigraphNTriplesSerializer(_OxigraphSerializer):
    _format = RdfFormat.N_TRIPLES


class OxigraphRdfXmlSerializer(_OxigraphSerializer):
    _format = RdfFormat.RDF_XML


class OxigraphNQuadsSerializer(_OxigraphSerializer):
    _format = RdfFormat.N_QUADS


class OxigraphTriGSerializer(_OxigraphSerializer):
    _format = RdfFormat.TRIG
