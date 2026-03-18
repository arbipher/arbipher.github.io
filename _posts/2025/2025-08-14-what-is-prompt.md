---
layout: post
title: What is Prompt?
comments: true
published: false
category:
- english
- programming-languages
---

## What is a Prompt

We are going to discuss one question, what is a prompt. We are going to explore the answer from the perspective of programming languages (PL), i.e., types, composition, and etc.

Let's start with some observations. Obviously, we can have:

```prompt
- How are you?
- I'm BLA~BLA~, an AI developed by BLA~BLA~.
```

```ocaml
type prompt = string
type reply = string

type llm_round = prompt -> reply
```

The dialogue with current LLMs are achieved by concatenating chat history. The stateful multiple round dialogue can merely be a stateless single round.

```prompt
- How are you?
- I'm BLA~BLA~, an AI developed by BLA~BLA~.

- What's your model?
- I'm based on the BLA~model architecture.
```

It's equivalent to the following:

```prompt
- [("How are you?", "I'm BLA~BLA~, an AI developed by BLA~BLA~.")], What's your model?
- I'm based on the BLA~model architecture.
```

Since both the prompt and reply are strings, for simplicity we give them a uniform type `utterance`. The type of this approach is:

```ocaml
type utterance = string
type prompt = utterance
type reply = utterance
type history = (prompt * reply) list
type llm_dialogue = history * prompt -> reply
```

LLM API may process the reply into a more structured form, or user may _parse_ the reply to get a specific `syntax`. This operation is expressed in the prompt, where it contains `instruct` for that. For example:

````prompt
(* prompt *)
Please generate a python function to compute the sum of two integers and return an integer `sum(a, b)`. Put the function in a markdown python code block.

(* reply *)
```python
def sum(a: int, b: int) -> int:
    return a + b
```

````

Now we have some requirements and expectations on the prompt and reply. The prompt contains an `instruct` to describe the expected `syntax` of the reply. The reply is expected to be a structured output, e.g., having a code block in markdown format, or totally be a JSON. In this example, the user can parse the reply to get the code string. We vaguely define the utterance conveys some meaning, and we can have:

```ocaml
type 'meaning utterance = string
type 'm prompt = 'm utterance
type 'm reply = 'm utterance

type ('instruct, 'syntax) llm_round = 'instruct prompt -> 'syntax reply
type 'syntax parse_reply = 'syntax reply -> 'syntax
```

We can refine the type further. Note we just use the OCaml syntax for illustration, and the type refinement and refinement check are beyond its static type checking capability.

We know the instruct is to describe a syntax, so we can have:

```ocaml
type 'syntax instruct = string
type 'syntax llm_round = ('syntax instruct) prompt -> 'syntax reply
type 'syntax parse_reply = 'syntax reply -> 'syntax
```

In practice, we often let the LLM simply the prompt, e.g., in this case, we can first ask the LLM to (spellcheck or) simplify the prompt but keep the same instruct result.

````prompt
(* prompt 1 *)
Simplify the below prompt but keep the same instruct result. Only reply the simplyfied prompt.
Please generate a python function to compute the sum of two integers and return an integer `sum(a, b)`. Put the function in a markdown python code block.

(* reply 1 *)
Generate a Python function `sum(a, b)` that returns the sum of two integers in a markdown Python code block.

(* prompt 2, the same as reply 1 *)
Generate a Python function `sum(a, b)` that returns the sum of two integers in a markdown Python code block.

(* reply 2 *)
```python
def sum(a, b):
    return a + b
```
````

The round 1 is used to simplfy the prompt to instruct the code, while the round 2 performs the actual code instruction. From the type perspective, we can have:

```ocaml
type 'syntax llm_round_1 = (('syntax instruct) instruct) prompt -> ('syntax instruct) reply
type 'syntax llm_round_2 = ('syntax instruct) prompt -> 'syntax reply
type 'syntax parse_reply = 'syntax reply -> 'syntax
```

We can natually see the pattern of type if we need to step-wise refine the prompt, the type will be `'syntax instruct instruct ... instruct`. 

Besides **typing**, we have another two aspects to see these steps. One is **meta-programming** (or _staged computation_). If we treat LLM as an interpreter taking the prompt and returing the reply, the refinement of a prompt is natually like meta-programming. Each llm round to refine the prompt is a stage to run the program with meta expressions. The other PL aspect is **language embedding** (_shallow embedding_). We embed our intention into the prompt and parse the intention result from the reply.

(another question is when can we have compositional property like `llm_interp e1 -> v1` and `llm_interp e2 -> v2`, then how to can expect from `llm_interp (e1; e2) -> v1; v2`?)

In common programming languages, concrete syntax are handled in the beginning while only information in abstract syntax e.g. AST or IR are precicely processed. With LLM, only conrete syntax are handled apparently. It's a very interesting question to explore, when asking `"What is the result of one plus one?"`, whether the abstract form `Plus(Int 1, Int 1)` is handled in some form internally to get `Int 2`.

The reason we are using the PL way is to seek a way to check and test the prompt. 


**Meta-circular evaluator**(https://en.wikipedia.org/wiki/Meta-circular_evaluator)

## How to Process a Language

