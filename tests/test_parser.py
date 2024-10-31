import unittest
from io import StringIO
from pathlib import Path

import rdflib
from rdflib import Dataset, Graph, URIRef
from rdflib.graph import DATASET_DEFAULT_GRAPH_ID

_TEST_DIR = Path(__file__).resolve().parent

rdflib_version = tuple(int(e) for e in rdflib.__version__.split(".")[:2])
s = URIRef("http://example.com/s")
p = URIRef("http://example.com/vocab#p")
o = URIRef("http://example.com/o")
g = URIRef("http://example.com/g")


class TestParser(unittest.TestCase):
    def test_parse_graph(self):
        for store in ("default", "oxigraph"):
            for transactional in (True, False):
                for fmt, serialization in (
                    ("ox-turtle", "@prefix v: <http://example.com/vocab#> . <s> v:p <o> ."),
                    ("ox-ttl", "@prefix v: <http://example.com/vocab#> . <s> v:p <o> ."),
                    ("ox-ntriples", "<http://example.com/s> <http://example.com/vocab#p> <http://example.com/o> .\n"),
                    ("ox-n3", "<http://example.com/s> <http://example.com/vocab#p> <http://example.com/o> .\n"),
                    ("ox-nquads", "<http://example.com/s> <http://example.com/vocab#p> <http://example.com/o> .\n"),
                    ("ox-nt", "<http://example.com/s> <http://example.com/vocab#p> <http://example.com/o> .\n"),
                    ("ox-nt11", "<http://example.com/s> <http://example.com/vocab#p> <http://example.com/o> .\n"),
                    ("ox-trig", "@prefix v: <http://example.com/vocab#> . <s> v:p <o> ."),
                    (
                        "ox-xml",
                        """<?xml version="1.0" encoding="UTF-8"?>
            <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
                <rdf:Description rdf:about="s">
                    <p xmlns="http://example.com/vocab#" rdf:resource="o"/>
                </rdf:Description>
            </rdf:RDF>""",
                    ),
                ):
                    with self.subTest(store=store, format=fmt, transactional=transactional):
                        graph = Graph(store=store, identifier="http://example.com/")
                        graph.parse(
                            StringIO(serialization),
                            format=fmt,
                            publicID="http://example.com/",
                            transactional=transactional,
                        )
                        self.assertEqual(list(graph), [(s, p, o)])

    @unittest.skipIf(rdflib_version < (7, 1), "only works in rdflib 7.1+")
    def test_parse_dataset(self):
        for store in ("default", "oxigraph"):
            for transactional in (True, False):
                for fmt, serialization in (
                    (
                        "ox-nquads",
                        "<http://example.com/s> <http://example.com/vocab#p> <http://example.com/o> .\n"
                        "<http://example.com/s> <http://example.com/vocab#p> "
                        "<http://example.com/o> <http://example.com/g> .\n",
                    ),
                    (
                        "ox-trig",
                        "@prefix v: <http://example.com/vocab#> . <s> v:p <o> . <g> { <s> v:p <o> }",
                    ),
                ):
                    with self.subTest(store=store, format=fmt, transactional=transactional):
                        dataset = Dataset(store=store)
                        dataset.parse(
                            StringIO(serialization),
                            format=fmt,
                            publicID="http://example.com/",
                            transactional=transactional,
                        )
                        self.assertEqual(set(dataset), {(s, p, o, g), (s, p, o, DATASET_DEFAULT_GRAPH_ID)})


if __name__ == "__main__":
    unittest.main()
