---
layout: post
title: Open-source randoms
comments: true
category:
- english
- programming-languages
- subjective
---

Any programming language is a DSL based on pure lambda calculus (PLC).

PLC provides the programmable controls including binding and abstraction. The rest of the language is usually stand-alone modules, e.g. integer module, string module. We call them the lambda part and the algebra part.

The dichotomy of programmablity and inner module operations give a new viewpoint of programming languages. Without the programmablity, the module operations are usually safe and closed (or unclosed at its own right).

With this view, the type also has two sources: the lambda part and the algebra part. The types from the lambda part has more freedom and design choices. It can even be _untyped_: you can allow functions to accept any terms (considering the types of the parameters). The types from the algebra part must be _typed_: a mis-used operations e.g. `Int.add 1 "foo"` either result in a type-error or a run-time error because it's meaningless.

With this view, data structures are also specific modules with operations.

The computational level of the language is usually determined by the lambda part. It can be turing-complete or not, and it can be dependent-typed or not.

I don't consider encoding sth into lambda part too much here.

The dichotomy also implies two kind of variables. One id over the possible values inside a module is a value for must-safe values, e.g. `x + y` when `x` and `y` are elements of `Int`. The other id comes from the lambda part e.g. `fun x y -> x + y`. These `x` and `y` are not always elements of `Int`.

Common languages usually have printing functions that can print any types to string. Does this belong to the lambda part or the algebra part? When algebra part has more modules, it's natural that some functions are inter-modules, which should belong to another special module.