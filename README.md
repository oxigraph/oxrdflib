Oxrdflib
========

[![PyPI](https://img.shields.io/pypi/v/oxrdflib)](https://pypi.org/project/oxrdflib/)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/oxrdflib)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/oxrdflib)
[![actions status](https://github.com/oxigraph/oxrdflib/workflows/build/badge.svg)](https://github.com/oxigraph/oxrdflib/actions)
[![Gitter](https://badges.gitter.im/oxigraph/community.svg)](https://gitter.im/oxigraph/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)

Oxrdflib provides an [rdflib](https://rdflib.readthedocs.io/) store based on [pyoxigraph](https://oxigraph.org/pyoxigraph/).
This store is named `"Oxigraph"`.

It also exposes pyoxigraph parsers and serializers as rdflib parser and serializer plugins.

Oxigraph store can be used as drop-in replacement of the rdflib default one. It support context but not formulas.
Transaction support is not implemented yet.

SPARQL query and update evaluation is done by pyoxigraph instead of rdflib if the Oxigraph store is used.
SPARQL update evaluation on `Graph` and `ConjunctiveGraph` is still done
using rdflib because of [a limitation in rdflib context management](https://github.com/RDFLib/rdflib/issues/1396).

Oxrdflib is [available on Pypi](https://pypi.org/project/oxrdflib/) and installable with:
```bash
pip install oxrdflib
```

The oxrdflib store is automatically registered as an rdflib store plugin by setuptools.

*Warning:* Oxigraph is not stable yet and its storage format might change in the future.
To migrate to future version you might have to dump and load the store content.
However, Oxigraph should be in a good enough shape to power most of use cases if you are not afraid of down time and data loss.

## API

### Store

To create a rdflib graph using the Oxigraph store use
```python
rdflib.Graph(store="Oxigraph")
```
instead of the usual
```python
rdflib.Graph()
```

Similarly, to get a dataset, use

```python
rdflib.Dataset(store="Oxigraph")
```
instead of the usual
```python
rdflib.Dataset()
```

If you want to get the store data persisted on disk, use the `open` method on the `Graph` or `Dataset` object with the directory where data should be persisted. For example:
```python
graph = rdflib.Graph(store="Oxigraph", identifier="http://example.com") # without identifier, some blank node will be used
graph.open("test_dir")
```
The store is closed with the `close()` method or automatically when Python garbage collector collects the store object.

If the `open` method is not called Oxigraph will automatically use a ramdisk on Linux and a temporary file in the other operating systems.

To do anything else, use the usual rdflib python API.

It is also possible to directly inject a [pyoxigraph `Store` object](https://pyoxigraph.readthedocs.io/en/stable/store.html#pyoxigraph.Store) directly into an Oxrdflib store:

```python
graph = rdflib.Graph(store=oxrdflib.OxigraphStore(store=pyoxigraph.Store("test_dir")))
```

This might be handy to e.g. open the database as read-only:

```python
graph = rdflib.Graph(store=oxrdflib.OxigraphStore(store=pyoxigraph.Store.read_only("test_dir")))
```

### Parsers and serializers

To use Oxigraph parser, prefix the format identifiers with `ox-`.
For example, to load data using the Oxigraph NTriples parser:
```python
graph.parse(data, format="ox-nt")
```
and to serialize to Turtle:
```python
graph.serialize(format="ox-ttl")
```

The following formats are supported:
- `ox-ntriples` (`ox-nt`)
- `ox-nquads` (`ox-nq`)
- `ox-turtle` (`ox-ttl`)
- `ox-trig`
- `ox-xml`

Note that Oxigraph parser and serializers are not 1:1 compatible with the rdflib ones and some minor differences exist.

An optimization has also been setup to skip Python entirely
if the Oxigraph parsers and serializers are used with the Oxigraph store.

## Differences with rdflib default store
- relative IRIs are not supported by Oxigraph.
- Just like the `SPARQLStore`, Oxigraph joins the `initBindings` parameter of the `query` method after the query has been evaluated, instead of injecting them at the beginning of the query.
- IRI prefixes set using the `Graph` `bind` method are not persisted on disk but kept in memory. They should be added again each time the store is opened.

## Migration guide

### From 0.2 to 0.3
* The 0.2 stores named `"OxSled"` and `"OxMemory"` have been merged into the `"Oxigraph"` store.
* The on-disk storage system provided by `"OxSled"` has been dropped and replaced by a new storage system based on [RocksDB](https://rocksdb.org/).
  To migrate you need to first dump your data in RDF using `oxrdflib` 0.2 and the `serialize` method, then upgrade to `oxrdflib` 0.3, and finally reload the data using the `parse` method.

## Development

To run the test do first `pip install -e .` to register the stores in rdflib plugin registry.
Then, `cd tests && python -m unittest` should run the tests.

The code is automatically formatted using [black](https://github.com/psf/black). A [pre-commit](https://pre-commit.com/) configuration is provided.
Run `pip install pre-commit && pre-commit install` to install pre-commit as a git pre-commit hook in your clone.
