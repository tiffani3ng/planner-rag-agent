# Anchor — RAG-powered scheduling assistant

***A grounded AI planning assistant that turns scattered deadlines, task lists, syllabi, and calendar data into actionable work plans.***

The intended product is a user-facing planning assistant for students and busy professionals who want to ask natural-language questions like:

```text
What should I work on this week?
I have 3 hours free. What should I do?
Can I take a weeklong vacation starting today?
What do I need to finish before my demo?
```

Anchor retrieves the relevant deadlines and commitments from the user’s own documents, then generates a feasible plan that explains what to prioritize and cites the source behind each recommendation.

---

## Current Status

Anchor is currently implemented as a **CLI-based MVP**.

The command-line interface is not the intended final app. It is a validation layer for testing the core system behavior:

- document ingestion,
- chunking,
- local embeddings,
- persistent vector storage,
- semantic retrieval,
- date-aware retrieval,
- source-grounded generation,
- response-time measurement,
- and retrieval debugging.

The full intended app is defined in `CAPB.md`: a non-technical user-facing planning assistant where users can upload or connect planning documents, ask questions in natural language, and receive personalized scheduling recommendations with citations, feasibility checks, and ongoing updates.

---

## Product Vision

Anchor is built around a simple idea:

> People should be able to ask, “What should I work on next?” and get an answer grounded in their real deadlines, commitments, and documents.

Most planning tools track tasks, but they do not always help users reason across competing obligations. Anchor is designed to bridge that gap by combining retrieval, scheduling context, and generated recommendations.

The long-term goal is a planning assistant that can:

- consolidate deadlines from multiple sources,
- identify what is urgent or blocking,
- generate realistic work plans,
- cite the source behind each recommendation,
- update when new tasks or deadlines appear,
- learn from user feedback,
- and help users make better decisions about time allocation.

---

## Why I Built This

Students and professionals often manage work across disconnected systems:

- course syllabi,
- PDF assignment sheets,
- Markdown task lists,
- calendar exports,
- project boards,
- routines,
- and informal notes.

The information is there, but it is fragmented.

Anchor explores whether a lightweight RAG system can turn a small personal corpus into a useful planning assistant that is:

- **grounded** in the user’s actual documents,
- **traceable** through citations,
- **actionable** through concrete time blocks and task ordering,
- **context-aware** through deadline and priority metadata,
- **privacy-conscious** through local embeddings,
- and **measurable** through retrieval quality, latency, and recommendation usefulness.

---

## MVP vs. Intended App

| Layer | Current MVP | Intended App |
|---|---|---|
| Interface | Command-line interface | User-facing chat or planning interface |
| User | Technical tester/developer | Non-technical student or professional |
| Input | Local files in `data/` folders | Uploaded files, connected calendars, task apps, and routines |
| Retrieval | Chroma vector search with metadata/date logic | Hybrid retrieval with stronger filtering, reranking, and live updates |
| Planning | Generated text answer from retrieved chunks | Dynamic schedule recommendations with editable task states |
| Evaluation | Manual test outputs and response-time logs | Ongoing tracking of relevance, feasibility, adoption, and user feedback |
| Execution | Advisory only | Still advisory first; future versions may create calendar/task suggestions with review |
| Goal | Validate the core RAG workflow | Deliver a reliable personal planning assistant |

The CLI exists to make the system inspectable. It lets me see what Anchor retrieved, how long retrieval and generation took, and whether the answer was grounded in the right evidence.

---

## What Anchor Does

Anchor answers natural-language planning questions using a retrieval-augmented generation pipeline.

Example questions:

```text
What should I work on this week?
Can I take a weeklong vacation starting today?
I have 3 hours free. What should I work on?
What is due before my sprint demo?
What should I prioritize today?
```

Anchor can:

- retrieve relevant tasks and deadlines,
- prioritize urgent work,
- explain why a task matters now,
- generate short work plans,
- cite source files,
- identify blockers before time off,
- and expose the retrieved context in verbose mode.

---

## Example Output

### Query

