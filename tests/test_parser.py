import unittest
import warnings
from pathlib import Path

import rdflib

_TEST_DIR = Path(__file__).resolve().parent

_NAMEDGRAPH_QUERY = """SELECT DISTINCT ?g WHERE {
  GRAPH ?g {
    ?s ?p ?o .
  }
}"""

_NAMEDGRAPH_TRIPLE_QUERY = """SELECT DISTINCT ?s ?p ?o WHERE {{
  GRAPH <{namedgraph}> {{
    ?s ?p ?o .
  }}
}}"""


class TestTripleParsing(unittest.TestCase):
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


class TestQuadParsing(unittest.TestCase):
    def test_parsing_ox_nquads_bulk_load(self):
        graph = rdflib.Dataset(store="Oxigraph")
        graph.parse(_TEST_DIR / "data/test.nq", format="ox-nquads", transactional=False)
        self.assertEqual(len(graph), 6)
        self.assertEqual(len(graph.query(_NAMEDGRAPH_QUERY)), 4)
        self.assertEqual(
            len(graph.query(_NAMEDGRAPH_TRIPLE_QUERY.format(namedgraph="urn:x-rdflib:default"))),
            2,
        )
        self.assertEqual(
            len(graph.query(_NAMEDGRAPH_TRIPLE_QUERY.format(namedgraph="http://example.com/graph3"))),
            1,
        )
        self.assertEqual(
            len(graph.query(_NAMEDGRAPH_TRIPLE_QUERY.format(namedgraph="http://example.com/graph2"))),
            1,
        )
        self.assertEqual(
            len(graph.query(_NAMEDGRAPH_TRIPLE_QUERY.format(namedgraph="http://example.com/graph1"))),
            2,
        )

    def test_parsing_ox_nquads_load(self):
        graph = rdflib.Dataset(store="Oxigraph")
        graph.parse(_TEST_DIR / "data/test.nq", format="ox-nquads", transactional=True)
        self.assertEqual(len(graph), 6)
        self.assertEqual(len(graph.query(_NAMEDGRAPH_QUERY)), 4)
        self.assertEqual(
            len(graph.query(_NAMEDGRAPH_TRIPLE_QUERY.format(namedgraph="urn:x-rdflib:default"))),
            2,
        )
        self.assertEqual(
            len(graph.query(_NAMEDGRAPH_TRIPLE_QUERY.format(namedgraph="http://example.com/graph3"))),
            1,
        )
        self.assertEqual(
            len(graph.query(_NAMEDGRAPH_TRIPLE_QUERY.format(namedgraph="http://example.com/graph2"))),
            1,
        )
        self.assertEqual(
            len(graph.query(_NAMEDGRAPH_TRIPLE_QUERY.format(namedgraph="http://example.com/graph1"))),
            2,
        )


if __name__ == "__main__":
    unittest.main()
