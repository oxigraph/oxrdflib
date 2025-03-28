import unittest
from pathlib import Path

from pyoxigraph import Store
from rdflib import RDF, XSD, BNode, ConjunctiveGraph, Graph, Literal, Namespace

from oxrdflib import OxigraphStore

EX = Namespace("http://example.com/")


class StoreTestCase(unittest.TestCase):
    def test_store_without_open(self) -> None:
        g = ConjunctiveGraph("Oxigraph")
        self._fill_graph(g)
        self._test_graph(g)
        self.assertEqual(len(list(iter(g))), 4)

    def test_store_with_open(self) -> None:
        g = ConjunctiveGraph("Oxigraph")
        g.open("test_store")
        self._fill_graph(g)
        g.close()
        del g
        self.assertTrue(Path("test_store").exists())

        g = ConjunctiveGraph("Oxigraph")
        g.open("test_store")
        self._test_graph(g)
        g.close()
        g.destroy("test_store")
        self.assertFalse(Path("test_store").exists())

    def test_store_with_late_open(self) -> None:
        g = ConjunctiveGraph("Oxigraph")
        g.add((EX.foo, RDF.type, EX.Entity))
        with self.assertRaises(Exception) as _:
            g.open("test_store")

    def test_store_with_shared_backend(self) -> None:
        store = Store()
        self._fill_graph(Graph(store=OxigraphStore(store=store), identifier="http://example.com"))
        self._test_graph(Graph(store=OxigraphStore(store=store), identifier="http://example.com"))

    def test_json_serialization(self) -> None:
        graph1 = Graph("Oxigraph", identifier=EX.graph)
        graph1.add((EX.foo, EX.name, Literal("foo")))
        json_ld = graph1.serialize(format="json-ld")
        graph2 = Graph("Oxigraph", identifier=EX.graph)
        graph2.parse(data=json_ld, format="json-ld")
        self.assertEqual(graph1, graph2)

    @staticmethod
    def _fill_graph(g: Graph) -> None:
        g.add((EX.foo, RDF.type, EX.Entity))
        g.add((EX.foo, EX.prop, BNode("123")))
        g.add((EX.foo, EX.prop1, Literal("foo")))
        g.add((EX.foo, EX.prop1, Literal("foo", lang="en")))
        g.add((EX.foo, EX.prop1, Literal("1", datatype=XSD.integer)))
        g.remove((EX.foo, EX.prop, BNode("123")))

    def _test_graph(self, g: Graph) -> None:
        self.assertIn((EX.foo, RDF.type, EX.Entity), g)
        self.assertNotIn((EX.foo, EX.prop, EX.bar), g)
        self.assertEqual(len(g), 4)


if __name__ == "__main__":
    unittest.main()
