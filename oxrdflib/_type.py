from typing import Optional, Tuple

from rdflib import Graph
from rdflib.term import Node

_Triple = Tuple[Node, Node, Node]
_Quad = Tuple[Node, Node, Node, Graph]
_TriplePattern = Tuple[Optional[Node], Optional[Node], Optional[Node]]
