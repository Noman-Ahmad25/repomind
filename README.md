# RepoMind

**Evidence-Driven Repository Intelligence Platform**

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python\&logoColor=white)
![Typer](https://img.shields.io/badge/Typer-CLI-009688)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql\&logoColor=white)
![pgvector](https://img.shields.io/badge/pgvector-Vector_Search-4169E1)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker\&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini-2.5_Pro-4285F4?logo=google\&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-success)

RepoMind is an AI-assisted repository intelligence platform that combines **deterministic static analysis** with **LLM-powered engineering reasoning** to help developers identify technical debt, prioritize engineering improvements, and generate implementation blueprints.

Unlike repository chat tools that answer:

> **"What does this code do?"**

RepoMind answers:

> **"What should engineers improve next, and why?"**

RepoMind performs **evidence-first analysis** using deterministic Python AST inspection before leveraging AI to transform verified findings into engineering recommendations and implementation blueprints.

---

# Features

## Deterministic Code Intelligence

* Deterministic AST-based repository auditing
* Function-level cyclomatic complexity analysis
* Nesting depth analysis
* Exception handling analysis
* Security anti-pattern detection
* Broad exception detection
* Empty exception detection
* God File detection
* Evidence-based repository health scoring
* Configurable engineering rules via `rules.json`

## AI-Powered Engineering Intelligence

* Repository maturity detection
* Engineering recommendation generation
* Refactoring blueprint generation
* Repository architecture reasoning

## Repository Intelligence

* Repository metadata extraction
* Repository structure analysis
* Dockerized PostgreSQL + pgvector knowledge base
* Vector embedding cache to prevent duplicate indexing
* CLI-first workflow
* Persistent repository intelligence

---

# Example

```bash
repomind analyze https://github.com/fastapi/fastapi
```

Example output

```text
Repository Stage: Mature

Health Report
Architecture: 82/100
Testing: 77/100
Security: 91/100
Documentation: 85/100
Scalability: 96/100

Top Findings

• GOD_FILE
  fastapi/routing.py
  6231 LOC

• HIGH_COMPLEXITY
  get_request_handler()
  Complexity: 35

• BROAD_EXCEPTION
  get_request_handler()

Recommended Next Action

Refactor routing.py into smaller routing modules to improve maintainability and reduce architectural complexity.
```

---

# Core Analysis Capabilities

RepoMind currently detects:

* High cyclomatic complexity
* Deep nesting
* Broad exception handling
* Empty exception blocks
* Oversized modules (God Files)
* Repository architecture metrics
* Repository maturity
* Deterministic repository health scores

---

# Installation

Clone the repository

```bash
git clone https://github.com/yourusername/repomind.git

cd repomind
```

Install dependencies

```bash
uv sync
```

Start PostgreSQL with pgvector

```bash
docker compose up -d
```

Create a `.env` file

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/repomind
GEMINI_API_KEY=your_api_key
```

---

# Database

RepoMind uses **PostgreSQL 16** with the **pgvector** extension running inside Docker for storing:

* Repository metadata
* Repository health reports
* Engineering findings
* Recommendations
* Vector embeddings

Default Docker configuration

| Setting  | Value                  |
| -------- | ---------------------- |
| Image    | pgvector/pgvector:pg16 |
| Database | repomind               |
| Username | postgres               |
| Password | password               |
| Port     | 5432                   |

Persistent data is stored using a Docker volume.

---

# Usage

Analyze a repository

```bash
repomind analyze <repository-url>
```

Run a deterministic AST audit

```bash
repomind audit <repository-url>
```

Generate an implementation blueprint

```bash
repomind blueprint <recommendation-id>
```

Generate an engineering report

```bash
repomind report <repository-url>
```

---

# Architecture

```text
                     Git Repository
                            │
                            ▼
                  Repository Parser
                            │
                            ▼
                Deterministic AST Engine
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
 Complexity Analysis   Security Analysis   God File Detection
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
                            ▼
           Evidence-Based Health Scoring Engine
                            │
               ┌────────────┴────────────┐
               ▼                         ▼
     PostgreSQL Metadata         pgvector Embeddings
          (Docker)                   (Docker)
               │                         │
               └────────────┬────────────┘
                            ▼
               AI Engineering Intelligence
                            │
                            ▼
             Recommendations & Blueprints
```

---

# Tech Stack

## Core

* Python
* Typer

## Database & Infrastructure

* PostgreSQL 16
* pgvector
* Docker
* Docker Compose

## Static Analysis

* Python AST
* Tree-Sitter
* GitPython

## AI

* Gemini 2.5 Pro
* BAAI BGE Small Embeddings

## Developer Experience

* Ruff
* MyPy
* Pytest

---

# Project Status

RepoMind is actively evolving into an engineering intelligence platform.

## Current Capabilities

* Deterministic AST-based repository analysis
* Evidence-based repository health scoring
* AI-assisted engineering recommendations
* Implementation blueprint generation
* Repository vector indexing with pgvector
* Dockerized PostgreSQL infrastructure
* Configurable engineering rules
* CLI-first workflow

## Planned Improvements

* Additional AST analysis rules
* Rich engineering reports
* Enhanced implementation blueprints
* Multi-language support
* Performance optimizations
* Advanced architectural metrics

---

# License

MIT License
