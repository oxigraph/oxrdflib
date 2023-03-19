"""Graph test.

Code from https://github.com/RDFLib/rdflib/blob/91037207580838e41c07eb457bd65d7cc6d6ed85/test/test_graph.py

Copyright (c) 2002-2017, RDFLib Team
See CONTRIBUTORS and urn:github.com/RDFLib/rdflib
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

  * Redistributions of source code must retain the above copyright
notice, this list of conditions and the following disclaimer.

  * Redistributions in binary form must reproduce the above
copyright notice, this list of conditions and the following
disclaimer in the documentation and/or other materials provided
with the distribution.

  * Neither the name of Daniel Krech nor the names of its
contributors may be used to endorse or promote products derived
from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import unittest

from rdflib import Graph, URIRef


class GraphTestCase(unittest.TestCase):
    def setUp(self):
        self.graph = Graph(store="Oxigraph")
        self.michel = URIRef("urn:michel")
        self.tarek = URIRef("urn:tarek")
        self.bob = URIRef("urn:bob")
        self.likes = URIRef("urn:likes")
        self.hates = URIRef("urn:hates")
        self.pizza = URIRef("urn:pizza")
        self.cheese = URIRef("urn:cheese")

    def add_stuff(self):
        tarek = self.tarek
        michel = self.michel
        bob = self.bob
        likes = self.likes
        hates = self.hates
        pizza = self.pizza
        cheese = self.cheese

        self.graph.add((tarek, likes, pizza))
        self.graph.add((tarek, likes, cheese))
        self.graph.add((michel, likes, pizza))
        self.graph.add((michel, likes, cheese))
        self.graph.addN(
            [(bob, likes, cheese, self.graph), (bob, hates, pizza, self.graph), (bob, hates, michel, self.graph)]
        )

    def remove_stuff(self):
        tarek = self.tarek
        michel = self.michel
        bob = self.bob
        likes = self.likes
        hates = self.hates
        pizza = self.pizza
        cheese = self.cheese

        self.graph.remove((tarek, likes, pizza))
        self.graph.remove((tarek, likes, cheese))
        self.graph.remove((michel, likes, pizza))
        self.graph.remove((michel, likes, cheese))
        self.graph.remove((bob, likes, cheese))
        self.graph.remove((bob, hates, pizza))
        self.graph.remove((bob, hates, michel))  # gasp!

    def test_add(self):
        self.add_stuff()

    def test_remove(self):
        self.add_stuff()
        self.remove_stuff()

    def test_triples(self):
        tarek = self.tarek
        michel = self.michel
        bob = self.bob
        likes = self.likes
        hates = self.hates
        pizza = self.pizza
        cheese = self.cheese
        triples = self.graph.triples

        self.add_stuff()

        # unbound subjects
        self.assertEqual(len(list(triples((None, likes, pizza)))), 2)
        self.assertEqual(len(list(triples((None, hates, pizza)))), 1)
        self.assertEqual(len(list(triples((None, likes, cheese)))), 3)
        self.assertEqual(len(list(triples((None, hates, cheese)))), 0)

        # unbound objects
        self.assertEqual(len(list(triples((michel, likes, None)))), 2)
        self.assertEqual(len(list(triples((tarek, likes, None)))), 2)
        self.assertEqual(len(list(triples((bob, hates, None)))), 2)
        self.assertEqual(len(list(triples((bob, likes, None)))), 1)

        # unbound predicates
        self.assertEqual(len(list(triples((michel, None, cheese)))), 1)
        self.assertEqual(len(list(triples((tarek, None, cheese)))), 1)
        self.assertEqual(len(list(triples((bob, None, pizza)))), 1)
        self.assertEqual(len(list(triples((bob, None, michel)))), 1)

        # unbound subject, objects
        self.assertEqual(len(list(triples((None, hates, None)))), 2)
        self.assertEqual(len(list(triples((None, likes, None)))), 5)

        # unbound predicates, objects
        self.assertEqual(len(list(triples((michel, None, None)))), 2)
        self.assertEqual(len(list(triples((bob, None, None)))), 3)
        self.assertEqual(len(list(triples((tarek, None, None)))), 2)

        # unbound subjects, predicates
        self.assertEqual(len(list(triples((None, None, pizza)))), 3)
        self.assertEqual(len(list(triples((None, None, cheese)))), 3)
        self.assertEqual(len(list(triples((None, None, michel)))), 1)

        # all unbound
        self.assertEqual(len(list(triples((None, None, None)))), 7)
        self.remove_stuff()
        self.assertEqual(len(list(triples((None, None, None)))), 0)

    def test_connected(self):
        graph = self.graph
        self.add_stuff()
        self.assertEqual(True, graph.connected())

        jeroen = URIRef("urn:jeroen")
        unconnected = URIRef("urn:unconnected")

        graph.add((jeroen, self.likes, unconnected))

        self.assertEqual(False, graph.connected())

    def test_sub(self):
        g1 = self.graph
        g2 = Graph(store=g1.store)

        tarek = self.tarek
        bob = self.bob
        likes = self.likes
        pizza = self.pizza
        cheese = self.cheese

        g1.add((tarek, likes, pizza))
        g1.add((bob, likes, cheese))

        g2.add((bob, likes, cheese))

        g3 = g1 - g2

        self.assertEqual(len(g3), 1)
        self.assertEqual((tarek, likes, pizza) in g3, True)
        self.assertEqual((tarek, likes, cheese) in g3, False)

        self.assertEqual((bob, likes, cheese) in g3, False)

        g1 -= g2

        self.assertEqual(len(g1), 1)
        self.assertEqual((tarek, likes, pizza) in g1, True)
        self.assertEqual((tarek, likes, cheese) in g1, False)

        self.assertEqual((bob, likes, cheese) in g1, False)

    def test_graph_add(self):
        g1 = self.graph
        g2 = Graph(store=g1.store)

        tarek = self.tarek
        bob = self.bob
        likes = self.likes
        pizza = self.pizza
        cheese = self.cheese

        g1.add((tarek, likes, pizza))

        g2.add((bob, likes, cheese))

        g3 = g1 + g2

        self.assertEqual(len(g3), 2)
        self.assertEqual((tarek, likes, pizza) in g3, True)
        self.assertEqual((tarek, likes, cheese) in g3, False)

        self.assertEqual((bob, likes, cheese) in g3, True)

        g1 += g2

        self.assertEqual(len(g1), 2)
        self.assertEqual((tarek, likes, pizza) in g1, True)
        self.assertEqual((tarek, likes, cheese) in g1, False)

        self.assertEqual((bob, likes, cheese) in g1, True)

    def test_graph_intersection(self):
        g1 = self.graph
        g2 = Graph(store=g1.store)

        tarek = self.tarek
        michel = self.michel
        bob = self.bob
        likes = self.likes
        pizza = self.pizza
        cheese = self.cheese

        g1.add((tarek, likes, pizza))
        g1.add((michel, likes, cheese))

        g2.add((bob, likes, cheese))
        g2.add((michel, likes, cheese))

        g3 = g1 * g2

        self.assertEqual(len(g3), 1)
        self.assertEqual((tarek, likes, pizza) in g3, False)
        self.assertEqual((tarek, likes, cheese) in g3, False)

        self.assertEqual((bob, likes, cheese) in g3, False)
        self.assertEqual((michel, likes, cheese) in g3, True)

        g1 *= g2

        self.assertEqual(len(g1), 1)

        self.assertEqual((tarek, likes, pizza) in g1, False)
        self.assertEqual((tarek, likes, cheese) in g1, False)

        self.assertEqual((bob, likes, cheese) in g1, False)

        self.assertEqual((michel, likes, cheese) in g1, True)


if __name__ == "__main__":
    unittest.main()
