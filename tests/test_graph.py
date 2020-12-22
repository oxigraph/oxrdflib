"""
Graph test.

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
        self.graph = Graph(store="OxMemory")
        self.michel = URIRef("urn:michel")
        self.tarek = URIRef("urn:tarek")
        self.bob = URIRef("urn:bob")
        self.likes = URIRef("urn:likes")
        self.hates = URIRef("urn:hates")
        self.pizza = URIRef("urn:pizza")
        self.cheese = URIRef("urn:cheese")

    def addStuff(self):
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
        self.graph.add((bob, likes, cheese))
        self.graph.add((bob, hates, pizza))
        self.graph.add((bob, hates, michel))

    def removeStuff(self):
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

    def testAdd(self):
        self.addStuff()

    def testRemove(self):
        self.addStuff()
        self.removeStuff()

    def testTriples(self):
        tarek = self.tarek
        michel = self.michel
        bob = self.bob
        likes = self.likes
        hates = self.hates
        pizza = self.pizza
        cheese = self.cheese
        triples = self.graph.triples
        Any = None

        self.addStuff()

        # unbound subjects
        self.assertEqual(len(list(triples((Any, likes, pizza)))), 2)
        self.assertEqual(len(list(triples((Any, hates, pizza)))), 1)
        self.assertEqual(len(list(triples((Any, likes, cheese)))), 3)
        self.assertEqual(len(list(triples((Any, hates, cheese)))), 0)

        # unbound objects
        self.assertEqual(len(list(triples((michel, likes, Any)))), 2)
        self.assertEqual(len(list(triples((tarek, likes, Any)))), 2)
        self.assertEqual(len(list(triples((bob, hates, Any)))), 2)
        self.assertEqual(len(list(triples((bob, likes, Any)))), 1)

        # unbound predicates
        self.assertEqual(len(list(triples((michel, Any, cheese)))), 1)
        self.assertEqual(len(list(triples((tarek, Any, cheese)))), 1)
        self.assertEqual(len(list(triples((bob, Any, pizza)))), 1)
        self.assertEqual(len(list(triples((bob, Any, michel)))), 1)

        # unbound subject, objects
        self.assertEqual(len(list(triples((Any, hates, Any)))), 2)
        self.assertEqual(len(list(triples((Any, likes, Any)))), 5)

        # unbound predicates, objects
        self.assertEqual(len(list(triples((michel, Any, Any)))), 2)
        self.assertEqual(len(list(triples((bob, Any, Any)))), 3)
        self.assertEqual(len(list(triples((tarek, Any, Any)))), 2)

        # unbound subjects, predicates
        self.assertEqual(len(list(triples((Any, Any, pizza)))), 3)
        self.assertEqual(len(list(triples((Any, Any, cheese)))), 3)
        self.assertEqual(len(list(triples((Any, Any, michel)))), 1)

        # all unbound
        self.assertEqual(len(list(triples((Any, Any, Any)))), 7)
        self.removeStuff()
        self.assertEqual(len(list(triples((Any, Any, Any)))), 0)

    def testConnected(self):
        graph = self.graph
        self.addStuff()
        self.assertEqual(True, graph.connected())

        jeroen = URIRef("urn:jeroen")
        unconnected = URIRef("urn:unconnected")

        graph.add((jeroen, self.likes, unconnected))

        self.assertEqual(False, graph.connected())

    def testSub(self):
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

    def testGraphAdd(self):
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

    def testGraphIntersection(self):
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
