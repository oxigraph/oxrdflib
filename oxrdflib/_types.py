from typing import Tuple, Optional
from enum import Enum

from rdflib import Graph
from rdflib.term import Node


_Triple = Tuple[Node, Node, Node]
_Quad = Tuple[Node, Node, Node, Graph]
_TriplePattern = Tuple[Optional[Node], Optional[Node], Optional[Node]]


class RDFSerialization(Enum):
    oxNTriple = "N-Triples"
    oxNQuads = "N-Quads"
    oxTurtle = "text/turtle"
    oxTriG = "application/trig"
    oxRDF_XML = "application/rdf+xml"
