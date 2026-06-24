# RepoMind

**AI-powered Repository Intelligence Platform**

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python\&logoColor=white)
![Typer](https://img.shields.io/badge/Typer-CLI-009688)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql\&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini-2.5_Pro-4285F4?logo=google\&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-success)

RepoMind analyzes source code repositories, identifies engineering improvement opportunities, prioritizes the highest-impact next actions, and generates implementation blueprints.

Unlike repository chat tools that answer:

> "What does this code do?"

RepoMind focuses on:

> "What should I improve next?"

---

## Features

* Repository analysis and metadata extraction
* Repository maturity detection
* Repository health assessment
* Function-level code auditing
* Engineering recommendation generation
* Implementation blueprint generation
* PostgreSQL + pgvector powered repository intelligence
* CLI-first workflow

---

## Example

```bash
repomind analyze https://github.com/fastapi/fastapi
```

Output:

```text
Repository Stage: Mature

Top Finding:
get_request_handler()
Complexity: 32
Nesting: 6

Recommended Next Action:
Refactor request handling flow to reduce complexity and improve maintainability.
```

---

## Installation

```bash
git clone https://github.com/yourusername/repomind.git

cd repomind

uv sync
```

Create a `.env` file:

```env
DATABASE_URL=postgresql://...
GEMINI_API_KEY=your_api_key
```

---

## Usage

Analyze a repository:

```bash
repomind analyze <repository-url>
```

Run a deterministic audit:

```bash
repomind audit <repository-url>
```

Generate a blueprint:

```bash
repomind blueprint <recommendation-id>
```

Generate a report:

```bash
repomind report <repository-url>
```

---

## Documentation

Full documentation, architecture details, setup guides, and roadmap are available on the documentation website.

**Documentation:** 

---

## Tech Stack

### Core

* Python
* Typer
* PostgreSQL
* pgvector

### Repository Analysis

* Tree-Sitter
* GitPython

### AI

* Gemini 2.5 Pro
* BGE Small Embeddings

### Quality

* Ruff
* MyPy
* Pytest

---

## Status

RepoMind is currently in active development and focused on improving:

* Repository understanding
* Recommendation quality
* Blueprint generation
* Deterministic code analysis

---

## License

MIT License
