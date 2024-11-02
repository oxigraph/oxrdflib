## [0.4.0] - 2024-11-02

### Added
- Oxigraph native parsers and serializers for N-Triples, N-Quads, Turtle, TriG, N3 and RDF/XML.

### Removed
- `OxMemory` and `OxSled` aliases.

### Changed
- Upgrades pyoxigraph to 0.4.
- `Dataset` `update` evaluation is now done using pyoxigraph and not rdflib.
- Restructures the codebase to account for further additions of parsers and serializers.


## [0.3.7] - 2024-03-30

### Changed
- Fixes JSON-LD serialization by allowing invalid triple patterns in the `Store.triple` function.


## [0.3.6] - 2023-08-02

### Added
- Compatibility with rdflib 7.0


## [0.3.5] - 2023-06-21

### Changed
- Fixes `Store.triples` and `Store.context` return types.


## [0.3.4] - 2023-04-22

### Changed
- Fixes support of rdflib `Query` object in `Store.query`.


## [0.3.3] - 2023-03-20

### Added
- Implements directly `Store.addN` method.
- Allows to inject the `pyoxigraph.Store` object directly into `OxigraphStore`.

### Changed
- Migrates setuptools configuration to `pyproject.toml`.
- Adds type annotation.


## [0.3.2] - 2022-08-03

### Changed
- Fixes compatibility with rdflib 6.2 (`bind` method signature change).
- Upgrades pyoxigraph requirement to 0.3.5 to make sure that bug fixes are also deployed when upgrading oxrdflib.


## [0.3.1] - 2022-04-02

### Added
- `OxigraphStore` now implements the `bind` method allowing to set namespaces.
  These namespaces are not persisted on disk.
- The `query` method now injects the namespaces set in the `Graph` object (including the ones set by default in rdflib) inside of SPARQL queries.

### Changed
- The default branch is now named `main` and not `master`.


## [0.3.0] - 2022-03-19

### Added
- `OxigraphStore` that provides both in-memory and disk-based storage.
  The storage format is not compatible with the one of the `SledStore`.

### Removed
- `MemoryStore` and `SledStore`
- Compatibility with Python 3.6 and rdflib 4 and 5.


## [0.2.1] - 2022-03-12

### Added
- Compatibility with rdflib 6.


## [0.2.0] - 2021-01-07

### Added
- `MemoryStore` in memory rdflib storage using Oxigraph.
- `SledStore` in disk-based rdflib storage using Oxigraph.
