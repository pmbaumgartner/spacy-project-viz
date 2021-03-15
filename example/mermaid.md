![spaCy project.yml diagram](https://mermaid.ink/img/Z3JhcGggVEQKICAgIDAoWyJkb3dubG9hZCJdKTo6OmNvbW1hbmQKICAgIDEoWyJjb252ZXJ0Il0pOjo6Y29tbWFuZAogICAgMigiYXNzZXRzLyR7dmFycy50cmFpbn0iKTo6OmlvCiAgICAzKCJhc3NldHMvJHt2YXJzLmRldn0iKTo6OmlvCiAgICA0KCJzY3JpcHRzL2NvbnZlcnQucHkiKTo6OmlvCiAgICA1KCJjb3JwdXMvdHJhaW4uc3BhY3kiKTo6OmlvCiAgICA2KCJjb3JwdXMvZGV2LnNwYWN5Iik6OjppbwogICAgNyhbImNyZWF0ZS1jb25maWciXSk6Ojpjb21tYW5kCiAgICA4KCJzY3JpcHRzL2NyZWF0ZV9jb25maWcucHkiKTo6OmlvCiAgICA5KCJjb25maWdzL2NvbmZpZy5jZmciKTo6OmlvCiAgICAxMChbInRyYWluIl0pOjo6Y29tbWFuZAogICAgMTEoInRyYWluaW5nL21vZGVsLWJlc3QiKTo6OmlvCiAgICAxMihbImV2YWx1YXRlIl0pOjo6Y29tbWFuZAogICAgMTMoInRyYWluaW5nL21ldHJpY3MuanNvbiIpOjo6aW8KICAgIDE0KFsicGFja2FnZSJdKTo6OmNvbW1hbmQKICAgIDE1KFsidmlzdWFsaXplLW1vZGVsIl0pOjo6Y29tbWFuZAogICAgMTYoInNjcmlwdHMvdmlzdWFsaXplX21vZGVsLnB5Iik6OjppbwogICAgMiAtLT4gMQogICAgMyAtLT4gMQogICAgNCAtLT4gMQogICAgMSAtLT4gNQogICAgMSAtLT4gNgogICAgOCAtLT4gNwogICAgNyAtLT4gOQogICAgOSAtLT4gMTAKICAgIDUgLS0-IDEwCiAgICA2IC0tPiAxMAogICAgMTAgLS0-IDExCiAgICA2IC0tPiAxMgogICAgMTEgLS0-IDEyCiAgICAxMiAtLT4gMTMKICAgIDExIC0tPiAxNAogICAgMTYgLS0-IDE1CiAgICAxMSAtLT4gMTUKICAgIGNsYXNzRGVmIGNvbW1hbmQgZmlsbDojMDlhNGQ3YWEsc3Ryb2tlOiMwNTVjNzksY29sb3I6IzMzMyxzdHJva2Utd2lkdGg6MnB4OzsKICAgIGNsYXNzRGVmIGlvIGZpbGw6IzA1YWQ4MGFhLHN0cm9rZTojMDM3NDU2LGNvbG9yOiMzMzMsc3Ryb2tlLXdpZHRoOjJweDsKICAgIGNsYXNzRGVmIHZhciBmaWxsOiM2NjQyZDFhYSxzdHJva2U6IzU2MzhhYixjb2xvcjojMzMzLHN0cm9rZS13aWR0aDoycHg7)

Definition
```
graph TD
    0(["download"]):::command
    1(["convert"]):::command
    2("assets/${vars.train}"):::io
    3("assets/${vars.dev}"):::io
    4("scripts/convert.py"):::io
    5("corpus/train.spacy"):::io
    6("corpus/dev.spacy"):::io
    7(["create-config"]):::command
    8("scripts/create_config.py"):::io
    9("configs/config.cfg"):::io
    10(["train"]):::command
    11("training/model-best"):::io
    12(["evaluate"]):::command
    13("training/metrics.json"):::io
    14(["package"]):::command
    15(["visualize-model"]):::command
    16("scripts/visualize_model.py"):::io
    2 --> 1
    3 --> 1
    4 --> 1
    1 --> 5
    1 --> 6
    8 --> 7
    7 --> 9
    9 --> 10
    5 --> 10
    6 --> 10
    10 --> 11
    6 --> 12
    11 --> 12
    12 --> 13
    11 --> 14
    16 --> 15
    11 --> 15
    classDef command fill:#09a4d7aa,stroke:#055c79,color:#333,stroke-width:2px;;
    classDef io fill:#05ad80aa,stroke:#037456,color:#333,stroke-width:2px;
    classDef var fill:#6642d1aa,stroke:#5638ab,color:#333,stroke-width:2px;
```
