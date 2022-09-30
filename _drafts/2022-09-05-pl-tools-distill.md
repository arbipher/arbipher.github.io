---
layout: post
title: PL Tools Distill
comments: true
category:
- english
- programming-languages
---

# Disclaim:

- This blog is a working draft and half-done (This sentence makes me relief).
- It's too late today. I don't run any spellcheck or even read it once.
- But it's fine. A terrible-written blog follows the Matt's [blog]({{ site.baseurl }}{% link _posts/2022/2022-08-08-writing-blogs.md %}) tip: take it easy!

# Main

Sometimes I am asked by other PhD students in the department on _how do PL people think about this question_, _how this topic is studies in PL_, _what is the PL persepective on this_. This is already the question on level 3. In the beginning, the question is usually (level 1) _what is PL_ asked by enough many people, after I saying I am doing PL research. Then level 2 quesiton is what do you research. For this question, I strongly suggest Mike Hicks's answer [[1]](http://www.pl-enthusiast.net/2015/05/27/what-is-pl-research-and-how-is-it-useful/) [[2]](http://www.pl-enthusiast.net/2019/02/04/what-is-pl-research-the-talk/). The motivation between the level 3 question is usually people wants to bring more PL ideas and techniques in their own work. This post is for that question.

The core of PL is a set of _rules_. Sometimes we call it **logic**, or 
we know it works like _logic_ but we don't say so. The other components are for making the logic run. We need to convert the system input into a format the _logic_ can accept, what is usually done by a _parser_. We need an engine to _saturate_ the logical rules and get the result.

In an interpreter, the **logic** is the operational semantics of the language. The **engine** is a recursive function `evaluate` which takes each expression and find the matching rule in the logical system to apply. A common interpreter runs until it gets the final answer (or diverge). This is the **saturation** though each expression usually just be evaluated once.

In type inference, the **logic** is the typing rules. The **engine** is an algorithm to 
compute the closure (fix-point) of type constraints on each expressions. The **saturation** means the compute is exhaustive with type informations. Static analysis is quite similar to this.

In symbolic execution, the **logic**s includes the operational semantics with constraints of the symbols and a SMT solver. What's more, since a symbolic executor need to run all the possible control-flows at one forking point e.g. an if clause. How to deal with it will also be defined in the **logic**. In a nondeterministic setting (also called dynamic symbolic execution), the **logic** doesn't need to change but the implemention need to handle the forking (or nondeterministic monad). If you need to apply state-merging, then how to merge should be defined in the **logic**.

In model checking, the **logic** is the abstract model, which can be e.g. some temporal logic in first-order model checking or HFL (higher order modal fixed point logic). You need to convert you program into this logical formula. To **saturate** it, run the model checking algorithm, or feed the formula into some solvers.


{% comment %}
<!-- Before into the core, let's think about a few related scenarios:

1. Read an arithmetic expression and compute the result.
2. Run a Python program and see the running output.
3. Compile a TypeScript program and see the compile result (a JavaScript file).
4.  -->
{% endcomment %}

{% comment %}
<!-- (We consider) many techniques belong to PL area: program analysis, symbolic execution, formal verification, etc. I have a vague idea that PL techniques usually contain three components:

1. Concrete stuff that you can see e.g. source-code, programs, logic formula.
2. Credible rules and inference. We need axioms that we believe and treat them as truth. We can collect the facts about individual stuff and then we need composition and inference to collect all the individual facts.
3. Saturation engine. No worry. I just make a fancy names to describe our code (or paper) system to apply (2) to (1). -->
{% endcomment %}


2. Abstract stuff that is extracted from the concrete stuff.

