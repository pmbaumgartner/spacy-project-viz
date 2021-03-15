from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
from collections import defaultdict
from pydantic import BaseModel
from graphviz import Digraph


class NodeType(Enum):
    command = "command"
    io = "io"
    var = "var"


class Node(BaseModel):
    name: str
    type: NodeType


class Edge(BaseModel):
    source: Node
    target: Node


def fill_html_template(graph_definition: str) -> str:
    html_template = f"""<!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="utf-8">
    </head>
    <body>
    <div class="mermaid">
        {graph_definition}
    </div>
    <div>
        <p>Definition</p>
        <pre>{graph_definition}</pre>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <script>mermaid.initialize({{startOnLoad:true}});</script>
    </body>
    </html>"""
    return html_template


def build_graph(
    project_yaml: Dict[str, Any],
    workflow: Optional[str] = None,
    variables: bool = False,
) -> Tuple[List[Node], List[Edge]]:
    if workflow is None:
        commands = [cmd for cmd in project_yaml["commands"]]
    elif workflow not in project_yaml["workflows"]:
        raise KeyError("ERROR: Workflow '{workflow}' not in project yaml.")
    else:
        workflow_cmds = project_yaml["workflows"][workflow]
        commands = [
            cmd for cmd in project_yaml["commands"] if cmd["name"] in workflow_cmds
        ]

    project_vars = list(project_yaml["vars"].keys()) if variables else []

    nodes, edges = [], []
    for command in commands:
        command_node = Node(name=command["name"], type="command")
        nodes.append(command_node)
        for dep in command.get("deps", []):
            source = Node(name=dep, type="io")
            e = Edge(
                source=source,
                target=command_node,
            )
            edges.append(e)
            if source not in nodes:
                nodes.append(source)
        for output in command.get("outputs", []):
            target = Node(name=output, type="io")
            e = Edge(
                source=command_node,
                target=target,
            )
            edges.append(e)
            if target not in nodes:
                nodes.append(target)

        for var in project_vars:
            var_node = Node(name=var, type="var")
            if var_node not in nodes:
                nodes.append(var_node)
            if f"vars.{var}" in " ".join(command["script"]):
                e = Edge(
                    source=var_node,
                    target=command_node,
                )
                edges.append(e)

    return nodes, edges


NODE_EMOJI = {
    NodeType.command: "⏯ ",
    NodeType.io: "🗂 ",
    NodeType.var: "⭐ ",
}  # note spaces
NODE_BRACKETS_LEFT = {NodeType.command: "([", NodeType.io: "(", NodeType.var: "{{"}
NODE_BRACKETS_RIGHT = {NodeType.command: "])", NodeType.io: ")", NodeType.var: "}}"}
NBL, NBR = NODE_BRACKETS_LEFT, NODE_BRACKETS_RIGHT


def create_mermaid_definition(
    nodes: List[Node],
    edges: List[Edge],
    horizontal: bool = False,
    use_emoji: bool = True,
) -> str:
    NE = NODE_EMOJI if use_emoji else defaultdict(str)
    orientation = "LR" if horizontal else "TD"
    graph_definition_lines = [f"graph {orientation}"]
    for node in nodes:
        n_i = nodes.index(node)
        t = node.type
        node_line = f'{n_i}{NBL[t]}"{NE[t]}{node.name}"{NBR[t]}:::{t.value}'
        graph_definition_lines.append(node_line)

    for edge in edges:
        s_i, t_i = nodes.index(edge.source), nodes.index(edge.target)
        edge_line = f"{s_i} --> {t_i}"
        graph_definition_lines.append(edge_line)

    classdef_lines = [
        "classDef command fill:#09a4d7aa,stroke:#055c79,color:#333,stroke-width:2px;;",
        "classDef io fill:#05ad80aa,stroke:#037456,color:#333,stroke-width:2px;",
        "classDef var fill:#6642d1aa,stroke:#5638ab,color:#333,stroke-width:2px;",
    ]
    graph_definition_lines.extend(classdef_lines)

    graph_definition = "\n    ".join(graph_definition_lines)

    return graph_definition


GRAPHVIZ_NODE_SHAPES = {
    NodeType.command: "ellipse",
    NodeType.io: "box",
    NodeType.var: "hexagon",
}  # note spaces

GRAPHVIZ_NODE_FILL = {
    NodeType.command: "#09a4d7aa",
    NodeType.io: "#05ad80aa",
    NodeType.var: "#6642d1aa",
}

GRAPHVIZ_NODE_BORDER = {
    NodeType.command: "#055c79",
    NodeType.io: "#037456",
    NodeType.var: "#5638ab",
}

GRAPHVIZ_MARGIN_MULTIPLIER = 1.5
M = GRAPHVIZ_MARGIN_MULTIPLIER


def create_graphviz_digraph(
    nodes: List[Node],
    edges: List[Edge],
    horizontal: bool = False,
    use_emoji: bool = True,
) -> Digraph:
    orientation = "LR" if horizontal else "TD"
    NE = NODE_EMOJI if use_emoji else defaultdict(str)
    g = Digraph(comment="spaCy project.yml diagram")
    g.attr(rankdir=orientation)
    g.attr(
        "node",
        style="filled",
        fontname="Trebuchet MS",
        margin=f"{0.11*M:.3f},{0.055*M:.3f}",  # multiplier of defaults
    )
    g.attr("edge", color="#333333")
    for i, node in enumerate(nodes):
        t = node.type
        g.attr(
            "node",
            shape=GRAPHVIZ_NODE_SHAPES[t],
            fillcolor=GRAPHVIZ_NODE_FILL[t],
            color=GRAPHVIZ_NODE_BORDER[t],
        )
        g.node(str(i), NE[t] + node.name)
    for edge in edges:
        s_i, t_i = nodes.index(edge.source), nodes.index(edge.target)
        g.edge(str(s_i), str(t_i))

    return g