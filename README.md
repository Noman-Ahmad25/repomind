# RepoMind

> **Evidence-driven repository intelligence powered by deterministic static analysis and AI.**

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Typer](https://img.shields.io/badge/Typer-CLI-009688?style=for-the-badge)
![Tree-sitter](https://img.shields.io/badge/Tree--sitter-AST-5B3FD6?style=for-the-badge)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![pgvector](https://img.shields.io/badge/pgvector-Vector_DB-336791?style=for-the-badge)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google_Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white)
![Sentence Transformers](https://img.shields.io/badge/Sentence--Transformers-FF6F00?style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![uv](https://img.shields.io/badge/uv-Package_Manager-6E56CF?style=for-the-badge)
![Ruff](https://img.shields.io/badge/Ruff-Linter-D7FF64?style=for-the-badge)
![mypy](https://img.shields.io/badge/mypy-Type_Checked-2A6DB2?style=for-the-badge)
![Pytest](https://img.shields.io/badge/pytest-Testing-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)
![MIT License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

RepoMind is a CLI that analyzes software repositories using deterministic AST analysis, evaluates repository health, detects maintainability issues, prioritizes technical debt, and transforms verified findings into actionable engineering recommendations and implementation blueprints.

Unlike AI-only code review tools, RepoMind grounds every recommendation in deterministic evidence before using AI for reasoning and planning.

---

## Features

- 🔍 Deterministic AST-based repository analysis
- 📊 Repository health scoring
- 🤖 Evidence-based AI issue synthesis
- 🎯 Prioritized engineering recommendations
- 📋 Implementation blueprint generation
- 📝 Markdown report generation
- 🗄️ PostgreSQL + pgvector backed repository intelligence
- ⚙️ Configurable engineering rule profiles

---

## Workflow

```text
Repository
     │
     ▼
Analyze / Audit
     │
     ▼
Deterministic AST Analysis
     │
     ▼
Repository Health Assessment
     │
     ▼
AI Issue Synthesis
     │
     ▼
Engineering Recommendations
     │
     ▼
Implementation Blueprints
     │
     ▼
Markdown Reports
```

---

## Quick Start (Docker)

Start RepoMind with PostgreSQL:

```bash
docker compose up -d app
```

Run commands inside the container:

```bash
# Analyze a repository (recommended)
docker compose exec app repomind analyze https://github.com/fastapi/fastapi --rules rules_relaxed.json

# Strict analysis
docker compose exec app repomind analyze https://github.com/fastapi/fastapi --rules rules_strict.json

# Run deterministic AST audit
docker compose exec app repomind audit https://github.com/fastapi/fastapi --rules rules_relaxed.json

# Generate implementation blueprint
docker compose exec app repomind blueprint <recommendation-id>

# Export blueprint
docker compose exec app repomind blueprint <recommendation-id> --export

# Export repository report
docker compose exec app repomind report https://github.com/fastapi/fastapi
```

Stop RepoMind:

```bash
docker compose down
```

---

## Local Installation

Clone the repository:

```bash
git clone https://github.com/Noman-Ahmad25/repomind.git

cd repomind
```

Install dependencies:

```bash
uv sync
```

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key

DATABASE_URL=postgresql+psycopg://postgres:password@localhost:5432/repomind
```

Start PostgreSQL and run:

```bash
repomind analyze https://github.com/fastapi/fastapi --rules rules_relaxed.json
```

---

## Rule Profiles

RepoMind ships with configurable rule profiles.

### Relaxed

Recommended for general repository analysis.

```bash
repomind analyze <repository> --rules rules_relaxed.json
```

### Strict

Applies lower thresholds to detect more engineering issues.

```bash
repomind analyze <repository> --rules rules_strict.json
```

---

## Typical Workflow

```bash
# Analyze repository
repomind analyze <repository> --rules rules_relaxed.json

# Review deterministic findings
repomind audit <repository> --rules rules_relaxed.json

# Export analysis report
repomind report <repository>

# Generate implementation blueprint
repomind blueprint <recommendation-id>

# Export blueprint
repomind blueprint <recommendation-id> --export
```

Generated reports are saved under:

```text
reports/
└── owner_repository/
    ├── analysis_owner_repository.md
    ├── blueprint_<recommendation-id>.md
    └── ...
```

---

## Tech Stack

- Python 3.12+
- Typer
- Tree-sitter
- Python AST
- PostgreSQL
- pgvector
- SQLAlchemy
- Google Gemini
- Sentence Transformers
- GitPython
- Docker

---

## Example Output

```
Architecture     97/100
Testing          92/100
Security         76/100
Documentation    85/100
Scalability     100/100

Overall          91/100
```

```
Top Recommendation

Refactor get_openapi_path to reduce cyclomatic complexity

Priority 9.4/10
Impact   8.5
Effort   7.0
```

---

## Documentation

Comprehensive documentation, architecture details, and implementation guides are available on the project documentation website.

---

## Roadmap

- Multi-language analysis
- Semantic repository search
- Incremental analysis
- GitHub integration
- Automatic fix generation
- Agentic implementation workflows

---

## Contributing

Contributions, bug reports, feature requests, and discussions are welcome.

---

## License

MIT License.