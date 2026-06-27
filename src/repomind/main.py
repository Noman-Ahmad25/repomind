import typer
import time
from pathlib import Path
from typing import Any
from dotenv import load_dotenv
from sqlalchemy.orm import Session

import logging

# Core Pipeline
from repomind.loader import clone_repository, validate_github_url
from repomind.scanner import RepositoryScanner
from repomind.analyzer import calculate_deterministic_health, classify_maturity
from repomind.validator import load_rules

# Database & Storage
from repomind.database import SessionLocal
from repomind.models import Repository, RepositoryHealth, Finding, Recommendation
from repomind.storage import save_repository, save_health_scores, save_findings, save_recommendations, save_blueprint

# Intelligence & Math
from repomind.prioritizer import get_top_issues
from repomind.ai import detect_repository_issues, generate_recommendations, generate_blueprint

# Reporting
from repomind.reporting import generate_analysis_markdown, generate_blueprint_markdown, save_report


load_dotenv()

logging.basicConfig(
    filename="repomind.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(module)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

app = typer.Typer(
    help="RepoMind AI - Repository Intelligence Platform",
    add_completion=False,
)


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------

def _cmd_header(subtitle: str, **kv_pairs: str) -> None:
    """Print the standard command title block followed by key/value context lines."""
    typer.echo("")
    typer.secho(f"  RepoMind AI  ·  {subtitle}", bold=True)
    typer.secho("  " + "═" * 58, fg=typer.colors.BRIGHT_BLACK)
    for label, value in kv_pairs.items():
        _kv(label, value)


def _section(title: str, color: str = typer.colors.WHITE) -> None:
    typer.echo("")
    typer.secho(f"  {title}", fg=color, bold=True)
    typer.secho("  " + "─" * 58, fg=typer.colors.BRIGHT_BLACK)


def _kv(label: str, value: str, indent: int = 4) -> None:
    pad = " " * indent
    typer.secho(f"{pad}{label:<18}", nl=False, fg=typer.colors.BRIGHT_BLACK)
    typer.echo(value)


def _ok(msg: str) -> None:
    typer.secho(f"  ✔  {msg}", fg=typer.colors.GREEN)


def _info(msg: str) -> None:
    typer.secho(f"  →  {msg}", fg=typer.colors.BRIGHT_BLACK)


def _error(msg: str) -> None:
    typer.secho(f"  ✖  {msg}", fg=typer.colors.RED, bold=True)


def _warn(msg: str) -> None:
    typer.secho(f"  ⚠  {msg}", fg=typer.colors.YELLOW)


def _score_bar(label: str, score: int, width: int = 20) -> None:
    filled = int(score / 100 * width)
    bar = "█" * filled + "░" * (width - filled)
    color = typer.colors.GREEN if score >= 70 else typer.colors.YELLOW if score >= 40 else typer.colors.RED
    typer.secho(f"    {label:<16}", nl=False, fg=typer.colors.BRIGHT_BLACK)
    typer.secho(f"{bar}  ", nl=False, fg=color)
    typer.secho(f"{score:>3}/100", fg=color, bold=(score >= 70))


# ---------------------------------------------------------------------------
# Compound print helpers
# ---------------------------------------------------------------------------

def _print_health_scores(analysis: dict[str, Any], health_scores: dict[str, Any]) -> None:
    _kv("Stage", analysis.get('stage', 'Unknown'))
    score_fields = [
        ("Architecture",  'architecture_score'),
        ("Testing",       'testing_score'),
        ("Security",      'security_score'),
        ("Documentation", 'documentation_score'),
        ("Scalability",   'scalability_score'),
    ]
    for label, key in score_fields:
        typer.echo("")
        _score_bar(label, health_scores[key])
    typer.echo("")
    typer.secho("    " + "─" * 38, fg=typer.colors.BRIGHT_BLACK)
    _score_bar("Overall", health_scores['maturity_score'])


def _print_issue(i: int, issue: dict[str, Any]) -> None:
    file_path = issue.get('file_path', issue.get('file', 'Unknown'))
    func_name = issue.get('function_name', issue.get('function', 'Unknown'))
    start     = issue.get('start_line')
    end       = issue.get('end_line')
    line_info = f":{start}-{end}" if (start and end) else ""
    severity  = issue.get('severity', 'medium').upper()
    sev_color = (
        typer.colors.RED if severity in ('HIGH', 'CRITICAL')
        else typer.colors.YELLOW if severity == 'MEDIUM'
        else typer.colors.BRIGHT_BLACK
    )

    typer.secho(f"  [{i:>2}] ", nl=False, fg=typer.colors.BRIGHT_BLACK)
    typer.secho(issue.get('title', 'Untitled'), bold=True)
    typer.secho("       Category  ", nl=False, fg=typer.colors.BRIGHT_BLACK)
    typer.echo(issue.get('category', 'Technical Debt'))
    typer.secho("       Severity  ", nl=False, fg=typer.colors.BRIGHT_BLACK)
    typer.secho(severity, fg=sev_color, bold=True)
    typer.secho("       Location  ", nl=False, fg=typer.colors.BRIGHT_BLACK)
    typer.echo(f"{file_path}  →  {func_name}{line_info}")
    typer.secho("       Detail    ", nl=False, fg=typer.colors.BRIGHT_BLACK)
    typer.echo(issue.get('description', 'No description provided.'))
    typer.echo("")


def _print_recommendation(rec: Recommendation) -> None:
    if rec.is_recommended:
        typer.secho("  ★  Top Priority", fg=typer.colors.YELLOW, bold=True)
    typer.secho("  ID      ", nl=False, fg=typer.colors.BRIGHT_BLACK)
    typer.secho(str(rec.id), fg=typer.colors.CYAN)
    typer.secho("  Title   ", nl=False, fg=typer.colors.BRIGHT_BLACK)
    typer.secho(str(rec.title), bold=True)
    typer.secho("  Score   ", nl=False, fg=typer.colors.BRIGHT_BLACK)
    typer.echo(f"Priority {rec.priority_score}/10  ·  Impact {rec.impact_score}  ·  Effort {rec.effort_score}")
    typer.secho("  Rationale  ", nl=False, fg=typer.colors.BRIGHT_BLACK)
    typer.echo(str(rec.description))
    typer.secho("  Next    ", nl=False, fg=typer.colors.BRIGHT_BLACK)
    typer.secho(f"repomind blueprint {rec.id}", fg=typer.colors.BRIGHT_BLACK)
    typer.echo("")


def _print_blueprint(blueprint_data: dict[str, Any]) -> None:
    typer.secho("  Goal", fg=typer.colors.BRIGHT_BLACK, bold=True)
    typer.echo(f"    {blueprint_data.get('goal')}")

    files_to_create = blueprint_data.get('files_to_create', [])
    if files_to_create:
        typer.echo("")
        typer.secho("  Files to Create", fg=typer.colors.BRIGHT_BLACK, bold=True)
        for f in files_to_create:
            typer.secho(f"    +  {f}", fg=typer.colors.GREEN)

    steps = blueprint_data.get('implementation_steps', [])
    if steps:
        typer.echo("")
        typer.secho("  Implementation Steps", fg=typer.colors.BRIGHT_BLACK, bold=True)
        for i, step in enumerate(steps, 1):
            typer.secho(f"    {i:>2}.  ", nl=False, fg=typer.colors.BRIGHT_BLACK)
            typer.echo(step)

    typer.echo("")
    typer.secho("  Estimated Effort  ", nl=False, fg=typer.colors.BRIGHT_BLACK)
    typer.secho(str(blueprint_data.get('estimated_effort', 'N/A')), bold=True)
    typer.echo("")


# ---------------------------------------------------------------------------
# Pipeline helpers
# ---------------------------------------------------------------------------

def _resolve_local_path(db: Session, repository_url: str) -> str:
    """Return a local path for the repo, cloning if not already cached."""
    repo = db.query(Repository).filter(Repository.github_url == repository_url).first()
    if not repo or not Path(repo.local_path).exists():
        _info("Not found in local cache. Cloning…")
        meta = clone_repository(repository_url)
        return meta["local_path"]
    return str(repo.local_path)


def _run_scanner(local_path: str, rules: str) -> RepositoryScanner:
    """Load rules, initialise and run the scanner, then return it."""
    parsed_rules = load_rules(rules)
    scanner = RepositoryScanner(local_path, parsed_rules)
    scanner.scan()
    return scanner


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

@app.command()
def analyze(
    repository_url: str,
    rules: str = typer.Option("rules.json", "--rules", "-r", help="Path to custom rules configuration file")
) -> None:
    """Analyze a repository and generate recommendations."""
    _cmd_header("Static Analysis & Intelligence", Target=repository_url, Rules=rules)

    if not validate_github_url(repository_url):
        _error("Invalid GitHub URL. Expected format: https://github.com/<owner>/<repo>")
        raise typer.Exit(code=1)

    db = SessionLocal()
    try:
        # ── Clone ────────────────────────────────────────────────────────────
        _section("Clone")
        _info("Fetching latest commits…")
        meta = clone_repository(repository_url, force_update=True)
        local_path = meta["local_path"]
        _ok(f"Cloned to {local_path}")

        repo_record = save_repository(db, meta, repository_url)
        if repo_record is None:
            _error("Database registration failed. Check db connectivity and retry.")
            raise typer.Exit(code=1)
        _kv("Record ID", str(repo_record.id))

        # ── Scan ─────────────────────────────────────────────────────────────
        _section("Scan")
        _info("Running single-pass AST scan…")
        scanner   = _run_scanner(local_path, rules)
        structure = scanner.structure
        findings  = scanner.findings

        _kv("Project Type",    scanner.context['project_type'])
        _kv("Languages",       ', '.join(scanner.context['languages']))
        _kv("Files Parsed",    str(structure['files']))
        _kv("Functions Found", str(structure['functions']))

        # ── Health Scores ────────────────────────────────────────────────────
        _section("Health Scores", color=typer.colors.BLUE)
        _info("Computing evidence-based scores…")
        analysis      = classify_maturity(structure)
        health_scores = calculate_deterministic_health(structure, findings)
        save_health_scores(db, repo_record.id, health_scores)
        _print_health_scores(analysis, health_scores)

        # ── Issues ───────────────────────────────────────────────────────────
        _section("Issues", color=typer.colors.RED)
        _info("Running AI issue synthesis on top audit findings…")
        top_audit_findings = get_top_issues(findings, limit=20)
        top_findings       = detect_repository_issues(meta, top_audit_findings)
        save_findings(db, repo_record.id, top_findings)

        if not top_findings:
            _ok("No issues detected in top audit findings.")
        else:
            typer.echo("")
            for i, issue in enumerate(top_findings, 1):
                _print_issue(i, issue)

        # ── Recommendations ──────────────────────────────────────────────────
        _section("Recommendations", color=typer.colors.GREEN)
        _info("Generating evidence-based engineering recommendations…")

        saved_findings_objects = db.query(Finding).filter(Finding.repository_id == repo_record.id).all()
        raw_recs   = generate_recommendations(meta, analysis['stage'], saved_findings_objects)
        saved_recs = save_recommendations(db, repo_record.id, raw_recs, saved_findings_objects)

        if not saved_recs:
            _warn("No recommendations produced. Check findings and retry.")
        else:
            typer.echo("")
            for rec in saved_recs:
                _print_recommendation(rec)

        typer.echo("")

    except Exception as e:
        logger.error(f"Analysis failed for {repository_url}", exc_info=True)
        _error(f"Repository analysis failed: {e}")
        raise typer.Exit(code=1)
    finally:
        db.close()


@app.command()
def audit(
    repository_url: str,
    rules: str = typer.Option("rules.json", "--rules", "-r", help="Path to custom rules configuration file")
) -> None:
    """Run a fast, offline, deterministic AST audit without AI synthesis."""
    _cmd_header("AST Audit")

    db = SessionLocal()
    try:
        local_path = _resolve_local_path(db, repository_url)
        _kv("Path",  local_path)
        _kv("Rules", rules)

        _section("AST Scan")
        _info("Parsing source files and evaluating rule violations…")
        start_time     = time.time()
        scanner        = _run_scanner(local_path, rules)
        findings       = scanner.findings
        execution_time = time.time() - start_time

        if not findings:
            _ok(f"Clean — no rule violations found.  ({execution_time:.2f}s)")
            typer.echo("")
            return

        sorted_findings = sorted(findings, key=lambda x: x.get('complexity', 0), reverse=True)

        typer.echo("")
        typer.secho(
            f"  {len(sorted_findings)} violation(s)  ·  {execution_time:.2f}s",
            fg=typer.colors.RED, bold=True
        )
        typer.secho("  Ranked by cyclomatic complexity — top 10\n", fg=typer.colors.BRIGHT_BLACK)

        for i, issue in enumerate(sorted_findings[:10], 1):
            violations = [f.get('type') for f in issue.get('findings', [])]
            typer.secho(f"  [{i:>2}] ", nl=False, fg=typer.colors.BRIGHT_BLACK)
            typer.secho(issue['function'], bold=True, fg=typer.colors.CYAN)
            typer.secho("       File        ", nl=False, fg=typer.colors.BRIGHT_BLACK)
            typer.echo(issue['file'])
            typer.secho("       Complexity  ", nl=False, fg=typer.colors.BRIGHT_BLACK)
            typer.echo(str(issue['complexity']))
            typer.secho("       Nesting     ", nl=False, fg=typer.colors.BRIGHT_BLACK)
            typer.echo(str(issue['nesting']))
            typer.secho("       Violations  ", nl=False, fg=typer.colors.BRIGHT_BLACK)
            typer.secho(', '.join(violations), fg=typer.colors.YELLOW)
            typer.echo("")

        if len(sorted_findings) > 10:
            _info(f"{len(sorted_findings) - 10} additional violation(s) omitted.")
            typer.echo("")
            typer.secho(
                "  Run `repomind analyze` to synthesize all findings into prioritized refactoring blueprints.",
                fg=typer.colors.MAGENTA
            )

        typer.echo("")

    except Exception as e:
        logger.error(f"Audit failed for recommendation {repository_url}", exc_info=True)
        _error(f"AST audit failed: {e}")
        raise typer.Exit(code=1)
    finally:
        db.close()


@app.command()
def report(repository_url: str) -> None:
    """Generate a markdown report for an analyzed repository."""
    _cmd_header("Report Export", Target=repository_url)

    db = SessionLocal()
    try:
        repo = db.query(Repository).filter(Repository.github_url == repository_url).first()
        if not repo:
            _error("No analysis found for this URL. Run `repomind analyze <url>` first.")
            raise typer.Exit(code=1)

        _section("Compile")
        _info("Loading health scores, findings, and recommendations…")

        health          = db.query(RepositoryHealth).filter(RepositoryHealth.repository_id == repo.id).first()
        findings        = db.query(Finding).filter(Finding.repository_id == repo.id).all()
        recommendations = (
            db.query(Recommendation)
            .filter(Recommendation.repository_id == repo.id)
            .order_by(Recommendation.priority_score.desc())
            .all()
        )

        _info("Rendering Markdown report…")
        md_content = generate_analysis_markdown(repo, health, findings, recommendations)

        filename  = f"analysis_{repo.owner}_{repo.name}.md"
        subfolder = f"{repo.owner}_{repo.name}"
        filepath  = save_report(md_content, filename, subfolder)

        typer.echo("")
        _ok(f"Report saved to {filepath}")
        typer.echo("")

    except Exception as e:
        logger.error(f"Report generation failed for Repository {repository_url}", exc_info=True)
        _error(f"Report generation failed: {e}")
        raise typer.Exit(code=1)
    finally:
        db.close()


@app.command()
def blueprint(
    recommendation_id: str,
    export: bool = typer.Option(False, "--export", "-e", help="Export the blueprint to a Markdown file")
) -> None:
    """Generate an implementation plan from a specific recommendation ID."""
    _cmd_header("Implementation Blueprint")

    db = SessionLocal()
    try:
        rec = db.query(Recommendation).filter(Recommendation.id == recommendation_id).first()
        if not rec:
            _error(f"Recommendation '{recommendation_id}' not found. Run `repomind analyze` to generate recommendations.")
            raise typer.Exit(code=1)

        repo        = db.query(Repository).filter(Repository.id == rec.repository_id).first()
        repo_folder = f"{repo.owner}_{repo.name}" if repo else "unknown_repo"

        _kv("Recommendation", str(rec.title))
        _kv("ID",             recommendation_id)

        _section("Generate")
        _info("Synthesizing implementation plan from linked findings…")

        repo_meta = {
            "language":  str(repo.language)  if repo and repo.language  else "Unknown",
            "framework": str(repo.framework) if repo and repo.framework else "Unknown",
        }
        blueprint_data = generate_blueprint(
            str(rec.title),
            str(rec.description),
            repo_meta,
            rec.linked_findings
        )
        save_blueprint(db, rec.id, blueprint_data)

        _section("Blueprint", color=typer.colors.MAGENTA)
        _print_blueprint(blueprint_data)

        if export:
            _section("Export")
            _info("Rendering blueprint to Markdown…")
            md_content = generate_blueprint_markdown(blueprint_data, str(rec.title))
            filename   = f"blueprint_{str(recommendation_id)[:8]}.md"
            filepath   = save_report(md_content, filename, repo_folder)
            _ok(f"Blueprint saved to {filepath}")
            typer.echo("")

    except Exception as e:
        logger.error(f"Blueprint generation failed for recommendation {recommendation_id}", exc_info=True)
        _error(f"Blueprint generation failed: {e}")
        raise typer.Exit(code=1)
    finally:
        db.close()


@app.command()
def version() -> None:
    """Display the current application version."""
    typer.echo("RepoMind AI v0.1.0")


if __name__ == "__main__":
    app()