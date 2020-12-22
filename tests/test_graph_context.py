"""
Graph context test.

Code from https://github.com/RDFLib/rdflib/blob/91037207580838e41c07eb457bd65d7cc6d6ed85/test/test_graph_context.py

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

from rdflib import BNode, ConjunctiveGraph, Graph, URIRef


class ContextTestCase(unittest.TestCase):
    def setUp(self):
        self.graph = ConjunctiveGraph(store="OxMemory")
        self.michel = URIRef("urn:michel")
        self.tarek = URIRef("urn:tarek")
        self.bob = URIRef("urn:bob")
        self.likes = URIRef("urn:likes")
        self.hates = URIRef("urn:hates")
        self.pizza = URIRef("urn:pizza")
        self.cheese = URIRef("urn:cheese")

        self.c1 = URIRef("urn:context-1")
        self.c2 = URIRef("urn:context-2")

        # delete the graph for each test!
        self.graph.remove((None, None, None))

    def addStuff(self):
        tarek = self.tarek
        michel = self.michel
        bob = self.bob
        likes = self.likes
        hates = self.hates
        pizza = self.pizza
        cheese = self.cheese
        c1 = self.c1
        graph = Graph(self.graph.store, c1)

        graph.add((tarek, likes, pizza))
        graph.add((tarek, likes, cheese))
        graph.add((michel, likes, pizza))
        graph.add((michel, likes, cheese))
        graph.add((bob, likes, cheese))
        graph.add((bob, hates, pizza))
        graph.add((bob, hates, michel))  # gasp!

    def removeStuff(self):
        tarek = self.tarek
        michel = self.michel
        bob = self.bob
        likes = self.likes
        hates = self.hates
        pizza = self.pizza
        cheese = self.cheese
        c1 = self.c1
        graph = Graph(self.graph.store, c1)

        graph.remove((tarek, likes, pizza))
        graph.remove((tarek, likes, cheese))
        graph.remove((michel, likes, pizza))
        graph.remove((michel, likes, cheese))
        graph.remove((bob, likes, cheese))
        graph.remove((bob, hates, pizza))
        graph.remove((bob, hates, michel))  # gasp!

    def addStuffInMultipleContexts(self):
        c1 = self.c1
        c2 = self.c2
        triple = (self.pizza, self.hates, self.tarek)  # revenge!

        # add to default context
        self.graph.add(triple)
        # add to context 1
        graph = Graph(self.graph.store, c1)
        graph.add(triple)
        # add to context 2
        graph = Graph(self.graph.store, c2)
        graph.add(triple)

    def testConjunction(self):
        self.addStuffInMultipleContexts()
        triple = (self.pizza, self.likes, self.pizza)
        # add to context 1
        graph = Graph(self.graph.store, self.c1)
        graph.add(triple)
        self.assertEqual(len(self.graph), len(graph))

    def testAdd(self):
        self.addStuff()

    def testRemove(self):
        self.addStuff()
        self.removeStuff()

    def testLenInOneContext(self):
        c1 = self.c1
        # make sure context is empty

        self.graph.remove_context(self.graph.get_context(c1))
        graph = Graph(self.graph.store, c1)
        oldLen = len(self.graph)

        for i in range(0, 10):
            graph.add((BNode(), self.hates, self.hates))
        self.assertEqual(len(graph), oldLen + 10)
        self.assertEqual(len(self.graph.get_context(c1)), oldLen + 10)
        self.graph.remove_context(self.graph.get_context(c1))
        self.assertEqual(len(self.graph), oldLen)
        self.assertEqual(len(graph), 0)

    def testLenInMultipleContexts(self):
        oldLen = len(self.graph)
        self.addStuffInMultipleContexts()

        # addStuffInMultipleContexts is adding the same triple to
        # three different contexts. So it's only + 1
        self.assertEqual(len(self.graph), oldLen + 1)

        graph = Graph(self.graph.store, self.c1)
        self.assertEqual(len(graph), oldLen + 1)

    def testRemoveInMultipleContexts(self):
        c1 = self.c1
        c2 = self.c2
        triple = (self.pizza, self.hates, self.tarek)  # revenge!

        self.addStuffInMultipleContexts()

        # triple should be still in store after removing it from c1 + c2
        self.assertTrue(triple in self.graph)
        graph = Graph(self.graph.store, c1)
        graph.remove(triple)
        self.assertTrue(triple in self.graph)
        graph = Graph(self.graph.store, c2)
        graph.remove(triple)
        self.assertTrue(triple in self.graph)
        self.graph.remove(triple)
        # now gone!
        self.assertTrue(triple not in self.graph)

        # add again and see if remove without context removes all triples!
        self.addStuffInMultipleContexts()
        self.graph.remove(triple)
        self.assertTrue(triple not in self.graph)

    def testContexts(self):
        triple = (self.pizza, self.hates, self.tarek)  # revenge!

        self.addStuffInMultipleContexts()

        def cid(c):
            return c.identifier

        self.assertTrue(self.c1 in map(cid, self.graph.contexts()))
        self.assertTrue(self.c2 in map(cid, self.graph.contexts()))

        context_list = list(map(cid, list(self.graph.contexts(triple))))
        self.assertTrue(self.c1 in context_list, (self.c1, context_list))
        self.assertTrue(self.c2 in context_list, (self.c2, context_list))

    def testRemoveContext(self):
        c1 = self.c1

        self.addStuffInMultipleContexts()
        self.assertEqual(len(Graph(self.graph.store, c1)), 1)
        self.assertEqual(len(self.graph.get_context(c1)), 1)

        self.graph.remove_context(self.graph.get_context(c1))
        self.assertTrue(self.c1 not in self.graph.contexts())

    def testRemoveAny(self):
        Any = None
        self.addStuffInMultipleContexts()
        self.graph.remove((Any, Any, Any))
        self.assertEqual(len(self.graph), 0)

    def testTriples(self):
        tarek = self.tarek
        michel = self.michel
        bob = self.bob
        likes = self.likes
        hates = self.hates
        pizza = self.pizza
        cheese = self.cheese
        c1 = self.c1
        triples = self.graph.triples
        graph = self.graph
        c1graph = Graph(self.graph.store, c1)
        c1triples = c1graph.triples
        Any = None

        self.addStuff()

        # unbound subjects with context
        self.assertEqual(len(list(c1triples((Any, likes, pizza)))), 2)
        self.assertEqual(len(list(c1triples((Any, hates, pizza)))), 1)
        self.assertEqual(len(list(c1triples((Any, likes, cheese)))), 3)
        self.assertEqual(len(list(c1triples((Any, hates, cheese)))), 0)

        # unbound subjects without context, same results!
        self.assertEqual(len(list(triples((Any, likes, pizza)))), 2)
        self.assertEqual(len(list(triples((Any, hates, pizza)))), 1)
        self.assertEqual(len(list(triples((Any, likes, cheese)))), 3)
        self.assertEqual(len(list(triples((Any, hates, cheese)))), 0)

        # unbound objects with context
        self.assertEqual(len(list(c1triples((michel, likes, Any)))), 2)
        self.assertEqual(len(list(c1triples((tarek, likes, Any)))), 2)
        self.assertEqual(len(list(c1triples((bob, hates, Any)))), 2)
        self.assertEqual(len(list(c1triples((bob, likes, Any)))), 1)

        # unbound objects without context, same results!
        self.assertEqual(len(list(triples((michel, likes, Any)))), 2)
        self.assertEqual(len(list(triples((tarek, likes, Any)))), 2)
        self.assertEqual(len(list(triples((bob, hates, Any)))), 2)
        self.assertEqual(len(list(triples((bob, likes, Any)))), 1)

        # unbound predicates with context
        self.assertEqual(len(list(c1triples((michel, Any, cheese)))), 1)
        self.assertEqual(len(list(c1triples((tarek, Any, cheese)))), 1)
        self.assertEqual(len(list(c1triples((bob, Any, pizza)))), 1)
        self.assertEqual(len(list(c1triples((bob, Any, michel)))), 1)

        # unbound predicates without context, same results!
        self.assertEqual(len(list(triples((michel, Any, cheese)))), 1)
        self.assertEqual(len(list(triples((tarek, Any, cheese)))), 1)
        self.assertEqual(len(list(triples((bob, Any, pizza)))), 1)
        self.assertEqual(len(list(triples((bob, Any, michel)))), 1)

        # unbound subject, objects with context
        self.assertEqual(len(list(c1triples((Any, hates, Any)))), 2)
        self.assertEqual(len(list(c1triples((Any, likes, Any)))), 5)

        # unbound subject, objects without context, same results!
        self.assertEqual(len(list(triples((Any, hates, Any)))), 2)
        self.assertEqual(len(list(triples((Any, likes, Any)))), 5)

        # unbound predicates, objects with context
        self.assertEqual(len(list(c1triples((michel, Any, Any)))), 2)
        self.assertEqual(len(list(c1triples((bob, Any, Any)))), 3)
        self.assertEqual(len(list(c1triples((tarek, Any, Any)))), 2)

        # unbound predicates, objects without context, same results!
        self.assertEqual(len(list(triples((michel, Any, Any)))), 2)
        self.assertEqual(len(list(triples((bob, Any, Any)))), 3)
        self.assertEqual(len(list(triples((tarek, Any, Any)))), 2)

        # unbound subjects, predicates with context
        self.assertEqual(len(list(c1triples((Any, Any, pizza)))), 3)
        self.assertEqual(len(list(c1triples((Any, Any, cheese)))), 3)
        self.assertEqual(len(list(c1triples((Any, Any, michel)))), 1)

        # unbound subjects, predicates without context, same results!
        self.assertEqual(len(list(triples((Any, Any, pizza)))), 3)
        self.assertEqual(len(list(triples((Any, Any, cheese)))), 3)
        self.assertEqual(len(list(triples((Any, Any, michel)))), 1)

        # all unbound with context
        self.assertEqual(len(list(c1triples((Any, Any, Any)))), 7)
        # all unbound without context, same result!
        self.assertEqual(len(list(triples((Any, Any, Any)))), 7)

        for c in [graph, self.graph.get_context(c1)]:
            # unbound subjects
            self.assertEqual(set(c.subjects(likes, pizza)), {michel, tarek})
            self.assertEqual(set(c.subjects(hates, pizza)), {bob})
            self.assertEqual(set(c.subjects(likes, cheese)), {tarek, bob, michel})
            self.assertEqual(set(c.subjects(hates, cheese)), set())

            # unbound objects
            self.assertEqual(set(c.objects(michel, likes)), {cheese, pizza})
            self.assertEqual(set(c.objects(tarek, likes)), {cheese, pizza})
            self.assertEqual(set(c.objects(bob, hates)), {michel, pizza})
            self.assertEqual(set(c.objects(bob, likes)), {cheese})

            # unbound predicates
            self.assertEqual(set(c.predicates(michel, cheese)), {likes})
            self.assertEqual(set(c.predicates(tarek, cheese)), {likes})
            self.assertEqual(set(c.predicates(bob, pizza)), {hates})
            self.assertEqual(set(c.predicates(bob, michel)), {hates})

            self.assertEqual(set(c.subject_objects(hates)), {(bob, pizza), (bob, michel)})
            self.assertEqual(
                set(c.subject_objects(likes)),
                {(tarek, cheese), (michel, cheese), (michel, pizza), (bob, cheese), (tarek, pizza)},
            )

            self.assertEqual(set(c.predicate_objects(michel)), {(likes, cheese), (likes, pizza)})
            self.assertEqual(set(c.predicate_objects(bob)), {(likes, cheese), (hates, pizza), (hates, michel)})
            self.assertEqual(set(c.predicate_objects(tarek)), {(likes, cheese), (likes, pizza)})

            self.assertEqual(set(c.subject_predicates(pizza)), {(bob, hates), (tarek, likes), (michel, likes)})
            self.assertEqual(set(c.subject_predicates(cheese)), {(bob, likes), (tarek, likes), (michel, likes)})
            self.assertEqual(set(c.subject_predicates(michel)), {(bob, hates)})

            self.assertEqual(
                set(c),
                {
                    (bob, hates, michel),
                    (bob, likes, cheese),
                    (tarek, likes, pizza),
                    (michel, likes, pizza),
                    (michel, likes, cheese),
                    (bob, hates, pizza),
                    (tarek, likes, cheese),
                },
            )

        # remove stuff and make sure the graph is empty again
        self.removeStuff()
        self.assertEqual(len(list(c1triples((Any, Any, Any)))), 0)
        self.assertEqual(len(list(triples((Any, Any, Any)))), 0)


if __name__ == "__main__":
    unittest.main()
