import os
import unittest

from rdflib import RDF, XSD, BNode, ConjunctiveGraph, Graph, Literal, Namespace

EX = Namespace("http://example.com/")


class StoreTestCase(unittest.TestCase):
    def test_store_without_open(self):
        g = ConjunctiveGraph("Oxigraph")
        self._fill_graph(g)
        self._test_graph(g)
        self.assertEqual(len(list(iter(g))), 4)

    def test_store_with_open(self):
        g = ConjunctiveGraph("Oxigraph")
        g.open("test_store")
        self._fill_graph(g)
        g.close()
        del g
        self.assertTrue(os.path.exists("test_store"))

        g = ConjunctiveGraph("Oxigraph")
        g.open("test_store")
        self._test_graph(g)
        g.close()
        g.destroy("test_store")
        self.assertFalse(os.path.exists("test_store"))

    def test_store_with_late_open(self):
        g = ConjunctiveGraph("Oxigraph")
        g.add((EX.foo, RDF.type, EX.Entity))
        with self.assertRaises(Exception) as _:
            g.open("test_store")

    def _fill_graph(self, g: Graph):
        g.add((EX.foo, RDF.type, EX.Entity))
        g.add((EX.foo, EX.prop, BNode("123")))
        g.add((EX.foo, EX.prop1, Literal("foo")))
        g.add((EX.foo, EX.prop1, Literal("foo", lang="en")))
        g.add((EX.foo, EX.prop1, Literal("1", datatype=XSD.integer)))
        g.remove((EX.foo, EX.prop, BNode("123")))

    def _test_graph(self, g: Graph):
        self.assertIn((EX.foo, RDF.type, EX.Entity), g)
        self.assertNotIn((EX.foo, EX.prop, EX.bar), g)
        self.assertEqual(len(g), 4)


if __name__ == "__main__":
    unittest.main()
