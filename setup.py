import pathlib

from setuptools import setup

setup(
    name="oxrdflib",
    version="0.2.1",
    description="rdflib stores based on pyoxigraph",
    long_description=(pathlib.Path(__file__).parent / "README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/oxigraph/oxrdflib",
    author="Tpt",
    author_email="thomas@pellissier-tanon.fr",
    license="BSD-3-Clause",
    platforms=["any"],
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: BSD License",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Database :: Database Engines/Servers",
    ],
    project_urls={
        "Documentation": "https://github.com/oxigraph/oxrdflib/blob/master/README.md",
        "Source": "https://github.com/oxigraph/oxrdflib",
        "Tracker": "https://github.com/oxigraph/oxrdflib/issues",
    },
    packages=["oxrdflib"],
    install_requires=["pyoxigraph>=0.2,<0.3", "rdflib>=4.0,<7.0"],
    entry_points={"rdf.plugins.store": ["OxMemory = oxrdflib:MemoryOxStore", "OxSled = oxrdflib:SledOxStore"]},
    include_package_data=True,
)
