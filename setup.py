from setuptools import find_packages, setup

setup(
    name="spacy-project-viz",
    version="0.0.1",
    description="CLI Tool to help generate a mermaid.js or graphviz chart of "
    "commands, dependencies, outputs, and optionally variables from a spaCy project.yml file.",
    url="https://github.com/pmbaumgartner/spacy-project-viz",
    author="Peter Baumgartner",
    packages=find_packages(),
    python_requires=">=3.6, <4",
    install_requires=["spacy>=3.0.0", "srsly>=2.4.0", "typer>=0.3.2"],
    extras_require={
        "test": ["pytest", "pytest-cov"],
        "graphviz": ["graphviz>=0.16"],
        "all": ["pytest", "pytest-cov", "graphviz>=0.16"],
    },
    entry_points={
        "console_scripts": [
            "spacy-project-viz=spacy_project_viz.cli:main",
        ],
    },
)
