import unittest
import warnings
from pathlib import Path

import rdflib

_TEST_DIR = Path(__file__).resolve().parent


class TestGraphParsing(unittest.TestCase):
    def test_parsing_ox_turtle_bulk_load(self):
        graph = rdflib.Graph(store="Oxigraph")
        graph.parse(_TEST_DIR / "data/test.ttl", format="ox-turtle", transactional=False)
        self.assertEqual(len(graph), 6)

    def test_parsing_ox_turtle_load(self):
        graph = rdflib.Graph(store="Oxigraph")
        graph.parse(_TEST_DIR / "data/test.ttl", format="ox-turtle", transactional=True)

        self.assertEqual(len(graph), 6)

    def test_parsing_ox_turtle_fallback(self):
        graph = rdflib.Graph()
        with warnings.catch_warnings(record=True) as warning:
            graph.parse(_TEST_DIR / "data/test.ttl", format="ox-turtle", transactional=False)

        self.assertEqual(
            warning[0].message.args[0],
            (
                "Graph store should be an instance of OxigraphStore, got Memory"
                " store instead. Attempting to parse using rdflib native parser."
            ),
        )
        self.assertEqual(len(graph), 6)

    def test_parsing_ox_url_turtle(self):
        graph = rdflib.Graph(store="Oxigraph")
        graph.parse(
            "https://i-adopt.github.io/ontology/ontology.ttl",
            format="ox-turtle",
            transactional=True,
        )
        self.assertIsNotNone(graph)

    def test_parsing_ox_ntriples_bulk_load(self):
        graph = rdflib.Graph(store="Oxigraph")
        graph.parse(_TEST_DIR / "data/test.nt", format="ox-ntriples", transactional=False)
        self.assertEqual(len(graph), 6)

    def test_parsing_ox_ntriples_load(self):
        graph = rdflib.Graph(store="Oxigraph")
        graph.parse(_TEST_DIR / "data/test.nt", format="ox-ntriples", transactional=True)

        self.assertEqual(len(graph), 6)

    def test_parsing_ox_ntriples_fallback(self):
        graph = rdflib.Graph()
        with warnings.catch_warnings(record=True) as warning:
            graph.parse(_TEST_DIR / "data/test.nt", format="ox-ntriples", transactional=False)

        self.assertEqual(
            warning[0].message.args[0],
            (
                "Graph store should be an instance of OxigraphStore, got Memory"
                " store instead. Attempting to parse using rdflib native parser."
            ),
        )
        self.assertEqual(len(graph), 6)

    def test_parsing_ox_url_ntriples(self):
        graph = rdflib.Graph(store="Oxigraph")
        graph.parse(
            "https://i-adopt.github.io/ontology/ontology.nt",
            format="ox-ntriples",
            transactional=True,
        )
        self.assertIsNotNone(graph)

    def test_parsing_ox_rdfxml_bulk_load(self):
        graph = rdflib.Graph(store="Oxigraph")
        graph.parse(
            _TEST_DIR / "data/test.rdf",
            publicID="http://example.com/",
            format="ox-xml",
            transactional=False,
        )

        self.assertEqual(len(graph), 6)
        self.assertTrue(next(iter(graph))[0].startswith("http://example.com/"))

    def test_parsing_ox_rdfxml_load(self):
        graph = rdflib.Graph(store="Oxigraph")
        graph.parse(
            _TEST_DIR / "data/test.rdf",
            publicID="http://example.com/",
            format="ox-xml",
            transactional=True,
        )
        self.assertEqual(len(graph), 6)
        self.assertTrue(next(iter(graph))[0].startswith("http://example.com/"))

    def test_parsing_ox_url_rdfxml_load(self):
        graph = rdflib.Graph(store="Oxigraph")
        graph.parse(
            "https://i-adopt.github.io/ontology/ontology.xml",
            format="ox-xml",
            transactional=True,
        )
        self.assertIsNotNone(graph)

    def test_parsing_ox_rdfxml_fallback(self):
        graph = rdflib.Graph()
        with warnings.catch_warnings(record=True) as warning:
            graph.parse(
                _TEST_DIR / "data/test.rdf",
                publicID="http://example.com/",
                format="ox-xml",
                transactional=False,
            )

        self.assertEqual(
            warning[0].message.args[0],
            (
                "Graph store should be an instance of OxigraphStore, got Memory"
                " store instead. Attempting to parse using rdflib native parser."
            ),
        )
        self.assertEqual(len(graph), 6)


if __name__ == "__main__":
    unittest.main()
