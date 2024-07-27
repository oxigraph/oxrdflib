import unittest
import warnings
from pathlib import Path

import rdflib

_TEST_DIR = Path(__file__).resolve().parent


class TestGraphParsing(unittest.TestCase):
    def setUp(self):
        self.oxi_graph = rdflib.Graph(store="Oxigraph")
        self.memory_graph = rdflib.Graph()

    def remove_triples_from_oxi_graph(self):
        self.oxi_graph.remove((None, None, None))

    def remove_triples_from_memory_graph(self):
        self.memory_graph.remove((None, None, None))

    def test_parsing_ox_turtle_bulk_load(self):
        self.oxi_graph.parse(_TEST_DIR / "data/test.ttl", format="oxTurtle", transactional=False)
        result = set(self.oxi_graph)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 6)
        self.remove_triples_from_oxi_graph()

    def test_parsing_ox_turtle_load(self):
        self.oxi_graph.parse(_TEST_DIR / "data/test.ttl", format="oxTurtle", transactional=True)
        result = set(self.oxi_graph)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 6)
        self.remove_triples_from_oxi_graph()

    def test_parsing_ox_turtle_fallback(self):
        with warnings.catch_warnings(record=True) as warning:
            self.memory_graph.parse(_TEST_DIR / "data/test.ttl", format="oxTurtle", transactional=False)

        result = set(self.memory_graph)
        self.assertIsNotNone(result)
        self.assertEqual(
            warning[0].message.args[0],
            (
                "Graph store should be an instance of OxigraphStore, got Memory"
                " store instead. Attempting to parse using rdflib native parser."
            ),
        )
        self.assertEqual(len(result), 6)
        self.remove_triples_from_memory_graph()

    def test_parsing_ox_ntriples_bulk_load(self):
        self.oxi_graph.parse(_TEST_DIR / "data/test.n3", format="oxNTriples", transactional=False)
        result = set(self.oxi_graph)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 6)
        self.remove_triples_from_oxi_graph()

        self.oxi_graph.parse(_TEST_DIR / "data/test.n3", format="oxNTriples", transactional=True)
        result = set(self.oxi_graph)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 6)
        self.remove_triples_from_oxi_graph()

    def test_parsing_ox_ntriples_load(self):
        self.oxi_graph.parse(_TEST_DIR / "data/test.n3", format="oxNTriples", transactional=True)
        result = set(self.oxi_graph)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 6)
        self.remove_triples_from_oxi_graph()

        self.oxi_graph.parse(_TEST_DIR / "data/test.n3", format="oxNTriples", transactional=True)
        result = set(self.oxi_graph)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 6)
        self.remove_triples_from_oxi_graph()

    def test_parsing_ox_ntriples_fallback(self):
        with warnings.catch_warnings(record=True) as warning:
            self.memory_graph.parse(_TEST_DIR / "data/test.n3", format="oxNTriples", transactional=False)

        result = set(self.memory_graph)
        self.assertIsNotNone(result)
        self.assertEqual(
            warning[0].message.args[0],
            (
                "Graph store should be an instance of OxigraphStore, got Memory"
                " store instead. Attempting to parse using rdflib native parser."
            ),
        )
        self.assertEqual(len(result), 6)
        self.remove_triples_from_memory_graph()

    def test_parsing_ox_rdfxml_bulk_load(self):
        self.oxi_graph.parse(_TEST_DIR / "data/test.rdf", format="oxRdfXml", transactional=False)
        result = set(self.oxi_graph)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 6)
        self.remove_triples_from_oxi_graph()

    def test_parsing_ox_rdfxml_load(self):
        self.oxi_graph.parse(_TEST_DIR / "data/test.rdf", format="oxRdfXml", transactional=True)
        result = set(self.oxi_graph)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 6)
        self.remove_triples_from_oxi_graph()

    def test_parsing_ox_rdfxml_fallback(self):
        with warnings.catch_warnings(record=True) as warning:
            self.memory_graph.parse(_TEST_DIR / "data/test.rdf", format="oxRdfXml", transactional=False)

        result = set(self.memory_graph)
        self.assertIsNotNone(result)
        self.assertEqual(
            warning[0].message.args[0],
            (
                "Graph store should be an instance of OxigraphStore, got Memory"
                " store instead. Attempting to parse using rdflib native parser."
            ),
        )
        self.assertEqual(len(result), 6)
        self.remove_triples_from_memory_graph()


if __name__ == "__main__":
    unittest.main()
