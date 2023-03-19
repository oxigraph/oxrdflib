"""Graph context test.

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
        self.graph = ConjunctiveGraph(store="Oxigraph")
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

    def add_stuff(self):
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
        self.graph.addN([(bob, likes, cheese, graph), (bob, hates, pizza, graph), (bob, hates, michel, graph)])

    def remove_stuff(self):
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

    def add_stuff_in_multiple_contexts(self):
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

    def test_conjunction(self):
        self.add_stuff_in_multiple_contexts()
        triple = (self.pizza, self.likes, self.pizza)
        # add to context 1
        graph = Graph(self.graph.store, self.c1)
        graph.add(triple)
        self.assertEqual(len(self.graph), len(graph))

    def test_add(self):
        self.add_stuff()

    def test_remove(self):
        self.add_stuff()
        self.remove_stuff()

    def test_len_in_one_context(self):
        c1 = self.c1
        # make sure context is empty

        self.graph.remove_context(self.graph.get_context(c1))
        graph = Graph(self.graph.store, c1)
        old_len = len(self.graph)

        for _ in range(0, 10):
            graph.add((BNode(), self.hates, self.hates))
        self.assertEqual(len(graph), old_len + 10)
        self.assertEqual(len(self.graph.get_context(c1)), old_len + 10)
        self.graph.remove_context(self.graph.get_context(c1))
        self.assertEqual(len(self.graph), old_len)
        self.assertEqual(len(graph), 0)

    def test_len_in_multiple_contexts(self):
        old_len = len(self.graph)
        self.add_stuff_in_multiple_contexts()

        # addStuffInMultipleContexts is adding the same triple to
        # three different contexts. So it's only + 1
        self.assertEqual(len(self.graph), old_len + 1)

        graph = Graph(self.graph.store, self.c1)
        self.assertEqual(len(graph), old_len + 1)

    def test_remove_in_multiple_contexts(self):
        c1 = self.c1
        c2 = self.c2
        triple = (self.pizza, self.hates, self.tarek)  # revenge!

        self.add_stuff_in_multiple_contexts()

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
        self.add_stuff_in_multiple_contexts()
        self.graph.remove(triple)
        self.assertTrue(triple not in self.graph)

    def test_contexts(self):
        triple = (self.pizza, self.hates, self.tarek)  # revenge!

        self.add_stuff_in_multiple_contexts()

        def cid(c):
            return c.identifier

        self.assertTrue(self.c1 in map(cid, self.graph.contexts()))
        self.assertTrue(self.c2 in map(cid, self.graph.contexts()))

        context_list = list(map(cid, list(self.graph.contexts(triple))))
        self.assertTrue(self.c1 in context_list, (self.c1, context_list))
        self.assertTrue(self.c2 in context_list, (self.c2, context_list))

    def test_remove_context(self):
        c1 = self.c1

        self.add_stuff_in_multiple_contexts()
        self.assertEqual(len(Graph(self.graph.store, c1)), 1)
        self.assertEqual(len(self.graph.get_context(c1)), 1)

        self.graph.remove_context(self.graph.get_context(c1))
        self.assertTrue(self.c1 not in self.graph.contexts())

    def test_remove_any(self):
        self.add_stuff_in_multiple_contexts()
        self.graph.remove((None, None, None))
        self.assertEqual(len(self.graph), 0)

    def test_triples(self):
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

        self.add_stuff()

        # unbound subjects with context
        self.assertEqual(len(list(c1triples((None, likes, pizza)))), 2)
        self.assertEqual(len(list(c1triples((None, hates, pizza)))), 1)
        self.assertEqual(len(list(c1triples((None, likes, cheese)))), 3)
        self.assertEqual(len(list(c1triples((None, hates, cheese)))), 0)

        # unbound subjects without context, same results!
        self.assertEqual(len(list(triples((None, likes, pizza)))), 2)
        self.assertEqual(len(list(triples((None, hates, pizza)))), 1)
        self.assertEqual(len(list(triples((None, likes, cheese)))), 3)
        self.assertEqual(len(list(triples((None, hates, cheese)))), 0)

        # unbound objects with context
        self.assertEqual(len(list(c1triples((michel, likes, None)))), 2)
        self.assertEqual(len(list(c1triples((tarek, likes, None)))), 2)
        self.assertEqual(len(list(c1triples((bob, hates, None)))), 2)
        self.assertEqual(len(list(c1triples((bob, likes, None)))), 1)

        # unbound objects without context, same results!
        self.assertEqual(len(list(triples((michel, likes, None)))), 2)
        self.assertEqual(len(list(triples((tarek, likes, None)))), 2)
        self.assertEqual(len(list(triples((bob, hates, None)))), 2)
        self.assertEqual(len(list(triples((bob, likes, None)))), 1)

        # unbound predicates with context
        self.assertEqual(len(list(c1triples((michel, None, cheese)))), 1)
        self.assertEqual(len(list(c1triples((tarek, None, cheese)))), 1)
        self.assertEqual(len(list(c1triples((bob, None, pizza)))), 1)
        self.assertEqual(len(list(c1triples((bob, None, michel)))), 1)

        # unbound predicates without context, same results!
        self.assertEqual(len(list(triples((michel, None, cheese)))), 1)
        self.assertEqual(len(list(triples((tarek, None, cheese)))), 1)
        self.assertEqual(len(list(triples((bob, None, pizza)))), 1)
        self.assertEqual(len(list(triples((bob, None, michel)))), 1)

        # unbound subject, objects with context
        self.assertEqual(len(list(c1triples((None, hates, None)))), 2)
        self.assertEqual(len(list(c1triples((None, likes, None)))), 5)

        # unbound subject, objects without context, same results!
        self.assertEqual(len(list(triples((None, hates, None)))), 2)
        self.assertEqual(len(list(triples((None, likes, None)))), 5)

        # unbound predicates, objects with context
        self.assertEqual(len(list(c1triples((michel, None, None)))), 2)
        self.assertEqual(len(list(c1triples((bob, None, None)))), 3)
        self.assertEqual(len(list(c1triples((tarek, None, None)))), 2)

        # unbound predicates, objects without context, same results!
        self.assertEqual(len(list(triples((michel, None, None)))), 2)
        self.assertEqual(len(list(triples((bob, None, None)))), 3)
        self.assertEqual(len(list(triples((tarek, None, None)))), 2)

        # unbound subjects, predicates with context
        self.assertEqual(len(list(c1triples((None, None, pizza)))), 3)
        self.assertEqual(len(list(c1triples((None, None, cheese)))), 3)
        self.assertEqual(len(list(c1triples((None, None, michel)))), 1)

        # unbound subjects, predicates without context, same results!
        self.assertEqual(len(list(triples((None, None, pizza)))), 3)
        self.assertEqual(len(list(triples((None, None, cheese)))), 3)
        self.assertEqual(len(list(triples((None, None, michel)))), 1)

        # all unbound with context
        self.assertEqual(len(list(c1triples((None, None, None)))), 7)
        # all unbound without context, same result!
        self.assertEqual(len(list(triples((None, None, None)))), 7)

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
        self.remove_stuff()
        self.assertEqual(len(list(c1triples((None, None, None)))), 0)
        self.assertEqual(len(list(triples((None, None, None)))), 0)


if __name__ == "__main__":
    unittest.main()
