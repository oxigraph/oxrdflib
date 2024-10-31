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
                ("ox-turtle", "<s> v:p <o> .\n"),
                ("ox-ttl", "<s> v:p <o> .\n"),
                ("ox-ntriples", "<http://example.com/s> <http://example.com/vocab#p> <http://example.com/o> .\n"),
                ("ox-n3", "<s> v:p <o> .\n"),
                ("ox-nquads", "<http://example.com/s> <http://example.com/vocab#p> <http://example.com/o> .\n"),
                ("ox-nt", "<http://example.com/s> <http://example.com/vocab#p> <http://example.com/o> .\n"),
                ("ox-nt11", "<http://example.com/s> <http://example.com/vocab#p> <http://example.com/o> .\n"),
                ("ox-trig", "<s> v:p <o> .\n"),
                (
                    "ox-xml",
                    """
	<rdf:Description rdf:about="s">
		<v:p rdf:resource="o"/>
	</rdf:Description>
</rdf:RDF>""",
                ),
            ):
                with self.subTest(store=store, format=fmt):
                    graph = Graph(store=store, base="http://example.com/")
                    graph.add((s, p, o))
                    graph.store.add((o, p, s), context=g)  # Should not be serialized
                    graph.bind("v", "http://example.com/vocab#")
                    self.assertTrue(graph.serialize(format=fmt).endswith(serialization))

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
                    "<g> {\n\t<s> v:p <o> .\n}\n",
                ),
            ):
                with self.subTest(store=store, format=fmt):
                    dataset = Dataset(store=store)
                    dataset.add((s, p, o, Graph(identifier=g)))
                    dataset.bind("v", "http://example.com/vocab#")
                    self.assertTrue(dataset.serialize(format=fmt, base="http://example.com/").endswith(serialization))


if __name__ == "__main__":
    unittest.main()
