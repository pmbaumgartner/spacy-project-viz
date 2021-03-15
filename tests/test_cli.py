from typer.testing import CliRunner
import pytest
from spacy_project_viz.cli import app

runner = CliRunner()


def test_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0


def test_mermaid_definition():
    result = runner.invoke(app, ["tests/project.yml", "--format", "mermaid-definition"])
    assert result.exit_code == 0
    assert "graph" in result.stdout
    assert "-->" in result.stdout


def test_mermaid_markdown():
    result = runner.invoke(app, ["tests/project.yml", "--format", "mermaid-markdown"])
    assert result.exit_code == 0
    assert "https://mermaid.ink/img/" in result.stdout
    assert "Definition" in result.stdout
    assert "graph" in result.stdout
    assert "-->" in result.stdout


def test_mermaid_html():
    result = runner.invoke(app, ["tests/project.yml", "--format", "mermaid-html"])
    assert result.exit_code == 0
    assert '<div class="mermaid">' in result.stdout
    assert "mermaid.initialize" in result.stdout
    assert "mermaid.min.js" in result.stdout
    assert "graph" in result.stdout
    assert "-->" in result.stdout


def test_graphviz_definition():
    result = runner.invoke(
        app, ["tests/project.yml", "--format", "graphviz-definition"]
    )
    assert result.exit_code == 0
    assert "digraph" in result.stdout
    assert "node" in result.stdout
    assert "edge" in result.stdout
    assert "rankdir" in result.stdout
    assert "->" in result.stdout


def test_graphviz_url():
    result = runner.invoke(app, ["tests/project.yml", "--format", "graphviz-url"])
    assert result.exit_code == 0
    assert "https://dreampuf.github.io/GraphvizOnline/" in result.stdout


def test_graphviz_svg():
    result = runner.invoke(app, ["tests/project.yml", "--format", "graphviz-svg"])
    assert result.exit_code == 0
    assert "svg" in result.stdout