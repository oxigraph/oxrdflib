import json
import unittest

import rdflib
from rdflib import RDF, ConjunctiveGraph, Dataset, Graph, Namespace

EX = Namespace("http://example.com/")

rdflib_version = tuple(int(e) for e in rdflib.__version__.split(".")[:2])


class SparqlTestCase(unittest.TestCase):
    def test_ask_query(self):
        g = ConjunctiveGraph("Oxigraph")
        g.add((EX.foo, RDF.type, EX.Entity))
        g.bind("ex", EX)

        # basic
        result = g.query("ASK { ?s ?p ?o }")
        self.assertTrue(result)
        self.assertIsInstance(result.serialize(), bytes)

        # with not initialized prefix
        self.assertTrue(g.query("ASK { ex:foo rdf:type ex2:Entity }", initNs={"ex2": EX}))

        # with init entities
        self.assertFalse(g.query("ASK { ?s ?p ?o }", initBindings={"o": EX.NotExists}))

        # in specific graph
        g = ConjunctiveGraph("Oxigraph")
        g1 = Graph(store=g.store, identifier=EX.g1)
        g1.add((EX.foo, RDF.type, EX.Entity))
        self.assertTrue(g1.query("ASK { ?s ?p ?o }"))

    def test_select_query_graph(self):
        g = Graph("Oxigraph")
        g.add((EX.foo, RDF.type, EX.Entity))
        result = g.query("SELECT ?s WHERE { ?s ?p ?o }")
        self.assertEqual(
            json.loads(result.serialize(format="json").decode("utf-8")),
            {
                "results": {"bindings": [{"s": {"type": "uri", "value": "http://example.com/foo"}}]},
                "head": {"vars": ["s"]},
            },
        )

    def test_select_query_conjunctive(self):
        g = ConjunctiveGraph("Oxigraph")
        g.add((EX.foo, RDF.type, EX.Entity))
        result = g.query("SELECT ?s WHERE { ?s ?p ?o }")
        self.assertEqual(
            json.loads(result.serialize(format="json").decode("utf-8")),
            {
                "results": {"bindings": [{"s": {"type": "uri", "value": "http://example.com/foo"}}]},
                "head": {"vars": ["s"]},
            },
        )

    @unittest.skipIf(rdflib_version < (7, 1), "only works in rdflib 7.1+")
    def test_select_query_dataset(self):
        g = Dataset("Oxigraph")
        g.add((EX.foo, RDF.type, EX.Entity))
        result = g.query("SELECT ?s WHERE { ?s ?p ?o }")
        self.assertEqual(
            json.loads(result.serialize(format="json").decode("utf-8")),
            {
                "results": {"bindings": [{"s": {"type": "uri", "value": "http://example.com/foo"}}]},
                "head": {"vars": ["s"]},
            },
        )

    def test_select_query_dataset_default_union(self):
        g = Dataset("Oxigraph", default_union=True)
        g.add((EX.foo, RDF.type, EX.Entity, EX.graph))
        result = g.query("SELECT ?s WHERE { ?s ?p ?o }")
        self.assertEqual(
            json.loads(result.serialize(format="json").decode("utf-8")),
            {
                "results": {"bindings": [{"s": {"type": "uri", "value": "http://example.com/foo"}}]},
                "head": {"vars": ["s"]},
            },
        )

    def test_construct_query(self):
        g = ConjunctiveGraph("Oxigraph")
        g.add((EX.foo, RDF.type, EX.Entity))
        result = g.query("CONSTRUCT WHERE { ?s ?p ?o }")
        self.assertEqual(
            result.serialize(format="ntriples").strip(),
            b"<http://example.com/foo> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://example.com/Entity> .",
        )

    def test_select_query_init_bindings(self):
        g = Graph("Oxigraph")
        result = g.query("SELECT ?s WHERE {}", initBindings={"s": EX.foo})
        self.assertEqual(
            json.loads(result.serialize(format="json").decode("utf-8")),
            {
                "results": {"bindings": [{"s": {"type": "uri", "value": "http://example.com/foo"}}]},
                "head": {"vars": ["s"]},
            },
        )

    def test_select_query_init_namespace(self):
        g = Graph("Oxigraph")
        result = g.query("SELECT (ex:foo AS ?s) WHERE {}", initNs={"ex": "http://example.com/"})
        self.assertEqual(
            json.loads(result.serialize(format="json").decode("utf-8")),
            {
                "results": {"bindings": [{"s": {"type": "uri", "value": "http://example.com/foo"}}]},
                "head": {"vars": ["s"]},
            },
        )

    def test_insert_where_update_graph(self):
        g = Graph("Oxigraph")
        g.add((EX.foo, RDF.type, EX.Entity))
        g.update("INSERT { ?s a <http://example.com/Entity2> } WHERE { ?s a <http://example.com/Entity> }")
        self.assertIn((EX.foo, RDF.type, EX.Entity2), g)

    def test_insert_where_update_conjunctive_graph(self):
        g = ConjunctiveGraph("Oxigraph")
        g.add((EX.foo, RDF.type, EX.Entity, EX.g))
        g.update("INSERT { ?s a <http://example.com/Entity2> } WHERE { ?s a <http://example.com/Entity> }")
        self.assertIn((EX.foo, RDF.type, EX.Entity2), g)

    def test_insert_where_update_dataset_named_graph(self):
        g = Dataset("Oxigraph")
        g.add((EX.foo, RDF.type, EX.Entity, EX.g))
        g.update("INSERT { ?s a <http://example.com/Entity2> } WHERE { GRAPH ?g { ?s a <http://example.com/Entity> } }")
        self.assertIn((EX.foo, RDF.type, EX.Entity2, g.identifier), g)

    def test_insert_where_update_dataset_default_graph(self):
        g = Dataset("Oxigraph")
        g.add((EX.foo, RDF.type, EX.Entity))
        g.update("INSERT { ?s a <http://example.com/Entity2> } WHERE { ?s a <http://example.com/Entity> }")
        self.assertIn((EX.foo, RDF.type, EX.Entity2, g.identifier), g)

    def test_insert_where_update_dataset_default_union(self):
        g = Dataset("Oxigraph", default_union=True)
        g.add((EX.foo, RDF.type, EX.Entity, EX.g))
        g.update("INSERT { ?s a <http://example.com/Entity2> } WHERE { ?s a <http://example.com/Entity> }")
        self.assertIn((EX.foo, RDF.type, EX.Entity2, g.identifier), g)


if __name__ == "__main__":
    unittest.main()
