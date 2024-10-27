import shutil
from typing import (
    Any,
    Dict,
    Generator,
    Iterable,
    Iterator,
    Mapping,
    Optional,
    Tuple,
    Union,
)

import pyoxigraph as ox
from rdflib import Graph
from rdflib.graph import DATASET_DEFAULT_GRAPH_ID
from rdflib.plugins.sparql.sparql import Query, Update
from rdflib.query import Result
from rdflib.store import VALID_STORE, Store
from rdflib.term import Identifier, Node, URIRef, Variable

from ._converter import (
    from_ox,
    from_ox_graph_name,
    to_ox,
    to_ox_quad_pattern,
)
from ._type import _Quad, _Triple, _TriplePattern

__all__ = ["OxigraphStore"]


class OxigraphStore(Store):
    context_aware: bool = True
    formula_aware: bool = False
    transaction_aware: bool = False
    graph_aware: bool = True

    def __init__(
        self,
        configuration: Optional[str] = None,
        identifier: Optional[Identifier] = None,
        *,
        store: Optional[ox.Store] = None,
    ):
        self._store = store
        self._prefix_for_namespace: Dict[URIRef, str] = {}
        self._namespace_for_prefix: Dict[str, URIRef] = {}
        super().__init__(configuration, identifier)

    def open(self, configuration: str, create: bool = False) -> Optional[int]:  # noqa: ARG002
        if self._store is not None:
            raise ValueError("The open function should be called before any RDF operation")
        self._store = ox.Store(configuration)
        return VALID_STORE

    def close(self, commit_pending_transaction: bool = False) -> None:  # noqa: ARG002
        del self._store

    def destroy(self, configuration: str) -> None:
        shutil.rmtree(configuration)

    def gc(self) -> None:
        pass

    @property
    def _inner(self) -> ox.Store:
        if self._store is None:
            self._store = ox.Store()
        return self._store

    def add(
        self,
        triple: _Triple,
        context: Graph,
        quoted: bool = False,
    ) -> None:
        if quoted:
            raise ValueError("Oxigraph stores are not formula aware")
        self._inner.add(to_ox(triple, context))
        super().add(triple, context, quoted)

    def addN(self, quads: Iterable[_Quad]) -> None:  # noqa: N802
        self._inner.extend([to_ox(q) for q in quads])
        for quad in quads:
            (s, p, o, g) = quad
            super().add((s, p, o), g)

    def remove(
        self,
        triple: _TriplePattern,
        context: Optional[Graph] = None,
    ) -> None:
        for q in self._inner.quads_for_pattern(*to_ox_quad_pattern(triple, context)):
            self._inner.remove(q)
        super().remove(triple, context)

    def triples(
        self,
        triple_pattern: _TriplePattern,
        context: Optional[Graph] = None,
    ) -> Iterator[Tuple[_Triple, Iterator[Optional[Graph]]]]:
        try:
            return (
                (
                    (from_ox(q.subject), from_ox(q.predicate), from_ox(q.object)),
                    iter(((from_ox_graph_name(q.graph_name, self)),)),
                )
                for q in self._inner.quads_for_pattern(*to_ox_quad_pattern(triple_pattern, context))
            )
        except (TypeError, ValueError):
            return iter(())  # We just don't return anything

    def __len__(self, context: Optional[Graph] = None) -> int:
        return int(
            next(
                self._inner.query(
                    "SELECT (COUNT(DISTINCT TRIPLE(?s, ?p, ?o)) AS ?c) WHERE { ?s ?p ?o }",
                    **(
                        {"use_default_graph_as_union": True} if context is None else {"default_graph": to_ox(context)}  # type: ignore[dict-item]
                    ),
                )
            )[0].value
        )

    def contexts(self, triple: Optional[_Triple] = None) -> Generator[Graph, None, None]:
        if triple is None:
            return (from_ox_graph_name(g, self) for g in self._inner.named_graphs())
        return (
            from_ox_graph_name(q.graph_name, self) for q in self._inner.quads_for_pattern(*to_ox_quad_pattern(triple))
        )

    def query(
        self,
        query: Union[Query, str],
        initNs: Mapping[str, Any],  # noqa: N803
        initBindings: Mapping[str, Identifier],  # noqa: N803
        queryGraph: str,  # noqa: N803
        **kwargs: Any,
    ) -> "Result":
        if isinstance(query, Query) or kwargs:
            raise NotImplementedError
        init_ns = dict(self._namespace_for_prefix, **initNs)
        query = "".join(f"PREFIX {prefix}: <{namespace}>\n" for prefix, namespace in init_ns.items()) + query
        if initBindings:
            query += "\nVALUES ( {} ) {{ ({}) }}".format(
                " ".join(f"?{k}" for k in initBindings),
                " ".join(v.n3() for v in initBindings.values()),
            )
        result = self._inner.query(
            query,
            use_default_graph_as_union=queryGraph == "__UNION__",
            default_graph=(to_ox(queryGraph) if isinstance(queryGraph, Node) else None),
        )
        if isinstance(result, ox.QueryBoolean):
            out = Result("ASK")
            out.askAnswer = bool(result)
        elif isinstance(result, ox.QuerySolutions):
            out = Result("SELECT")
            out.vars = [Variable(v.value) for v in result.variables]
            out.bindings = ({v: from_ox(val) for v, val in zip(out.vars, solution)} for solution in result)
        elif isinstance(result, ox.QueryTriples):
            out = Result("CONSTRUCT")
            out.graph = Graph()
            out.graph += (from_ox(t) for t in result)
        else:
            raise ValueError(f"Unexpected query result: {result}")
        return out

    def update(
        self,
        update: Union[Update, str],
        initNs: Mapping[str, Any],  # noqa: N803
        initBindings: Mapping[str, Identifier],  # noqa: N803
        queryGraph: str,  # noqa: N803
        **kwargs: Any,  # noqa: ARG002
    ) -> None:
        init_ns = dict(self._namespace_for_prefix, **initNs)
        update = "".join(f"PREFIX {prefix}: <{namespace}>\n" for prefix, namespace in init_ns.items()) + update
        if initBindings:
            raise NotImplementedError("initBindings are not supported by Oxigraph store")
        if queryGraph != DATASET_DEFAULT_GRAPH_ID:
            raise NotImplementedError(f"Only {DATASET_DEFAULT_GRAPH_ID} is supported by native Oxigraph store")
        self._inner.update(update)

    def commit(self) -> None:
        # TODO: implement
        pass

    def rollback(self) -> None:
        # TODO: implement
        pass

    def add_graph(self, graph: Graph) -> None:
        self._inner.add_graph(to_ox(graph))

    def remove_graph(self, graph: Graph) -> None:
        self._inner.remove_graph(to_ox(graph))

    def bind(self, prefix: str, namespace: URIRef, override: bool = True) -> None:
        if not override and (prefix in self._namespace_for_prefix or namespace in self._prefix_for_namespace):
            return  # nothing to do
        self._delete_from_prefix(prefix)
        self._delete_from_namespace(namespace)
        self._namespace_for_prefix[prefix] = namespace
        self._prefix_for_namespace[namespace] = prefix

    def _delete_from_prefix(self, prefix):
        if prefix not in self._namespace_for_prefix:
            return
        namespace = self._namespace_for_prefix[prefix]
        del self._namespace_for_prefix[prefix]
        self._delete_from_namespace(namespace)

    def _delete_from_namespace(self, namespace):
        if namespace not in self._prefix_for_namespace:
            return
        prefix = self._prefix_for_namespace[namespace]
        del self._prefix_for_namespace[namespace]
        self._delete_from_prefix(prefix)

    def prefix(self, namespace: URIRef) -> Optional[str]:
        return self._prefix_for_namespace.get(namespace)

    def namespace(self, prefix: str) -> Optional[URIRef]:
        return self._namespace_for_prefix.get(prefix)

    def namespaces(self) -> Iterator[Tuple[str, URIRef]]:
        yield from self._namespace_for_prefix.items()
