# Plan for "LLM Messages are a Poor Man's Programming Language"

## Current status

- [x] Initial draft with analogy examples (parse, typecheck, interpret, REPL, meta)
- [x] Table of PL operations with entity types, beliefs, compositions
- [x] Script `gen_beliefs_diagrams.py` for generating Mermaid diagrams
- [x] Generated `beliefs-diagram-full.mmd` (PL ecosystem, clean)
- [x] Generated `beliefs-diagram-full-beliefs.mmd` (PL ecosystem, with belief annotations)

## Core framing

### The primitives

|                   | PL                               | LLM                             |
| ----------------- | -------------------------------- | ------------------------------- |
| **Primitive**     | `interp: exp -> exp`             | `request: msg -> msg`           |
| **Engineering**   | PL engineering                   | Message engineering             |
| **What it means** | Everything around interpretation | Everything around request/reply |

- **PL engineering**: the ecosystem built around `interp: exp -> exp` — parsing, typechecking, compilation, REPL, meta-programming. Each tool establishes beliefs about expressions before/after interpretation.
- **Message engineering**: the ecosystem built around `request: msg -> msg` — prompt construction, output parsing, schema validation, context management, agent loops, tool use. Each tool establishes beliefs about messages before/after the request.

"Prompt engineering" is too narrow (input-side only). "LLM engineering" is already used loosely for application-level work. "Message engineering" captures that everything derives from the `msg -> msg` primitive, covering both input and output.

### The thesis

PL engineering propagates beliefs compositionally around `interp`. Message engineering tries to do the same around `request`, but lacks compositional guarantees. The post maps PL's compositional techniques onto LLM tooling to show what's there, what's missing, and what could be borrowed.

## Next steps

### 1. Solidify the PL text (now)
- Expand the "PL Essences: Compositions and Beliefs" section
- Clarify the distinction: entities are nouns, operations are verbs, beliefs are properties that propagate
- Each analogy section (parse, typecheck, interpret, REPL, meta) should build toward the key insight: beliefs accumulate
- Flesh out the "spectrum of beliefs" stub (line 63)

### 2. Polish the PL diagram (after text is solid)
- Diagram should show belief accumulation, not just the textbook pipeline
- See "Diagram design direction" below

### 3. LLM side (later)
- Once PL diagram is solid, build the LLM counterpart
- Use highlight diagrams to show per-section alignment
- Fill the "Beliefs in LLMs" section (structured output, context compression, tool use, progressive disclosure)

## Diagram design direction

Target audience: PL people who are less familiar with LLM/agents.

Key insight: PL people already know the pipeline. The diagram's job is NOT "here's the PL pipeline" but "here's how beliefs layer on top of each other through the pipeline" — which then sets up the question: does LLM tooling do the same?

### Core design

Horizontal spine with beliefs accumulating:

```
source ──[parse]──► exp ──[typecheck]──► typed exp ──[interpret]──► value
                     │                      │                         │
               well-formed            + well-typed           + semantics ok
```

The `+` is the visual punchline: beliefs accumulate. After typecheck, you still have well-formedness AND well-typedness. This compositionality is what LLM tooling largely lacks.

### Loops / side paths (for agent analogy)
- REPL: value → exp (= agent loop)
- Meta-programming: meta-term → source (= prompt engineering)

### Drop from main diagram (detail for prose)
- Small-step vs big-step (variation of interpret)
- Syntactic vs semantic typecheck (variation of typecheck)
- Compile/decompile (less central to agent analogy)
- These belong in prose as points along a "spectrum of beliefs"

### Result
~4-5 nodes, ~5 edges. Readable at a glance. Belief accumulation is the visual punchline.

## Analogy mapping (working reference)

| PL concept                | LLM concept                       | Belief (PL)                         | Belief (LLM)                | Section  |
| ------------------------- | --------------------------------- | ----------------------------------- | --------------------------- | -------- |
| Source code               | Prompt / message                  | —                                   | —                           | §1 intro |
| Expression                | Structured output                 | well-formed                         | parseable                   | §2/§3    |
| Parse                     | Output parsing                    | well-formedness                     | valid format                | §2/§3    |
| Syntactic type check      | Schema validation (JSON/Pydantic) | well-typed (static)                 | schema-conformant           | §2/§3    |
| Semantic type check       | Runtime check / re-ask            | well-typed (dynamic)                | content acceptable          | §2/§3    |
| Interpreter               | LLM inference                     | operational semantics               | ??? (no formal guarantee)   | §2/§3    |
| REPL                      | Agent loop                        | interaction correctness             | agent converges?            | §2/§3    |
| Meta-programming          | Prompt engineering                | code generation correct             | prompt produces good output | §2/§3    |
| Compile / unparse         | Context compression               | semantics preservation / round-trip | information preserved       | §3       |
| Program synthesis         | Code generation (Copilot etc.)    | meets spec                          | meets intent                | §2/§3    |
| Protocol/contract types   | Tool use format                   | interaction executable              | tool call well-formed       | §3       |
| Refinement/semantic types | Output validation                 | result acceptable                   | result useful               | §3       |

## Scratchpad triage

Every note from the post's scratchpad, tagged with destination.

### → §1 Intro

- **"poor man's and rich man's"**: LLM messages are also literally a rich man's PL — tokens cost money. Good quip for intro.
- **Program synthesis as intro hook**: the most immediately obvious PL↔LLM analogy. Use it to open: "finding a program from I/O examples is like finding a prompt from trajectories." Then: "but the analogy goes much deeper." Don't develop synthesis fully here — save the depth (abstraction levels, parametricity) for §3.

