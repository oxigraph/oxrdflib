import json
import unittest

from rdflib import RDF, ConjunctiveGraph, Graph, Namespace

EX = Namespace("http://example.com/")


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
        self.assertEqual(len(result), 1)
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
        self.assertEqual(len(result), 1)
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
        self.assertEqual(len(result), 1)
        self.assertEqual(
            result.serialize(format="ntriples").strip(),
            b"<http://example.com/foo> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://example.com/Entity> .",
        )


if __name__ == "__main__":
    unittest.main()
