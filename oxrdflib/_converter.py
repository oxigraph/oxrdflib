from typing import TYPE_CHECKING, Optional, Tuple, Union

import pyoxigraph as ox
from rdflib import Graph
from rdflib.graph import DATASET_DEFAULT_GRAPH_ID
from rdflib.term import BNode, Literal, Node, URIRef

from oxrdflib._type import _Quad, _Triple, _TriplePattern

if TYPE_CHECKING:
    from oxrdflib.store import OxigraphStore


def to_ox(
    term: Optional[Union[Node, _Triple, _Quad, Graph]], context: Optional[Graph] = None
) -> Optional[Union[ox.NamedNode, ox.BlankNode, ox.Literal, ox.DefaultGraph, ox.Quad]]:
    """Convert an rdflib term to an Oxigraph term."""
    if term is None:
        return None
    if term == DATASET_DEFAULT_GRAPH_ID:
        return ox.DefaultGraph()
    if isinstance(term, URIRef):
        return ox.NamedNode(term)
    if isinstance(term, BNode):
        return ox.BlankNode(term)
    if isinstance(term, Literal):
        return ox.Literal(
            term,
            language=term.language,
            datatype=ox.NamedNode(term.datatype) if term.datatype else None,
        )
    if isinstance(term, Graph):
        return to_ox(term.identifier)
    if isinstance(term, tuple):
        if len(term) == 3:
            return ox.Quad(
                to_ox(term[0]),
                to_ox(term[1]),
                to_ox(term[2]),
                to_ox(context),
            )
        if len(term) == 4:
            return ox.Quad(
                to_ox(term[0]),
                to_ox(term[1]),
                to_ox(term[2]),
                to_ox(term[3]),
            )
    raise ValueError(f"Unexpected rdflib term: {term!r}")


def to_ox_quad_pattern(triple: _TriplePattern, context: Optional[Graph] = None):
    """Convert an rdflib quad pattern to an Oxigraph quad pattern."""

    (s, p, o) = triple
    return (
        to_ox_term_pattern(s),
        to_ox_term_pattern(p),
        to_ox_term_pattern(o),
        to_ox_term_pattern(context),
    )


def to_ox_term_pattern(
    term: Optional[Union[URIRef, BNode, Literal, Graph]],
) -> Optional[Union[ox.NamedNode, ox.BlankNode, ox.Literal]]:
    if term is None:
        return None
    if isinstance(term, URIRef):
        return ox.NamedNode(term)
    if isinstance(term, BNode):
        return ox.BlankNode(term)
    if isinstance(term, Literal):
        return ox.Literal(
            term,
            language=term.language,
            datatype=ox.NamedNode(term.datatype) if term.datatype else None,
        )
    if isinstance(term, Graph):
        return to_ox(term.identifier)
    raise ValueError(f"Unexpected rdflib term: {term!r}")


def from_ox_graph_name(
    graph_name: Union[ox.NamedNode, ox.BlankNode, ox.DefaultGraph],
    store: "OxigraphStore",
) -> Graph:
    if isinstance(graph_name, ox.NamedNode):
        return Graph(identifier=URIRef(graph_name.value), store=store)
    if isinstance(graph_name, ox.BlankNode):
        return Graph(identifier=BNode(graph_name.value), store=store)
    if isinstance(graph_name, ox.DefaultGraph):
        return Graph(identifier=DATASET_DEFAULT_GRAPH_ID, store=store)
    raise ValueError(f"Unexpected Oxigraph graph name: {graph_name!r}")


def from_ox(
    term: Optional[Union[ox.NamedNode, ox.BlankNode, ox.Literal, ox.Triple]],
) -> Optional[Union[Node, Tuple[Node, Node, Node]]]:
    if term is None:
        return None
    if isinstance(term, ox.NamedNode):
        return URIRef(term.value)
    if isinstance(term, ox.BlankNode):
        return BNode(term.value)
    if isinstance(term, ox.Literal):
        if term.language:
            return Literal(term.value, lang=term.language)
        return Literal(term.value, datatype=URIRef(term.datatype.value))
    if isinstance(term, ox.Triple):
        return from_ox(term.subject), from_ox(term.predicate), from_ox(term.object)
    raise ValueError(f"Unexpected Oxigraph term: {term!r}")


def rdflib_to_mime_type(rdflib_type: str) -> str:
    """Convert an rdflib type to a MIME type."""
    if rdflib_type in ("ttl", "turtle"):
        return "text/turtle"
    if rdflib_type in ("nt", "ntriples"):
        return "application/n-triples"
    if rdflib_type == "xml":
        return "application/rdf+xml"
    if rdflib_type == "trig":
        return "application/trig"
    if rdflib_type == "nquads":
        return "application/n-quads"
    if rdflib_type == "trix":
        return "application/trix"
    raise ValueError(f"Unsupported rdflib type: {rdflib_type}")


def ox_to_rdflib_type(ox_format: str) -> str:
    """Convert an Oxigraph format to a rdflib parser format."""
    print(ox_format)
    if ox_format in ("ox-turtle", "ox-ttl"):
        return "turtle"
    if ox_format in ("ox-nt", "ox-ntriples"):
        return "nt"
    if ox_format == "ox-xml":
        return "xml"
    if ox_format in ("ox-nquads", "ox-nq"):
        return "nquads"
    raise ValueError(f"Unsupported Oxigraph type: {ox_format}")
