vth - validation through hints
==============================

A small library that lets you create objects that are automatically validated at
runtime through type hints.

Currently supports "primitive" types and the following types from `typing`:

* Dict
* Union
* Optional
* Tuple
* List

The library can also handle nested types (such as `List[List[int]]`).
