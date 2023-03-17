"""Dataset test.

Code from https://github.com/RDFLib/rdflib/blob/91037207580838e41c07eb457bd65d7cc6d6ed85/test/test_dataset.py

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

from rdflib import Dataset, URIRef
from rdflib.graph import DATASET_DEFAULT_GRAPH_ID


class DatasetTestCase(unittest.TestCase):
    def setUp(self):
        self.graph = Dataset(store="Oxigraph")
        self.michel = URIRef("urn:michel")
        self.tarek = URIRef("urn:tarek")
        self.bob = URIRef("urn:bob")
        self.likes = URIRef("urn:likes")
        self.hates = URIRef("urn:hates")
        self.pizza = URIRef("urn:pizza")
        self.cheese = URIRef("urn:cheese")

        # Use regular URIs because SPARQL endpoints like Fuseki alter short names
        self.c1 = URIRef("urn:context-1")
        self.c2 = URIRef("urn:context-2")

        # delete the graph for each test!
        self.graph.remove((None, None, None))
        for c in self.graph.contexts():
            c.remove((None, None, None))
            self.assertEqual(len(c), 0)
            self.graph.remove_graph(c)

    def tearDown(self):
        self.graph.close()

    def test_graph_aware(self):
        if not self.graph.store.graph_aware:
            return

        g = self.graph
        g1 = g.graph(self.c1)

        # added graph exists
        self.assertEqual(
            {x.identifier for x in self.graph.contexts()},
            {self.c1, DATASET_DEFAULT_GRAPH_ID},
        )

        # added graph is empty
        self.assertEqual(len(g1), 0)

        g1.add((self.tarek, self.likes, self.pizza))

        # added graph still exists
        self.assertEqual(
            {x.identifier for x in self.graph.contexts()},
            {self.c1, DATASET_DEFAULT_GRAPH_ID},
        )

        # added graph contains one triple
        self.assertEqual(len(g1), 1)

        g1.remove((self.tarek, self.likes, self.pizza))

        # added graph is empty
        self.assertEqual(len(g1), 0)

        # graph still exists, although empty
        self.assertEqual(
            {x.identifier for x in self.graph.contexts()},
            {self.c1, DATASET_DEFAULT_GRAPH_ID},
        )

        g.remove_graph(self.c1)

        # graph is gone
        self.assertEqual(
            {x.identifier for x in self.graph.contexts()},
            {DATASET_DEFAULT_GRAPH_ID},
        )

    def test_default_graph(self):
        self.graph.add((self.tarek, self.likes, self.pizza))
        self.assertEqual(len(self.graph), 1)
        # only default exists
        self.assertEqual(
            {x.identifier for x in self.graph.contexts()},
            {DATASET_DEFAULT_GRAPH_ID},
        )

        # removing default graph removes triples but not actual graph
        self.graph.remove_graph(DATASET_DEFAULT_GRAPH_ID)

        self.assertEqual(len(self.graph), 0)
        # default still exists
        self.assertEqual(
            {x.identifier for x in self.graph.contexts()},
            {DATASET_DEFAULT_GRAPH_ID},
        )

    def test_not_union(self):
        g1 = self.graph.graph(self.c1)
        g1.add((self.tarek, self.likes, self.pizza))

        self.assertEqual(list(self.graph.objects(self.tarek, None)), [])
        self.assertEqual(list(g1.objects(self.tarek, None)), [self.pizza])


if __name__ == "__main__":
    unittest.main()
