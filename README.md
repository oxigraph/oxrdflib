Oxrdflib
========

[![PyPI](https://img.shields.io/pypi/v/oxrdflib)](https://pypi.org/project/oxrdflib/)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/oxrdflib)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/oxrdflib)
[![actions status](https://github.com/oxigraph/oxrdflib/workflows/build/badge.svg)](https://github.com/oxigraph/oxrdflib/actions)
[![Gitter](https://badges.gitter.im/oxigraph/community.svg)](https://gitter.im/oxigraph/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)

Oxrdflib provides [rdflib](https://rdflib.readthedocs.io/) stores using [pyoxigraph](https://oxigraph.org/pyoxigraph/).

The stores could be used as drop-in replacements of the rdflib default ones. They support context but not formulas.
Transaction support is not implemented yet.

SPARQL query evaluation is done by pyoxigraph instead of rdflib if an oxrdflib store is used.

Two stores are currently provided:
* An in-memory store, named `"OxMemory"`.
* A disk-based store based on the [Sled key-value store](https://sled.rs/), named `"OxSled"`.

Oxrdflib is [available on Pypi](https://pypi.org/project/oxrdflib/) and installable with:
```bash
pip install oxrdflib
```

The oxrdflib stores are automatically registered as rdflib store plugins by setuptools.

## API

### `"OxMemory"`, an in-memory store

To create a rdflib graph with pyoxigraph in memory store use
```python
rdflib.Graph(store="OxMemory")
```
instead of the usual
```python
rdflib.Graph()
```

Similarly, to get a conjunctive graph, use
```python
rdflib.ConjunctiveGraph(store="OxMemory")
```
instead of the usual
```python
rdflib.ConjunctiveGraph()
```

### `"OxSled"`, a disk-based store

The disk-based store is based on the [Sled key-value store](https://sled.rs/).
Sled is not stable yet and its storage system might change in the future.

To open Sled based graph in the directory `test_dir` use
```python
graph = rdflib.Graph(store="OxSled")
graph.open("test_dir")
```
The store is closed with the `close()` method or automatically when Python garbage collector collects the store object.

It is also possible to not provide a directory name.
In this case, a temporary directory will be created and deleted when the store is closed.
For example, this code uses a temporary directory:
```python
rdflib.Graph(store="OxSled")
```

`rdflib.ConjunctiveGraph` is also usable with `"OxSled"`.


## Development

To run the test do first `pip install -e` to register the stores in rdflib plugin registry.
Then, `cd tests && python -m unittest` should run the tests.

The code is automatically formatted using [black](https://github.com/psf/black). A [pre-commit](https://pre-commit.com/) configuration is provided.
Run `pip install pre-commit && pre-commit install` to install pre-commit as a git pre-commit hook in your clone.
