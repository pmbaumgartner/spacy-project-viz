import base64
import urllib.parse
from enum import Enum
from pathlib import Path
from typing import Optional

import srsly
import typer

from spacy_project_viz.utils import (
    build_graph,
    create_graphviz_digraph,
    create_mermaid_definition,
    fill_html_template,
)

app = typer.Typer()


class OutputFormat(str, Enum):
    mermaid_definition = "mermaid-definition"
    mermaid_markdown = "mermaid-markdown"
    mermaid_html = "mermaid-html"
    graphviz_definition = "graphviz-definition"
    graphviz_url = "graphviz-url"
    graphviz_svg = "graphviz-svg"


Fmt = OutputFormat


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
    output_format: Fmt = typer.Option(
        Fmt.mermaid_definition,
        "--format",
        "-f",
        case_sensitive=False,
        help="Output format of the graph to stdout. "
        "You can pipe output to the correct file type,"
        " e.g. [...] --format mermaid-html > diagram.html ",
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
    variables: bool = typer.Option(
        False,
        "--vars/--no-vars",
        help="Include variables if mentioned in a command script. "
        "Warning: Can make diagram complex.",
    ),
):
    """Generate a mermaid.js or graphviz chart of commands, dependencies, outputs,
    and optionally variables from a spaCy project.yml file.

    Output goes to STDOUT.

    For the default format (mermaid-definition),
    you can copy the graph definition and paste it
    at https://mermaid-js.github.io/mermaid-live-editor/

    For the graphviz-definition, you can copy the graph
    definition and paste it at
    https://dreampuf.github.io/GraphvizOnline/, or use
    the graphviz-url format.

    For mermaid-markdown, mermaid-html, and graphviz-svg,
    you will likely want to redirect the output to a file.
    e.g.

      spacy-project-viz project.yml --format mermaid-html > diagram.html
    """

    project = srsly.read_yaml(project_yaml)

    nodes, edges = build_graph(project, workflow, variables)
    # PNG doesn't render emoji
    use_emoji = output_format not in {
        Fmt.mermaid_markdown,
    }

    if output_format.startswith("mermaid"):
        graph_definition = create_mermaid_definition(
            nodes, edges, horizontal, use_emoji
        )
        if output_format == Fmt.mermaid_definition:
            print(graph_definition)
        elif output_format == Fmt.mermaid_html:
            html_template = fill_html_template(graph_definition)
            print(html_template)
        elif output_format == Fmt.mermaid_markdown:
            graph_definition_bytes = graph_definition.encode("utf-8")
            graph_bytes_base64 = base64.urlsafe_b64encode(
                graph_definition_bytes
            ).decode()
            print(
                f"![spaCy project.yml diagram](https://mermaid.ink/img/{graph_bytes_base64})\n\nDefinition\n```\n{graph_definition}\n```"
            )
    elif output_format.startswith("graphviz"):
        graphviz_graph = create_graphviz_digraph(nodes, edges, horizontal, use_emoji)
        if output_format == Fmt.graphviz_definition:
            print(graphviz_graph.source)
        elif output_format == Fmt.graphviz_url:
            quoted_graph_source = urllib.parse.quote(graphviz_graph.source, safe="")
            print(f"https://dreampuf.github.io/GraphvizOnline/#{quoted_graph_source}")
        elif output_format == Fmt.graphviz_svg:
            graph_svg_bytes = graphviz_graph.pipe("svg").decode()
            print(graph_svg_bytes)


def main():
    app()