### → §2 Compositions and Beliefs in PL

- **"principle typed"** (line 59 comment): principal types relate to type inference — the spectrum of beliefs within typechecking. Syntactic type systems can have principal types (Hindley-Milner), semantic ones often can't.
- **"intensional type vs extensional type"** (line 119 comment): intensional = structure of the term, extensional = behavior. This is another axis of the belief spectrum in PL. Good for §2's spectrum discussion.
- **"type-and meta-type"** (line 168): the Hemingway quote analogy — "you can't simultaneously have youth and the feeling of youth" maps to the distinction between operating at the type level vs meta-type level. Interesting for meta-programming discussion in §2.

### → §3 Compositions and Beliefs in LLMs

- **"Any prompts can reply" vs "any program can run"** (lines 125–127): in pure lambda calculus every well-formed term can be evaluated; similarly any prompt gets a reply. But not every reply is *useful* — that's the missing belief. The LLM "type system" is trivial (everything "typechecks").
- **"protocol types vs refinement types"** quote (line 129): "We distinguish protocol (contract) types, which govern whether an interaction is executable, from refinement (semantic) types, which govern whether an execution result is acceptable." — directly maps to tool use format (protocol) vs output quality (refinement). Key quote for §3.
- **Structured output** (lines 101–104, line 137): OpenAI structured outputs, Claude agent SDK structured outputs. Concrete examples for §3.
- **Context compression** (lines 107–110): `unparse ∘ parse` invariant, serialize/deserialize round-trip. Also "de-type and re-type." For §3.
- **Tool use format** (line 112): tool calls have a schema (protocol type). Stub — needs expansion in §3.
- **Progressive disclosure** (lines 114–117): "on-demand small-step interpreter" — revealing information incrementally is like small-step semantics. 现在可以公开的情报 = "intel that can now be made public."
- **Prompting-level printing** (lines 156–165): the CLAUDE.md "call me by name" trick as a runtime assertion / canary — like `assert isinstance(x, int)`. The Van Halen brown M&M story. This is a great concrete example of a semantic belief check in LLM context.
  - > 在Reddit讨论里发现这么个小技巧
      在 CLAUDE.md 里加一条指令
      "每次回复时都叫我 【名称】
      如果 Claude 突然不叫你这个称呼。
      说明它开始忽略 CLAUDE.md 了。
      这时需要重置上下文。
      很像范海伦乐队在合同里要求"不能有棕色 M&M 豆"一样，
      看似无关细节，恰恰能检验有没有Follow指令。
      - 向阳乔木
- **REPL → Read-Eval-Print-Human Loop** (line 170): rename for agent context — the "print" goes to human, adding a human-in-the-loop belief verification step.
- **Token-usage-as-type / Money Type** (lines 172–173): token cost as a type-level constraint. Tokens are a resource type (linear type analogy?). Could be §3 or deep-dive.
- **Agent skill as package** (line 152): agent capabilities are like library packages — composable units with interfaces. §3.
- **Program synthesis → prompt synthesis** (abstraction levels): concrete (find a function for specific types ↔ find a prompt for a specific task), polymorphic (find a parametric function ↔ find a prompt that generalizes across task types, e.g. swe-bench system prompt), meta (find a program that generates programs ↔ meta-prompting). The polymorphic case connects to parametricity: learning a general rule from specific examples while being blind to specifics. The swe-bench example is concrete — finding a system prompt from expected trajectories across diverse GitHub issues.

### → §4 Conclusion

- **"extend what can be said in SE"** (lines 175–178): "first-class development", 从不可言说之物到可编程之物 (from the unspeakable to the programmable), 可编程→可类型 (programmable → typeable). This is the vision: PL techniques make LLM engineering expressible and checkable. Good for conclusion.

### → Deep-dive posts (not this post)

- **"Implementing your agent in some lines of code"** / 200 lines (lines 131–133): the "emperor has no clothes" critique of agent complexity. Separate deep-dive on agent simplicity.
- **LLM internals as PL** (lines 148–150): average as variant type, QKV as dict in average. Speculative analogies about LLM *internals* (not tooling). Different scope — maybe a separate post on "LLM internals through PL eyes."
- **Three dimensions** (lines 141–144): 离散→连续, 模糊→精确, exp-type 值和类型. Philosophical framing of how LLMs differ from PL at a fundamental level. Separate post.
- **Language embedding / prompt injection** (lines 138–139): console.log as prompt injection, "everything becomes speakable." Security/embedding angle — deep-dive.

### → Not for this series

- **Composing LLM requests as coinductive functions** (line 117): treat LLM request as a coinductive function, then two coinductive functions can compose structurally. Vague idea, not exploring soon.
- **围棋足球部** (line 181): unrelated.
- **Incremental repr / updated library** (lines 182–183): when an LLM is trained on e.g. Python 3.7 or a specific package version, and the language/API gets updated, how to provide the incremental diff so the LLM generates correct code for the new version. Separate topic about knowledge staleness and incremental updates.
- **Hemingway quote** (line 167): 一个人可能是无法同时拥有青春和对青春的感受 — evocative but tangential unless tied tightly to type/meta-type.
- token-usage-as-type? Money Type?

## Technical notes

- Diagram convention: `<div class="mermaid">...</div>` (matching 2021 post)
- Mermaid loaded via `/js/mermaid.min.js` in default layout
- Script: `gen_beliefs_diagrams.py` in this directory
- The post's key thesis: PL tools propagate beliefs compositionally; LLM tooling does the same thing but ad-hoc
