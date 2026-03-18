---
layout: post
title: LLM Messages are a Poor Man’s Programming Language
comments: true
published: false
category:
- english
- programming-languages
- ai
---

# Outline
<!-- claude can edit this section -->

**This post** (manifesto): the whole picture and key examples

1. **Intro** — thesis: LLM messages are a poor man's PL. Hook with program synthesis as the most obvious analogy (finding a program from I/O examples ↔ finding a prompt from trajectories), then: "but the analogy goes deeper." Why PL people should care.
2. **Compositions and Beliefs in PL** — the PL side. Entities, operations, beliefs. The pipeline, the diagram, belief accumulation. Spectrum of beliefs (syntactic/semantic, static/dynamic) as variations within each phase. PL-only, no LLM here.
3. **Compositions and Beliefs in LLMs** — the LLM side, same perspective. Structured output, context compression, tool use, progressive disclosure. Program synthesis revisited in depth here (concrete/polymorphic/meta levels, parametricity). What maps, what's missing (compositionality).
4. **Conclusion** — what PL techniques could improve LLM tooling.

**Deep-dive posts** (separate, linked from here):
- e.g. structured output as type checking
- e.g. context compression and the round-trip invariant
- e.g. agent loops as REPL

Related:
- [A Spectrum of Type Soundness and Performance](https://prl.khoury.northeastern.edu/blog/2018/10/06/a-spectrum-of-type-soundness-and-performance/)
- https://zhuanlan.zhihu.com/p/2004251702040208924
  - [AI Agent 背后的函数式渊源](https://x.com/guyingjie129/status/2012901366189179050)
- https://agent-calculus-demo.vercel.app/
- https://writings.stephenwolfram.com/2026/01/what-is-ruliology/

# Intro

LLMs and the related tools have been widely used recently. I often encounter similiar terms and concepts, which have different meanings in AI and programming languages (PL). I am using LLM tools, agents, and programming API. I see many scenarios and use cases on **compositions** and **beliefs** on _prompts_, where PL performs them on code, expression, or types. I find it interesting and helpful to make some analogy, and explore more connections that originated from the PL perspective. My motivation is to identify where the beliefs comes from, and try to minic PL techniques to compose and propagate beliefs in LLMs.

By messages I mean the full conversation protocol: user prompts, assistant replies, tool calls, system instructions — the whole structured exchange that LLM APIs operate on.

<!-- internal, external ; syntax, sementics; static, dynamic -->

**engineering for interp/llm_request**
<!-- tying the loop: step vs full -->


# Exmamples of Analogy

Here are some exmamples:

**Parse**:

In PL, we have _source code_ and the parsed _expression_.
In LLM, we have _prompt_ and in many cases it must be safely parsed to get userful information.

**Type checking**:

In PL, we have _type system_ to check the types of expressions. The _syntactic type system_ checks the types based on the syntax of expressions. The static type can be explicitly declared or inferred, as in C++ or OCaml. Python or TypeScript have some syntactic type hints, but they are not strictly checked. They can have statements like `assert isinstance(x, int)` to check the type at runtime. I would say them as _semantic type checking_ (though you may also find terms dynamic typing or gradual typing).
In LLM, people expect the reply is or have certain types e.g. JSON or pydantic model.

<!-- principle typed -->

**Interpreting**:

In PL, we have _interpreter_ to evaluate expressions. We don't use the term _interpretability_ since an interpreter is something concrete that should respect the semantics of the language. A langauge can have operational semantics which describes how to evaluate expressions step by step (small-step or big-step). An interpreter should follow the operational semantics, while a compiler translates the expressions in this language to another language (e.g., bytecode or machine code) and still observe the semantics in some sense. PL also have denotational semantics which maps expressions to mathematical objects.
LLM behaves like an interpreter that takes a prompt and returns a reply.

**REPL/Agent**:

In PL, we have _REPL_ (read-eval-print loop) to interactively read expressions, evaluate them, and print the results. The example is what you can get after running `python` command in terminal. _REPL_ is a helper tool build upon the interpreter.
In LLM, we have _agents_ to interactively read prompts, invoke LLM to evaluate them, and print the replies. An agent is a helper tool build upon LLM.

**Meta-programming**:

In PL, an interpreter evaluates expressions in a language. Meta-programming is to write terms out of a language to generate the expressions in the language. The terms of meta-programming are not in the original language, but if that language is _large_ enough, those terms can also be expressed in the language itself. For example, for a language cantining only digits e.g. `0` or `42`, you can make a meta term as `repeat(6, 10)` to generate a long digit with 10 sixes `6666666666`, or a mete term as `repeat(6, 100)`.

**program synthesis**:

# PL Essences: Compositions and Beliefs

We try to propose two PL essences before going into more details:
- **Compositions**: Make compound things from simple ones.
- **Beliefs**: Propagate beliefs from small to large.

I pick the non-formal words on purpose, like things and beliefs intead of formal or concrete terms like wellformness, typecheck, invariant, truth, terminating, soundness, etc. We would use the approach that describe the PL tools and techniques in types: not the usually types in a language, for types for their entities. In this perspective, the above exmamples can be described as:

| Tool operation        | Entity Type            | Belief                             | Composition                     |
| --------------------- | ---------------------- | ---------------------------------- | ------------------------------- |
| parse                 | `source -> exp`        | well-formness of `exp`             | structure of `exp`              |
| syntical type check   | `exp -> type option`   | well-typed of `type`               | typing rules of `exp`           |
| semantical type check | `exp -> type option`   | well-typed of `type`               | models of `exp` (runtime check) |
| interpret small-step  | `exp -> exp`           | operational semantics (small-step) | structure of `exp`              |
| interpret big-step    | `exp -> exp`           | operational semantics (big-step)   | structure of `exp`              |
| repl                  | `exp Io.t -> exp Io.t` | interpration of one `exp`          | structure of `exp`              |
| meta-eval             | `meta_term -> exp`     | belief of `exp`                    | structure of `exp`              |

Many PL areas have a spectrum of beliefs

# Beliefs in LLMs

In web chat app, users can eyeball and verify the reply from LLM, only if one is familiar with the topic. We are more interested in programmatic use of LLMs including agents, where the beliefs must be propagated and verified automatically.

**Structured output**
We can ask LLM to specify the format for the whole output or the content inside, for example, a JSON object or a piece of Python code. Framework or the users can reject or re-ask the LLM if the output is not well-formed. This is similar to syntactical type checking in PL.

- https://platform.claude.com/docs/en/agent-sdk/structured-outputs
- https://platform.openai.com/docs/guides/structured-outputs?api-mode=chat&example=chain-of-thought

**Context Compression**
context compression coresponds to the `unparse parse` invariant in PL (or serialize deserialize). Another analyze is de-type and re-type: compile the typed expression to untyped code, and then re-type check it.

see : https://factory.ai/news/evaluating-compression

<!-- to categorize -->

【演绎核】与【概率壳】：AI Agent 工程架构优化(https://zhuanlan.zhihu.com/p/2004499338219496104)
- https://zhuanlan.zhihu.com/p/2004502163422994849