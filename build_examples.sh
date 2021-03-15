#!/bin/bash

spacy-project-viz example/project.yml -f mermaid-html -h > example/mermaid.html
spacy-project-viz example/project.yml -f mermaid-markdown > example/mermaid.md
spacy-project-viz example/project.yml --vars -f graphviz-svg > example/graphviz.svg

