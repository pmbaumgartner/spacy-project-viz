import srsly
from pydantic import BaseModel
from enum import Enum
import typer
import base64
from collections import defaultdict
from typing import Optional

from pathlib import Path

app = typer.Typer()


class NodeType(Enum):
    command = "command"
    io = "io"


class Node(BaseModel):
    name: str
    type: NodeType


class Edge(BaseModel):
    source: Node
    target: Node


class OutputFormat(str, Enum):
    definition = "definition"
    markdown = "markdown"
    html = "html"


node_emoji = {NodeType.command: "⏯ ", NodeType.io: "🗂 "}  # note spaces
node_brackets_left = {NodeType.command: "([", NodeType.io: "("}
node_brackets_right = {NodeType.command: "])", NodeType.io: ")"}
nbl, nbr = node_brackets_left, node_brackets_right


@app.command()
def viz(
    project_yaml: Path = typer.Argument(
        ...,
        help="Location of your spaCy project.yml file",
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
    ),
    output_format: OutputFormat = typer.Option(
        OutputFormat.definition,
        "--format",
        case_sensitive=False,
        help="Output format of the graph to stdout. "
        "You can pipe output to the correct file type,"
        " e.g. [...] --format html > diagram.html ",
    ),
    horizontal: bool = typer.Option(
        False,
        "--horizontal",
        "-h",
        help="Generate graph horizontal (left-to-right) instead of top-down.",
    ),
    workflow: Optional[str] = typer.Option(
        None,
        "--workflow",
        "-w",
        help="Generate graph only for specific workflow in project.yml file",
    ),
):
    """Generate a mermaid.js chart of commands, dependencies, and outputs
    from a spaCy project.yml file.

    Output goes to STDOUT. For the default format (definition),
    you can copy the graph definition and paste it
    at https://mermaid-js.github.io/mermaid-live-editor/

    For HTML or Markdown, you will likely want to redirect the output to a file.
    e.g.

    [command] --format html > diagram.html
    """

    # PNG in markdown can't render emoji
    if output_format != OutputFormat.markdown:
        ne = node_emoji
    else:
        ne = defaultdict(str)

    project = srsly.read_yaml(project_yaml)

    if workflow is None:
        commands = [cmd for cmd in project["commands"]]
    elif workflow not in project["workflows"]:
        typer.echo(f"ERROR: Workflow `{workflow}` not in project.yml", err=True)
        raise typer.Exit(code=1)
    else:
        workflow_cmds = project["workflows"][workflow]
        commands = [cmd for cmd in project["commands"] if cmd["name"] in workflow_cmds]

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

    orientation = "LR" if horizontal else "TD"
    graph_definition_lines = [f"graph {orientation}"]
    for node in nodes:
        n_i = nodes.index(node)
        t = node.type
        node_line = f'{n_i}{nbl[t]}"{ne[t]}{node.name}"{nbr[t]}:::{t.value}'
        graph_definition_lines.append(node_line)

    for edge in edges:
        s_i, t_i = nodes.index(edge.source), nodes.index(edge.target)
        edge_line = f"{s_i} --> {t_i}"
        graph_definition_lines.append(edge_line)

    classdef_lines = [
        "classDef command fill:#09a4d7aa,stroke:#055c79,color:#333,stroke-width:2px;;",
        "classDef io fill:#05ad80aa,stroke:#037456,color:#333,stroke-width:2px;",
    ]
    graph_definition_lines.extend(classdef_lines)

    graph_definition = "\n    ".join(graph_definition_lines)

    if output_format == OutputFormat.definition:
        print(graph_definition)
    elif output_format == OutputFormat.html:
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
        print(html_template)
    elif output_format == OutputFormat.markdown:
        graph_definition_bytes = graph_definition.encode("utf-8")
        graph_bytes_base64 = base64.urlsafe_b64encode(graph_definition_bytes).decode()
        print(
            f"![spacy project.yml diagram](https://mermaid.ink/img/{graph_bytes_base64})\n\nDefinition\n```\n{graph_definition}\n```"
        )


if __name__ == "__main__":
    app()