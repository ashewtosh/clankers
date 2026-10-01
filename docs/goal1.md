agent-runtime/
│
├── core/
│   ├── agent.py
│   ├── state.py
│   ├── message.py
│   ├── action.py
│   └── execution.py
│
├── llm/
│   ├── client.py
│   ├── protocol.py
│   └── streaming.py
│
├── agents/
│   ├── builder.py
│   ├── registry.py
│   └── delegation.py
│
├── workflow/
│   ├── graph.py
│   ├── node.py
│   ├── edge.py
│   └── executor.py
│
├── tools/
│   ├── registry.py
│   ├── schema.py
│   └── executor.py
│
├── memory/
│   ├── short_term.py
│   ├── long_term.py
│   ├── checkpoint.py
│   └── vector.py
│
├── rag/
│   ├── ingestion.py
│   ├── chunking.py
│   ├── embedding.py
│   ├── retrieval.py
│   └── reranking.py
│
├── communication/
│   ├── messages.py
│   ├── a2a.py
│   └── mcp.py
│
├── human/
│   ├── approval.py
│   └── interrupt.py
│
├── api/
│   └── server.py
│
└── experiments/
    ├── ...