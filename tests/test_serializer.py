import unittest

from rdflib import Dataset, Graph, URIRef

s = URIRef("http://example.com/s")
p = URIRef("http://example.com/vocab#p")
o = URIRef("http://example.com/o")
g = URIRef("http://example.com/g")


class TestSerializer(unittest.TestCase):
    def test_serialize_graph(self):
        for store in ("default", "oxigraph"):
            for fmt, serialization in (
                ("ox-turtle", "<http://example.com/s> <http://example.com/vocab#p> <http://example.com/o> .\n"),
                ("ox-ttl", "<http://example.com/s> <http://example.com/vocab#p> <http://example.com/o> .\n"),
                ("ox-ntriples", "<http://example.com/s> <http://example.com/vocab#p> <http://example.com/o> .\n"),
                ("ox-n3", "<http://example.com/s> <http://example.com/vocab#p> <http://example.com/o> .\n"),
                ("ox-nquads", "<http://example.com/s> <http://example.com/vocab#p> <http://example.com/o> .\n"),
                ("ox-nt", "<http://example.com/s> <http://example.com/vocab#p> <http://example.com/o> .\n"),
                ("ox-nt11", "<http://example.com/s> <http://example.com/vocab#p> <http://example.com/o> .\n"),
                ("ox-trig", "<http://example.com/s> <http://example.com/vocab#p> <http://example.com/o> .\n"),
                (
                    "ox-xml",
                    """<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
	<rdf:Description rdf:about="http://example.com/s">
		<p xmlns="http://example.com/vocab#" rdf:resource="http://example.com/o"/>
	</rdf:Description>
</rdf:RDF>""",
                ),
            ):
                with self.subTest(store=store, format=fmt):
                    graph = Graph(store=store)
                    graph.add((s, p, o))
                    graph.store.add((o, p, s), context=g)  # Should not be serialized
                    self.assertEqual(graph.serialize(format=fmt), serialization)

    def test_serialize_dataset(self):
        for store in ("default", "oxigraph"):
            for fmt, serialization in (
                (
                    "ox-nquads",
                    "<http://example.com/s> <http://example.com/vocab#p> "
                    "<http://example.com/o> <http://example.com/g> .\n",
                ),
                (
                    "ox-trig",
                    "<http://example.com/g> {\n\t<http://example.com/s> "
                    "<http://example.com/vocab#p> <http://example.com/o> .\n}\n",
                ),
            ):
                with self.subTest(store=store, format=fmt):
                    dataset = Dataset(store=store)
                    dataset.add((s, p, o, Graph(identifier=g)))
                    self.assertEqual(dataset.serialize(format=fmt), serialization)


if __name__ == "__main__":
    unittest.main()
