from jinja2 import Template
from pathlib import Path

# Fixed Mermaid header (structure + classDefs)
mermaid_header = """%% Mermaid diagram generator for resolution steps
%% This version represents the diagram plus highlight states for resolution logic

%%{ init: {
  'themeVariables': {
    'edgeLabelBackground': 'transparent',
    "fontSize": "20px",
    "fontFamily": "monospace",
    'textAlign': 'center',
    'wrap': true
    }
} }%%
flowchart LR
  subgraph FOO [foo]
    direction TB
    foo20[ ]:::invisible
    foo11[\"foo 1.1\"]
    foo10[\"foo 1.0\"]
  end

  subgraph STD [std]
    direction TB
    std20[\"std 2.0\"]
    std11[\"std 1.1\"]
    std10[\"std 1.0\"]
  end

  subgraph BAR [bar]
    direction TB
    bar20[\"bar 2.0\"]
    bar11[ ]:::invisible
    bar10[\"bar 1.0\"]
  end

  FOO ~~~ STD
  STD ~~~ BAR
  foo10 ~~~ std10 ~~~ bar10
  %% foo11 ~~~ std11 ~~~ bar11
  %% foo20 ~~~ std20 ~~~ bar20
  foo10 -->|dep| std10
  foo11 -.->|either| std10
  foo11 -.->|either| std11
  bar10 -->|dep| std10
  bar20 -->|dep| std20

  linkStyle default stroke:#222, color:#000, background:#fff

  %% Base category styles
  classDef foo fill:#e0f8e0, stroke:#ccc, stroke-width:2px, color:#000;
  classDef std fill:#e0eaff, stroke:#ccc, stroke-width:2px, color:#000;
  classDef bar fill:#ffe0e0, stroke:#ccc, stroke-width:2px, color:#000;

  %% Role-based overlays
  classDef selectedLocal stroke:#0077cc, stroke-width:4px, stroke-width:4px;
  classDef selectedInstall stroke:#f90, stroke-width:4px;

  %% Inactive nodes
  classDef faded fill:#f5f5f5, stroke:#ccc, color:#aaa;

  %% Subgraph hint for to-install selection
  classDef subgraphStyle fill:#fff, stroke:#0af, stroke-width:2px, color:#000
  classDef invisible fill:transparent, stroke:none, color:transparent
  classDef selectedGroup fill:#fff2cc, stroke:#f90, stroke-width:4px, stroke-dasharray: 6 3;

  %% Assign base categories (default for all nodes)
  class foo10,foo11 foo
  class std10,std11,std20 std
  class bar10,bar20 bar
"""

# Define node groups
base_classes = {
    'foo': ['foo10', 'foo11'],
    'std': ['std10', 'std11', 'std20'],
    'bar': ['bar10',          'bar20']
}

all_subgraphs = ['FOO', 'STD', 'BAR']

# Template for class assignment block
mermaid_state_template = Template("""
  %% State: {{ label }}
{% for node in all_nodes %}
  class {{ node }}{% if node in local %} selectedLocal{% elif node in install %} selectedInstall{% else %} faded{% endif %}
{% endfor %}
{% for sub in all_subgraphs %}
  class {{ sub }} {% if sub|lower in to_install_groups %}selectedGroup{% else %}subgraphStyle{% endif %}
{% endfor %}
""")

# Function to generate two diagrams: initial and final

def save_resolution_step_pair(initial_local, to_install_groups, final_install, label_start, label_end, action_name):
    all_nodes = sum(base_classes.values(), [])

    state1 = mermaid_state_template.render(
        all_nodes=all_nodes,
        local=initial_local,
        install=[],
        to_install_groups=to_install_groups,
        label=label_start,
        all_subgraphs=all_subgraphs
    )
    path1 = Path("assets") / f"resolve_{action_name}_pre.mmd"
    path1.parent.mkdir(parents=True, exist_ok=True)
    path1.write_text(mermaid_header + "\n" + state1)

    state2 = mermaid_state_template.render(
        all_nodes=all_nodes,
        local=initial_local,
        install=final_install,
        to_install_groups=[],
        label=label_end,
        all_subgraphs=all_subgraphs
    )
    path2 = Path("assets") / f"resolve_{action_name}_post.mmd"
    path2.write_text(mermaid_header + "\n" + state2)

    print(f"Saved: {path1}")
    print(f"Saved: {path2}")

# Legend generator

def save_legend():
    legend = """%%{ init: { 'theme': 'default' } }%%
flowchart TB
    subgraph Legend_Node_Styles
        A1["selectedLocal"]:::selectedLocal
        A2["selectedInstall"]:::selectedInstall
        A3["faded"]:::faded
    end

    subgraph Legend_Subgraph_Style
        G1["selectedGroup"]:::selectedGroup
    end

    classDef selectedLocal stroke:#000, stroke-width:4px;
    classDef selectedInstall stroke:#0077cc, stroke-width:4px;
    classDef faded fill:#f5f5f5, stroke:#ccc, color:#aaa;
    classDef selectedGroup fill:#fff2cc, stroke:#f90, stroke-width:4px, stroke-dasharray: 6 3;
"""
    Path("assets").mkdir(exist_ok=True)
    Path("assets/legend.mmd").write_text(legend)
    print("Saved: assets/legend.mmd")

def save_all_resolution_steps():
    steps = [
        {
            "action_name": "upgrade_foo_from_std11",
            "initial_local": ["std11"],
            "to_install_groups": ["foo"],
            "final_install": ["std11", "foo11"],
            "label_start": "Initial: std1.1 installed, selecting foo",
            "label_end": "Final: std1.1, foo1.1 installed"
        },
        {
            "action_name": "allow_downgrade_foo_bar",
            "initial_local": ["std11"],
            "to_install_groups": ["foo", "bar"],
            "final_install": ["std10", "foo11", "bar10"],
            "label_start": "Initial: std1.1 installed, selecting foo & bar",
            "label_end": "Final: std1.0, foo1.1, bar1.0 installed"
        },
        {
            "action_name": "upgrade_foo_from_std10",
            "initial_local": ["std10"],
            "to_install_groups": ["foo"],
            "final_install": ["std11", "foo11"],
            "label_start": "Initial: std1.0 installed, selecting foo",
            "label_end": "Final: std1.1, foo1.1 installed"
        },
        {
            "action_name": "least_change_foo",
            "initial_local": ["std10"],
            "to_install_groups": ["foo"],
            "final_install": ["std10", "foo11"],
            "label_start": "Initial: std1.0 installed, selecting foo",
            "label_end": "Final: std1.0, foo1.1 installed"
        },
        {
            "action_name": "upgrade_least_foo_bar_std10",
            "initial_local": ["std10"],
            "to_install_groups": ["foo", "bar"],
            "final_install": ["std10", "foo11", "bar10"],
            "label_start": "Initial: std1.0 installed, selecting foo & bar",
            "label_end": "Final: std1.0, foo1.1, bar1.0 installed"
        },
        {
            "action_name": "downgrade_from_r1",
            "initial_local": ["std11", "foo11"],
            "to_install_groups": ["bar"],
            "final_install": ["std10", "foo11", "bar10"],
            "label_start": "Initial: std1.1, foo1.1 installed, selecting bar",
            "label_end": "Final: std1.0, foo1.1, bar1.0 installed"
        }
    ]
    for step in steps:
        save_resolution_step_pair(**step)

# Run batch
save_all_resolution_steps()