```bash
"What should I work on this week?"
```

### Generated Recommendation

Anchor then generates a prioritized weekly plan:

> # Your Week at a Glance (Sep 28 – Oct 5)
>
> You have one urgent item today and a Sprint 1 demo wrapping up the week. Here's how to tackle it:
>
> ## Monday, Sep 28 (TODAY — urgent)
> - **Finish Lab 2: TDD** — submit code + coverage report to GitHub by **11:59 PM tonight**. Block off 2–3 hours this evening if not yet done. [software_dev_tasks.md]
>
> ## Tuesday, Sep 29 – Wednesday, Sep 30
> - **Read Popper, Ch. 1 ("Science: Conjectures and Refutations")** for Reading Response 2. Aim for a 1.5–2 hour focused reading block on Tuesday; due **Oct 1**. [philosophy_tasks.md]
> - Take notes as you read — they'll feed directly into the response paper (due Oct 6).
> 
> .
> .
> .
>
> ## Monday, Oct 5
> - **Sprint 1 Demo day.** Submit the **retrospective document** (what went well / what to improve). Draft it after the demo while it's fresh — 30–45 min. [software_dev_tasks.md]
>
> ## Priority Order
> 1. Lab 2 submission (tonight) [software_dev_tasks.md]
> 2. Popper reading (by Oct 1) [philosophy_tasks.md]
> 3. Demo deployment → rehearsal → retrospective [software_dev_tasks.md]
>
> Knock out tonight's lab first — everything else has breathing room.

The purpose is not just to produce a fluent answer. The purpose is to show:

```text
What was retrieved?
Why was this recommended?
Which source supports it?
What should the user do next?
```

---

## System Architecture

Anchor currently follows a lightweight RAG pipeline:

```text
User Documents
    ↓
Parsers
    ↓
Chunks + Metadata
    ↓
Local Embeddings
    ↓
Chroma Vector Store
    ↓
Semantic + Date-Aware Retrieval
    ↓
Hosted LLM Generation
    ↓
Cited Planning Recommendation
```

---

## Core Components

### 1. Document Ingestion

The ingestion pipeline scans local folders and converts documents into chunks.

Supported input folders:

```text
data/
├── syllabi/
├── tasks/
└── calendars/
```

Supported file types:

| Source type | Format | Parser |
|---|---|---|
| Syllabi / course docs | PDF | `pdf_parser.py` |
| Task lists | Markdown / TXT | `md_parser.py` |
| Calendar exports | ICS | `ics_parser.py` |

Each parsed chunk is stored with metadata such as:

- source file,
- document type,
- due date,
- priority,
- and course/category when available.

---

### 2. Local Embeddings

Anchor uses a local SentenceTransformer embedding model:

```text
all-MiniLM-L6-v2
```

This keeps embedding generation local and low-cost. The full document corpus does not need to be sent to an external embedding API.

---

### 3. Vector Store

Anchor stores embedded chunks in a persistent ChromaDB collection:

```text
chroma_db/
```

Chroma stores:

- text chunks,
- embeddings,
- source metadata,
- due dates,
- priorities,
- and course labels.

---

### 4. Retrieval

The retriever uses semantic search over the vector store, then adds simple date-aware logic for time-sensitive queries.

Anchor recognizes timeframe language such as:

```text
today
tomorrow
this week
next week
this month
in 3 days
Friday
```

When the query includes a timeframe, Anchor pulls deadline chunks in that date range and merges them with semantic results. This helps planning queries prioritize deadlines rather than relying only on textual similarity.

---

### 5. Generation

The generator uses a hosted language model to turn retrieved chunks into a clear recommendation.

The generation prompt instructs the model to:

- use only retrieved context,
- avoid inventing tasks or deadlines,
- cite source files after each task,
- suggest concrete time blocks and ordering,
- account for priorities,
- use plain language,
- and keep the answer concise.

---

## Current CLI Commands

### Ingest documents

```bash
python -m src.cli ingest
```

Parses all supported documents in the `data/` folder and stores chunks in the local vector database.

