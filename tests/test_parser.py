import unittest
from pathlib import Path

import rdflib

_TEST_DIR = Path(__file__).resolve().parent


class TestGraphParsing(unittest.TestCase):
    def setUp(self):
        self.graph = rdflib.Graph(store="Oxigraph")

    def remove_triples(self):
        self.graph.remove((None, None, None))

    def test_parsing_ox_turtle_bulk_load(self):
        self.graph.parse(_TEST_DIR / "data/test.ttl", format="oxTurtle", transactional=False)
        result = set(self.graph)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 6)
        self.remove_triples()

    def test_parsing_ox_turtle_load(self):
        self.graph.parse(_TEST_DIR / "data/test.ttl", format="oxTurtle", transactional=True)
        result = set(self.graph)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 6)
        self.remove_triples()

    def test_parsing_ox_ntriples_bulk_load(self):
        self.graph.parse(_TEST_DIR / "data/test.n3", format="oxNTriples", transactional=False)
        result = set(self.graph)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 6)
        self.remove_triples()

    def test_parsing_ox_ntriples_load(self):
        self.graph.parse(_TEST_DIR / "data/test.n3", format="oxNTriples", transactional=True)
        result = set(self.graph)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 6)
        self.remove_triples()

    def test_parsing_ox_rdfxml_bulk_load(self):
        self.graph.parse(_TEST_DIR / "data/test.rdf", format="oxRdfXml", transactional=False)
        result = set(self.graph)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 6)
        self.remove_triples()

    def test_parsing_ox_rdfxml_load(self):
        self.graph.parse(_TEST_DIR / "data/test.rdf", format="oxRdfXml", transactional=True)
        result = set(self.graph)
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 6)
        self.remove_triples()


if __name__ == "__main__":
    unittest.main()
