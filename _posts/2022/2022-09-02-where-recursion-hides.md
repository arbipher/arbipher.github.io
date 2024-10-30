---
layout: post
title: Where Recursion Hides
comments: true
category:
- english
- programming-languages
---

{: .text-align-center}
![Ouroboros](https://upload.wikimedia.org/wikipedia/commons/7/71/Serpiente_alquimica.jpg)

# Disclaim:

- This blog is a working draft.
- Not going to cover the duality of recursion and corecursion this time.
- Not going to cover functional graphs this time.
- Not going to discuss recursive types, though I think comparing between recursive types, recursive functions, and recursive expressions is interesting.

# Material: Sum on the ground

```ocaml
# let rec sum n = if n = 0 then 0 else n + sum (n-1);;
val sum : int -> int = <fun>
# sum 3;;
- : int = 6
```

```python
def sum(n):
  return (0 if n == 0 else n + (sum (n-1)))

sum(3)
```

It's common to define a recursive function: in the function body, we can use the function name to refer to itself.

# Observation 1: Anonymous recursive function

What if the supposed recursive function had no name?

After defining such a function, we can give it the name `sum` and use it.

<!-- $MDX skip -->
```ocaml
let sum =
  fun n -> if n = 0 then 0 else n + <THIS_FUNCTION> (n-1)
  in
sum 3
```

I am not going to say the details in this post. The key is to use a fixed-point combinator e.g. **Y**. See [rosettacode/Y_combinator#OCaml](https://rosettacode.org/wiki/Y_combinator#OCaml).

The answer is like this:

<!-- $MDX skip -->
```ocaml
let sum' =
  y_comb (fun sum -> fun n -> if n = 0 then 0 else n + sum (n-1))
  in
sum' 3

(* the language doesn't really need `let`, we can have *)
(y_comb (fun sum -> fun n -> if n = 0 then 0 else n + sum (n-1))) 3
```

Observation 1: There are recursions **with only functions**.

# Observation 2 : Recursive name

[Recursive acronym](https://en.wikipedia.org/wiki/Recursive_acronym) is common in computer land e.g. `GNU = GNU's Not Unix`. Real people don't get stuck in reading this. They won't really expand `GNU` in the previous expanded result forever.

Can we represent this in programs?

```ocaml
# let rec gnu () : string = gnu () ^ "'s Not Unix";;
val gnu : unit -> string = <fun>

# let rec gnu : string = gnu ^ "'s Not Unix";;
Line 1, characters 24-43:
Error: This kind of expression is not allowed as right-hand side of `let rec'

# type rec_name = {part1 : rec_name; part2 : string};;
type rec_name = { part1 : rec_name; part2 : string; }

# let rec gnu : rec_name = {part1 = gnu; part2 = "'s Not Unix"};;
val gnu : rec_name = {part1 = <cycle>; part2 = "'s Not Unix"}

# let rec circle_xs = 1 :: 2 :: circle_xs;;
val circle_xs : int list = [1; 2; <cycle>]

# List.(hd (tl (tl (tl circle_xs))));;
- : int = 2
```

In OCaml, if we treat it as a function, then we can define `gnu : unit -> string`. Application of this function diverges (runs into an infinite loop, or triggers a stack-overflow). 

We cannot define a recursive string. However, we can define a recursive record or list. Recursive value is the first language extension of OCaml, stated [here](https://v2.ocaml.org/manual/letrecvalues.html).

In Haskell, we are freer to define things recursively.

```haskell
> gnu = gnu ++ "'s Not Unix"

# diverge
> take 3 gnu

> ung = "Xinu Ton \'s" ++ ung
> take 3 ung
"Xin"

> take 15 ung
"Xinu Ton 'sXinu"
```

Observation 2: There are recursions **without functions**.

# Observation 3: Mutation

```ocaml
# let sum_cell = ref (fun _ -> 0);;
val sum_cell : ('_weak1 -> int) ref = {contents = <fun>}

# sum_cell := (fun n -> if n = 0 then 0 else n + !sum_cell (n-1));;
- : unit = ()

# let sum = !sum_cell;;
val sum : int -> int = <fun>

# sum 3;;
- : int = 6
```

Using mutation, the definition of a recursive function can be split into multiple steps. Think about the problem on `THIS_FUNCTION` in Observation 1. Now the function doesn't need to know itself's name `THIS_FUNCTION` immediately. By dereferencing that cell, the function can get itself.

Observation 3: There are recursions with **mutations**.

# Observation 4: Self-reference.

Any recursion has some sort of self-reference. In recursive functions and recursive names, the self-reference is direct in the syntax (a.k.a function body itself). In anonymous function and mutation-based recursion, the self-reference is not direct in the syntax.

# Observation 5: Somewhat lazy.

Expanding a recursive name lasts for-ever. Whether evaluating around a recursive expression terminates or not is case-by-case.

Haskell is famous for its call-by-need lazy evaluation. OCaml is an eager language. However, though not specified, evaluating recursive expression must involve some sort of _laziness_ conceptually. OCaml also provides `Lazy.t`. With the `Lazy.t`, we can define more _lazy_ things in OCaml. 

```ocaml
# let rec gnu : string = gnu ^ "'s Not Unix";;
Line 1, characters 24-43:
Error: This kind of expression is not allowed as right-hand side of `let rec'

# let rec gnu : string Lazy.t = lazy ((Lazy.force gnu) ^ "'s Not Unix");;
val gnu : string lazy_t = <lazy>

# Lazy.force gnu;;
Exception: CamlinternalLazy.Undefined.

# type 'a stream = 'a streamcell Lazy.t and 'a streamcell = { head: 'a; tail: 'a stream };;
type 'a stream = 'a streamcell lazy_t
and 'a streamcell = { head : 'a; tail : 'a stream; }

# let rec ints n = lazy { head = n; tail = ints (n + 1) };;
val ints : int -> int stream = <fun>
```

OCaml's `lazy` is weaker than Haskell's native laziness. We cannot define direct a recursive string and lazy recursive string.

I started to think about these topics in mid-August. Last week, a thread [[Caml-list] coinductive data types](https://sympa.inria.fr/sympa/arc/caml-list/2022-08/msg00007.html) on OCaml mail-list asked about similar question. The stream example is from Xavier Leroy's [reply](https://sympa.inria.fr/sympa/arc/caml-list/2022-08/msg00010.html).

(t.b.c)

more:
https://en.wikipedia.org/wiki/Let_expression
https://www.cs.cornell.edu/Projects/CoCaml/