### Ask a planning question

```bash
python -m src.cli ask "What should I work on this week?"
```

Retrieves relevant chunks and generates a cited planning recommendation.

### Inspect retrieval

```bash
python -m src.cli ask "What should I work on this week?" --verbose
```

Shows retrieved chunks before generation.

### Change retrieval depth

```bash
python -m src.cli ask "What's due this week?" --top-k 8
```

Retrieves more chunks before generation.

### List the knowledge base

```bash
python -m src.cli list
```

Shows a summary of stored chunks by type and source.

### Clear the vector store

```bash
python -m src.cli clear
```

Deletes the local vector store so the documents can be re-ingested.

---

## Repository Structure

```text
planner-rag-agent/
├── CAPB.md                    # Full product/design document
├── README.md                  # Project overview
├── requirements.txt           # Python dependencies
├── src/
│   ├── cli.py                 # CLI MVP: ingest, ask, list, clear
│   ├── config.py              # Test date/current date configuration
│   ├── generator.py           # Hosted LLM generation with citation rules
│   ├── ingest.py              # Document ingestion, embeddings, Chroma upsert
│   ├── retriever.py           # Semantic retrieval + date-aware filtering
│   └── parsers/
│       ├── pdf_parser.py      # PDF syllabus parser
│       ├── md_parser.py       # Markdown/TXT task parser
│       └── ics_parser.py      # Calendar event parser
├── data/
│   ├── syllabi/               # PDF course documents
│   ├── tasks/                 # Markdown/TXT task lists
│   └── calendars/             # ICS calendar files
└── chroma_db/                 # Generated local vector store after ingestion
```

---

## Sample Corpus

The current sample corpus includes synthetic academic and planning documents such as:

```text
software_dev_tasks.md
philosophy_tasks.md
portfolio_tasks.md
cs350_software_development.pdf
fin405_portfolio_allocation.pdf
```

The sample data includes:

- software development labs,
- sprint demo preparation,
- philosophy readings and response papers,
- portfolio allocation problem sets,
- exams,
- project proposals,
- final reports,
- and course planning milestones.

The current test configuration fixes the date to:

```text
September 28, 2026
```

This makes the sample outputs reproducible regardless of the real calendar date.

---

## How to Run the MVP

### 1. Clone the repository

