# text-to-sql-agent

An agent that answers questions about a relational database in plain language: it finds the
relevant tables, writes the SQL, runs it, fixes its own errors, and returns a sourced answer.

> **Status: in progress.** This repository is built step by step; the roadmap below shows what
> is done and what is next. Every step is measured on the same evaluation set.

## Why this project

Writing SQL against a large, unfamiliar schema is slow, and most people who need the data
cannot write SQL at all. Two engineering teams have published how they tackled this in
production:

- **Uber — QueryGPT.** A first version based on simple retrieval and few-shot prompting
  retrieved irrelevant schemas, and accuracy dropped as tables were added. The production
  version splits the work across specialised steps: an intent step that maps the question to a
  business domain, a table-selection step the user can correct, and column pruning to keep
  large schemas within the context window. Intent, table selection and SQL quality are
  evaluated separately.
- **Pinterest — Text-to-SQL.** Table summaries and past-query summaries are indexed in a vector
  store; retrieval returns candidate tables, then an LLM keeps the most relevant ones before
  generating SQL.

This project reproduces these ideas on a public dataset, one layer at a time, and measures what
each layer actually brings.

## Planned architecture

```
question
   │
   ▼
1. schema retrieval      ── vector search over table / column descriptions
   │
   ▼
2. table selection       ── LLM keeps the K relevant tables out of the N retrieved
   │
   ▼
3. SQL generation        ── structured output, read-only SQL only
   │
   ▼
4. execution + repair    ── run on PostgreSQL; on error, feed the error back and retry
   │
   ▼
answer + SQL + rows used
```

## Evaluation

Correctness of generated SQL is checked by **executing it** and comparing the result with a
reference query — an objective signal, unlike most LLM tasks.

Metrics, reported for every step of the roadmap:

- execution accuracy (same result as the reference query),
- table-selection precision / recall,
- latency and cost per question,
- comparison across model providers (Mistral and Claude models).

## Roadmap

- [ ] Project skeleton: configuration, entry point, PostgreSQL with a public dataset
- [ ] Evaluation harness and a baseline: whole schema in the prompt
- [ ] Schema retrieval with embeddings and pgvector
- [ ] LLM table selection
- [ ] Execution and self-correction loop
- [ ] Provider-agnostic model layer; Mistral vs Claude comparison
- [ ] Read-only safety, limits on rows, cost and retries
- [ ] API and Docker packaging
- [ ] Results write-up

## Safety

The agent only ever runs read-only queries, through a database role without write permissions.
Questions and database contents are treated as data, never as instructions.

## References

- Uber Engineering, *QueryGPT – Natural Language to SQL using Generative AI* — https://www.uber.com/blog/query-gpt
- Pinterest Engineering, *How we built Text-to-SQL at Pinterest* — https://medium.com/pinterest-engineering/how-we-built-text-to-sql-at-pinterest-30bad30dabff

## License

MIT
