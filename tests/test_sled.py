import shutil
import unittest

from rdflib import RDF, Namespace, Literal, XSD, Graph, ConjunctiveGraph, BNode

EX = Namespace("http://example.com/")


class StoreTestCase(unittest.TestCase):
    def test_sled_store_default(self):
        g = ConjunctiveGraph("OxSled")
        self._fill_graph(g)
        self._test_graph(g)
        self.assertEqual(len(list(iter(g))), 4)

    def test_sled_store_open(self):
        g = ConjunctiveGraph("OxSled")
        g.open("test_sled")
        self._fill_graph(g)
        g.close()
        del g

        g = ConjunctiveGraph("OxSled")
        g.open("test_sled")
        self._test_graph(g)
        g.close()
        del g

        shutil.rmtree("test_sled")

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