```bash
git clone https://github.com/tiffani3ng/planner-rag-agent.git
cd planner-rag-agent
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Add environment variables

Create a `.env` file:

```bash
ANTHROPIC_API_KEY=your_api_key_here
```

Optional:

```bash
HF_TOKEN=your_huggingface_token_here
```

A Hugging Face token is not required, but authenticated requests may improve download speed and rate limits for embedding model access.

### 5. Ingest documents

```bash
python -m src.cli ingest
```

### 6. Ask a question

```bash
python -m src.cli ask "What should I work on this week?"
```

For debugging:

```bash
python -m src.cli ask "What should I work on this week?" --verbose
```

---

## Test Outputs and Evaluation

The current MVP has been tested on several planning questions.

### 1. Weekly planning query

```text
What should I work on this week?
```

Anchor retrieved upcoming tasks from the philosophy and software development task lists, then generated a weekly plan that prioritized:

- Lab 2 due September 28,
- Popper reading due October 1,
- Sprint 1 demo deployment due October 3,
- demo rehearsal on October 4,
- and Sprint 1 retrospective/demo work on October 5.

### 2. Vacation feasibility query

```text
Can I take a weeklong vacation starting today?
```

Anchor correctly identified that a weeklong vacation starting immediately was not realistic because of a same-day Lab 2 deadline and upcoming class preparation.

This demonstrates an important behavior: the system can use retrieved deadlines to make a grounded feasibility judgment, not just list tasks.

### 3. Short time-block query

```text
I have 3 hours free. What should I work on?
```

Anchor generated a structured three-hour work block. However, this test also revealed a weakness: the assistant surfaced a later Lab 4 task instead of the most urgent same-day Lab 2 task.

That failure is useful because it identifies the next technical improvement: stronger urgency-aware reranking for open-ended planning queries.

---

## Performance Snapshot

| Query | Retrieval time | Generation time | Total response time | Outcome |
|---|---:|---:|---:|---|
| `What should I work on this week?` | 0.5s | 12.0s | 12.5s | Strong weekly prioritization with cited tasks |
| `Can I take a weeklong vacation starting today?` | 0.4s | 8.5s | 8.9s | Correctly identifies immediate blockers |
| `What should I work on this week?` | 0.3s | 11.3s | 11.7s | Similar plan without verbose mode |
| `I have 3 hours free. What should I work on?` | 0.3s | 10.7s | 11.0s | Useful plan, but reveals urgency-ranking weakness |

### Evaluation Takeaways

- Retrieval is fast enough for interactive use.
- Generation is currently the main latency bottleneck.
- Source citations are working.
- Weekly deadline planning is strong.
- Feasibility reasoning is promising.
- Open-ended time-block planning needs better urgency weighting.
- The MVP does not yet meet the intended ≤5s latency target.

---

## Success Criteria

Anchor is evaluated by whether it helps users make better planning decisions, not just whether it generates fluent text.

| Success criterion | Current status |
|---|---|
| Retrieve relevant tasks and deadlines | Working |
| Cite source documents | Working |
| Generate actionable recommendations | Working |
| Support deadline-aware planning | Partially working |
| Reject unrealistic plans when blockers exist | Working in test cases |
| Keep retrieval latency low | Working |
| Keep total response time ≤5s | Not yet met |
| Avoid invented tasks/deadlines | Mostly working through retrieved-context prompting |
| Prioritize urgent tasks reliably | Needs improvement for open-ended queries |
| Update continuously from live user data | Not yet implemented |
| Track user feedback and task completion | Not yet implemented |

---

## Design Principles

### 1. Ground every recommendation

Anchor should not invent tasks, deadlines, or commitments. Recommendations should be tied to retrieved evidence.

### 2. Show why the plan was suggested

A useful planning assistant should not be a black box. Source citations help users understand why something was prioritized.

### 3. Prioritize feasibility over generic productivity advice

The assistant should consider deadlines, available time, task priority, and known commitments.

### 4. Keep the system inspectable

The CLI MVP exposes retrieval results and response times so failure modes can be diagnosed.

### 5. Treat planning as an iterative workflow

The intended app should improve over time through user feedback, updated documents, and completion tracking.

---

## Known Limitations

### 1. The CLI is only an MVP

The command-line interface is useful for testing, but it is not the intended user experience. The full product should have a user-facing chat or dashboard interface.

### 2. Generation latency is too high

Retrieval is fast, but generation currently pushes total response time above the intended target.

Potential improvements:

- use a faster generation model,
- reduce output length,
- stream generated responses,
- cache common queries,
- or use a smaller local model for simple planning cases.

### 3. Urgency ranking needs improvement

The short time-block query revealed that semantic relevance can overpower deadline urgency. Anchor needs a reranking layer that combines semantic similarity with due-date proximity and priority.

### 4. Calendar reasoning is incomplete

Anchor can parse ICS files, but it does not yet fully reason around calendar availability or avoid suggesting work during existing commitments.

### 5. No completion state

Anchor does not yet maintain task status. It cannot reliably distinguish between unfinished and already completed work unless that information appears in the documents.

### 6. Data can become stale

If a task list or syllabus changes, the vector store must be updated. Future versions need incremental ingestion or live integrations.

### 7. Privacy needs stronger controls for production

Embeddings are local, but generated answers are produced through a hosted model using retrieved context. Sensitive deployments would need redaction, local generation, or stricter data-governance controls.

---

## Future Work

### 1. Build the intended app interface

The CLI should evolve into a user-facing planning interface where users can:

- upload documents,
- connect calendars,
- ask questions in natural language,
- view retrieved sources,
- edit task status,
- and save generated plans.

### 2. Add urgency-aware reranking

Add a scoring layer that combines:

```text
semantic relevance
+ due-date proximity
+ priority
+ estimated effort
+ completion status
+ available time window
```

This would make questions like “I have 3 hours free” more reliable.

### 3. Add live calendar integration

Connect to calendar APIs so Anchor can reason around actual availability instead of only retrieving deadlines.

Potential integrations:

- Google Calendar,
- Microsoft Outlook,
- Canvas or Moodle,
- GitHub Issues,
- Notion,
- Todoist,
- Google Tasks.

### 4. Track task state

Add task states such as:

```text
not started
in progress
blocked
done
```

This would prevent Anchor from recommending completed work.

### 5. Add user feedback loops

Let users mark recommendations as:

```text
helpful
irrelevant
too ambitious
already done
wrong source
missing deadline
```

This feedback could guide prompt revisions, reranking, and future personalization.

### 6. Add evaluation harness

Build a small benchmark of planning questions with expected retrieved sources and expected recommendation behavior.

Suggested checks:

```text
Does Anchor retrieve the right source?
Does it identify urgent tasks?
Does it cite every task?
Does it avoid unsupported deadlines?
Does it make a feasible plan?
How long does retrieval take?
How long does generation take?
```

### 7. Improve privacy and deployment readiness

Future versions should support:

- encrypted local storage,
- optional local generation,
- redaction before API calls,
- authentication,
- multi-user data isolation,
- and audit logs for recommendations.

### 8. Add monitoring

Track whether Anchor is actually helping users plan better.

Possible outcome metrics:

- task completion rate,
- missed-deadline reduction,
- recommendation acceptance rate,
- user trust rating,
- plan feasibility rating,
- source citation accuracy,
- weekly planning adherence,
- and average response latency.

---

## Requirements

Core dependencies:

```text
chromadb
sentence-transformers
anthropic
pypdf
icalendar
python-dotenv
click
fpdf2
```

See:

```text
requirements.txt
```

---

## Project Files

| File | Purpose |
|---|---|
| `README.md` | Project overview and MVP usage guide |
| `CAPB.md` | Full product/design document and intended app framing |
| `src/cli.py` | CLI MVP for ingestion, querying, listing, and clearing |
| `src/ingest.py` | Document ingestion and embedding pipeline |
| `src/retriever.py` | Semantic retrieval and date-aware filtering |
| `src/generator.py` | Hosted LLM generation with citation rules |
| `src/config.py` | Test date/current-date configuration |
| `src/parsers/pdf_parser.py` | PDF parsing for syllabi and course documents |
| `src/parsers/md_parser.py` | Markdown/TXT parsing for task lists |
| `src/parsers/ics_parser.py` | ICS parsing for calendar events |
| `data/tasks/` | Sample Markdown task lists |
| `data/syllabi/` | Sample PDF course documents |
| `data/calendars/` | Sample ICS calendar exports |

---

## Responsible AI and Privacy Notes

Anchor handles personal planning data, so recommendations should remain transparent, inspectable, and user-controlled.

Current safeguards:

- local embeddings,
- local vector storage,
- source citations,
- retrieved-context-only prompting,
- no autonomous task execution,
- and CLI-level inspection of retrieved evidence.

Important caveat:

The current generator sends retrieved context to a hosted LLM. For sensitive use cases, future versions should support local generation, stronger redaction, and explicit user controls over what context is sent.

---

## What This Project Demonstrates


Anchor demonstrates:

- RAG product design,
- local embedding pipelines,
- vector search with metadata,
- date-aware retrieval,
- source-grounded generation,
- CLI-based MVP validation,
- latency measurement,
- qualitative evaluation of AI recommendations,
- and iterative diagnosis of model behavior.

The central lesson is that useful AI planning requires more than a fluent answer: it needs the right retrieved evidence, transparent citations, measurable latency, and a feedback loop for diagnosing whether recommendations actually help users make better decisions.

---

## Author

**Tiffanie Ng**  
Economics & Mathematics major, Scientific Computing concentration  
Kenyon College ’26  

[LinkedIn](https://www.linkedin.com/in/tiffanie-ng)
