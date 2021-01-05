from abc import ABC, abstractmethod

import pyoxigraph as ox
from rdflib import Graph
from rdflib.graph import DATASET_DEFAULT_GRAPH_ID
from rdflib.query import Result
from rdflib.store import VALID_STORE, Store
from rdflib.term import BNode, Literal, Node, URIRef, Variable

__all__ = ["MemoryOxStore", "SledOxStore"]


class _BaseOxStore(Store, ABC):
    context_aware = True
    formula_aware = False
    transaction_aware = False
    graph_aware = True

    @property
    @abstractmethod
    def _inner(self):
        pass

    def gc(self):
        pass

    def add(self, triple, context, quoted=False):
        if quoted:
            raise ValueError("Oxigraph stores are not formula aware")
        self._inner.add(_to_ox(triple, context))
        super().add(triple, context, quoted)

    def remove(self, triple, context=None):
        for q in self._inner.quads_for_pattern(*_to_ox_quad_pattern(triple, context)):
            self._inner.remove(q)
        super().remove(triple, context)

    def triples(self, triple_pattern, context=None):
        return (_from_ox(q) for q in self._inner.quads_for_pattern(*_to_ox_quad_pattern(triple_pattern, context)))

    def __len__(self, context=None):
        if context is None:
            # TODO: very bad
            return len({q.triple for q in self._inner})
        else:
            return sum(1 for _ in self._inner.quads_for_pattern(None, None, None, _to_ox(context)))

    def contexts(self, triple=None):
        if triple is None:
            return (_from_ox(g) for g in self._inner.named_graphs())
        else:
            return (_from_ox(q[3]) for q in self._inner.quads_for_pattern(*_to_ox_quad_pattern(triple)))

    def query(self, query, initNs, initBindings, queryGraph, **kwargs):
        if initNs:
            query = (
                "".join("PREFIX {}: <{}>\n".format(prefix, namespace) for prefix, namespace in initNs.items()) + query
            )
        if initBindings:
            query += "\nVALUES ( {} ) {{ ({}) }}".format(
                " ".join("?{}".format(k) for k in initBindings.keys()), " ".join(v.n3() for v in initBindings.values())
            )
        result = self._inner.query(
            query,
            use_default_graph_as_union=queryGraph == "__UNION__",
            default_graph=_to_ox(queryGraph) if isinstance(queryGraph, Node) else None,
        )
        if isinstance(result, bool):
            out = Result("ASK")
            out.askAnswer = result
        elif isinstance(result, ox.QuerySolutions):
            out = Result("SELECT")
            out.vars = [Variable(v.value) for v in result.variables]
            out.bindings = ({v: _from_ox(solution[str(v)]) for v in out.vars} for solution in result)
        elif isinstance(result, ox.QueryTriples):
            out = Result("CONSTRUCT")
            out.graph = Graph()
            out.graph += (_from_ox(t) for t in result)
        else:
            raise ValueError("Unexpected query result: {}".format(result))
        return out

    def update(self, update, initNs, initBindings, queryGraph, **kwargs):
        raise NotImplementedError

    def commit(self):
        # TODO: implement
        pass

    def rollback(self):
        # TODO: implement
        pass

    def add_graph(self, graph):
        self._inner.add_graph(_to_ox(graph))

    def remove_graph(self, graph):
        self._inner.remove_graph(_to_ox(graph))


class MemoryOxStore(_BaseOxStore):
    def __init__(self, configuration=None, identifier=None):
        self._store = ox.MemoryStore()
        super().__init__(configuration, identifier)

    @property
    def _inner(self):
        return self._store


class SledOxStore(_BaseOxStore):
    def __init__(self, configuration=None, identifier=None):
        self._store = None
        super().__init__(configuration, identifier)

    def open(self, configuration, create=False):
        self._store = ox.SledStore(configuration)
        return VALID_STORE

    def close(self, commit_pending_transaction=False):
        del self._store

    def destroy(self, configuration):
        raise NotImplementedError("destroy is not implemented yet for the Sled based store")

    @property
    def _inner(self):
        if self._store is None:
            self._store = ox.SledStore()
        return self._store


def _to_ox(term, context=None):
    if term is None:
        return None
    elif term == DATASET_DEFAULT_GRAPH_ID:
        return ox.DefaultGraph()
    elif isinstance(term, URIRef):
        return ox.NamedNode(term)
    elif isinstance(term, BNode):
        return ox.BlankNode(term)
    elif isinstance(term, Literal):
        return ox.Literal(term, language=term.language, datatype=ox.NamedNode(term.datatype) if term.datatype else None)
    elif isinstance(term, Graph):
        return _to_ox(term.identifier)
    elif isinstance(term, tuple):
        if len(term) == 3:
            return ox.Quad(_to_ox(term[0]), _to_ox(term[1]), _to_ox(term[2]), _to_ox(context))
        elif len(term) == 4:
            return ox.Quad(_to_ox(term[0]), _to_ox(term[1]), _to_ox(term[2]), _to_ox(term[3]))
        else:
            raise ValueError("Unexpected rdflib term: {}".format(repr(term)))
    else:
        raise ValueError("Unexpected rdflib term: {}".format(repr(term)))


def _to_ox_quad_pattern(triple, context=None):
    (s, p, o) = triple
    return _to_ox_term_pattern(s), _to_ox_term_pattern(p), _to_ox_term_pattern(o), _to_ox_term_pattern(context)


def _to_ox_term_pattern(term):
    if term is None:
        return None
    elif isinstance(term, URIRef):
        return ox.NamedNode(term)
    elif isinstance(term, BNode):
        return ox.BlankNode(term)
    elif isinstance(term, Literal):
        return ox.Literal(term, language=term.language, datatype=ox.NamedNode(term.datatype) if term.datatype else None)
    elif isinstance(term, Graph):
        return _to_ox(term.identifier)
    else:
        raise ValueError("Unexpected rdflib term: {}".format(repr(term)))


def _from_ox(term):
    if term is None:
        return None
    if isinstance(term, ox.NamedNode):
        return URIRef(term.value)
    elif isinstance(term, ox.BlankNode):
        return BNode(term.value)
    elif isinstance(term, ox.Literal):
        if term.language:
            return Literal(term.value, lang=term.language)
        else:
            return Literal(term.value, datatype=URIRef(term.datatype.value))
    elif isinstance(term, ox.DefaultGraph):
        return None
    elif isinstance(term, ox.Triple):
        return _from_ox(term.subject), _from_ox(term.predicate), _from_ox(term.object)
    elif isinstance(term, ox.Quad):
        return (_from_ox(term.subject), _from_ox(term.predicate), _from_ox(term.object)), _from_ox(term.graph_name)
    else:
        raise ValueError("Unexpected Oxigraph term: {}".format(repr(term)))
