#!/usr/bin/env python3
"""Generate Mermaid diagram showing the PL concept ecosystem.

The diagram shows PL entities (source, exp, type, value) as nodes
and PL operations (parse, typecheck, interpret, ...) as labeled edges,
forming a connected pipeline. Beliefs are annotated on edges.

Output: .mmd file in _posts/2026/
"""

import os

OUTDIR = os.path.join(os.path.dirname(__file__), "..", "_posts", "2026")

# --- Entities (nodes) ---
# (id, label, shape)  shape: [] = rectangle, ([]) = rounded, {} = rhombus
ENTITIES = [
    ("src",       "Source code"),
    ("exp",       "Expression"),
    ("typed_exp", "Typed expression"),
    ("value",     "Value"),
    ("type",      "Type"),
    ("meta",      "Meta-term"),
    ("code",      "Target code"),
]

# --- Operations (edges) ---
# (from, to, operation label, belief label)
OPERATIONS = [
    ("src",       "exp",       "parse",                "well-formedness"),
    ("exp",       "typed_exp", "syntactic\ntype check", "well-typed"),
    ("exp",       "typed_exp", "semantic\ntype check",  "well-typed\n(runtime)"),
    ("typed_exp", "type",      "type\ninference",       "principal type"),
    ("typed_exp", "value",     "interpret\n(big-step)",  "operational\nsemantics"),
    ("typed_exp", "typed_exp", "interpret\n(small-step)","operational\nsemantics"),
    ("exp",       "value",     "interpret\n(untyped)",   "evaluation"),
    ("value",     "exp",       "REPL\n(loop back)",     "interaction"),
    ("meta",      "src",       "meta-eval",             "code generation"),
    ("typed_exp", "code",      "compile",               "semantics\npreservation"),
    ("code",      "exp",       "decompile\n/ unparse",  "round-trip"),
]


def gen_mermaid() -> str:
    lines = ["flowchart TD"]

    # Styles
    lines.append("    classDef entity fill:#6a9fd8,stroke:#3a6fa0,color:#fff,stroke-width:2px,font-weight:bold")
    lines.append("    classDef aux fill:#d8a06a,stroke:#a07a3a,color:#fff,stroke-width:2px,font-weight:bold")

    # Nodes
    lines.append("")
    for eid, label in ENTITIES:
        lines.append(f'    {eid}(["{label}"])')

    # Edges with operation and belief labels
    lines.append("")
    edge_count = 0
    for src, dst, op, belief in OPERATIONS:
        edge_count += 1
        lines.append(f'    {src} -->|"{op}"| {dst}')

    # Apply entity styles
    lines.append("")
    core = ["src", "exp", "typed_exp", "value"]
    aux = ["type", "meta", "code"]
    lines.append(f"    class {','.join(core)} entity")
    lines.append(f"    class {','.join(aux)} aux")

    return "\n".join(lines)


def gen_mermaid_with_beliefs() -> str:
    """Version with beliefs shown as a separate annotation layer."""
    lines = ["flowchart TD"]

    lines.append("    classDef entity fill:#6a9fd8,stroke:#3a6fa0,color:#fff,stroke-width:2px,font-weight:bold")
    lines.append("    classDef aux fill:#d8a06a,stroke:#a07a3a,color:#fff,stroke-width:2px,font-weight:bold")
    lines.append("    classDef belief fill:#f5f5f5,stroke:#999,color:#666,stroke-width:1px,font-style:italic")

    # Nodes
    lines.append("")
    for eid, label in ENTITIES:
        lines.append(f'    {eid}(["{label}"])')

    # Edges: operation label on edge, belief as a small annotation node
    lines.append("")
    for i, (src, dst, op, belief) in enumerate(OPERATIONS):
        bid = f"b{i}"
        lines.append(f'    {src} -->|"{op}"| {dst}')
        # Belief annotation linked to destination
        lines.append(f'    {bid}[/"{belief}"/] -.-o {dst}')

    # Styles
    lines.append("")
    core = ["src", "exp", "typed_exp", "value"]
    aux = ["type", "meta", "code"]
    belief_ids = [f"b{i}" for i in range(len(OPERATIONS))]
    lines.append(f"    class {','.join(core)} entity")
    lines.append(f"    class {','.join(aux)} aux")
    lines.append(f"    class {','.join(belief_ids)} belief")

    return "\n".join(lines)


def write_mmd(name: str, content: str):
    path = os.path.join(OUTDIR, f"beliefs-diagram-{name}.mmd")
    with open(path, "w") as f:
        f.write(content + "\n")
    print(f"  wrote {path}")


def main():
    os.makedirs(OUTDIR, exist_ok=True)

    # Clean up old two-column diagrams
    old_files = [
        "beliefs-diagram-compression.mmd",
        "beliefs-diagram-interpret.mmd",
        "beliefs-diagram-meta.mmd",
        "beliefs-diagram-parse.mmd",
        "beliefs-diagram-repl.mmd",
        "beliefs-diagram-typecheck.mmd",
    ]
    for f in old_files:
        p = os.path.join(OUTDIR, f)
        if os.path.exists(p):
            os.remove(p)
            print(f"  removed old {f}")

    print("Generating PL ecosystem diagram...")
    write_mmd("full", gen_mermaid())

    print("Generating PL ecosystem diagram (with beliefs)...")
    write_mmd("full-beliefs", gen_mermaid_with_beliefs())

    print(f"\nDone. Output in {OUTDIR}")


if __name__ == "__main__":
    main()
