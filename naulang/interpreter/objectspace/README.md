# Object Space

The object space defines the types of things that Naulang can work with, from
primitive data types, such as integers and floating point numbers, to more
complex types, such as channels and functions.

The PrimitiveObject type is used to implement the primitive types.  This super
type supports several operations which mirror some of the operations in the
bytecode.  Consequently, for these primitive types, a method vtable lookup occurs in
the low level implementation (the implementation translated from RPython)
rather than in the high level interpreter, written in Python.
