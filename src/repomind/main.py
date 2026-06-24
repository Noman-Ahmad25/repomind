import typer, os, time
from pathlib import Path
from dotenv import load_dotenv
from repomind.loader import clone_repository, validate_github_url
from repomind.parser import analyze_repository_structure
from repomind.embedding import chunk_text, generate_embeddings
from repomind.database import SessionLocal
from repomind.models import Repository, Embedding, RepositoryHealth
from repomind.ai import detect_repository_stage, analyze_repository_health, detect_repository_issues, generate_recommendations, generate_blueprint, generate_ai_explanation
from repomind.storage import save_repository, save_embeddings, save_health_scores, save_findings, save_recommendations, save_blueprint
from repomind.reporting import generate_analysis_markdown, generate_blueprint_markdown, save_report
from repomind.models import Repository, RepositoryHealth, Finding, Recommendation, Blueprint
from repomind.analyzer import get_function_registry, get_code_slice
from repomind.validator import load_rules, evaluate_function
from repomind.prioritizer import get_top_issues
from repomind.analyzer_metrics import analyze_function_body


# Load environment variables from .env file
load_dotenv()

app = typer.Typer(
    help="RepoMind AI - Repository Intelligence Platform",
    add_completion=False,
)

@app.command()
def analyze(repository_url: str) -> None:
    """Analyze a repository and generate recommendations."""
    typer.echo(f"Initializing analysis for: {repository_url}")
    
    if not validate_github_url(repository_url):
        typer.secho("Error: Invalid GitHub URL.", fg=typer.colors.RED)
        raise typer.Exit(code=1)
        
    typer.echo("Cloning repository locally (this may take a moment)...")
    db = SessionLocal()
    try:
        meta = clone_repository(repository_url)
        typer.secho("✓ Repository cloned successfully!", fg=typer.colors.GREEN)
        
        # 1. Save Repository to Database
        repo_record = save_repository(db, meta, repository_url)
        typer.echo(f"Database Record ID: {repo_record.id}")
        
        # 2. Parse Architecture
        typer.echo("Parsing repository architecture...")
        structure = analyze_repository_structure(meta["local_path"])
        
        typer.secho("\n--- Repository Metadata ---", fg=typer.colors.CYAN)
        typer.echo(f"Files Parsed: {structure['files']}")
        typer.echo(f"Classes Found: {structure['classes']}")
        typer.echo(f"Functions Found: {structure['functions']}")
        typer.echo("---------------------------\n")

        # 3. Generate and Save Embeddings (Recursive for all source files)
        # First, check if we already have data for this repository
        existing_vectors = db.query(Embedding).filter(Embedding.repository_id == repo_record.id).count()
        
        if existing_vectors > 0:
            typer.secho(f"✓ Found {existing_vectors} existing vectors in Postgres. Skipping re-embedding!", fg=typer.colors.YELLOW)
        else:
            typer.echo("Generating embeddings for repository source files...")
            repo_root = Path(meta["local_path"])
            extensions = ['*.py', '*.js', '*.ts', '*.md']
            
            files_to_process = []
            for ext in extensions:
                for file_path in repo_root.rglob(ext):
                    if 'venv' in str(file_path) or 'node_modules' in str(file_path) or '.git' in str(file_path):
                        continue
                    files_to_process.append(file_path)
            
            total_vectors = 0
            with typer.progressbar(files_to_process, label="Vectorizing codebase") as progress:
                for file_path in progress:
                    try:
                        content = file_path.read_text(encoding="utf-8")
                        chunks = chunk_text(content)
                        if chunks:
                            vectors = generate_embeddings(chunks)
                            save_embeddings(db, repo_record.id, str(file_path.relative_to(repo_root)), chunks, vectors)
                            total_vectors += len(chunks)
                    except Exception:
                        pass
                        
            typer.secho(f"\n✓ Saved {total_vectors} vectors to Postgres (pgvector)!", fg=typer.colors.GREEN)

        # 4. AI Stage Detection
        typer.echo("Executing AI Stage Detection via Gemini 2.5 Pro...")
        analysis = detect_repository_stage(meta, structure)
        
        typer.secho("\n--- Intelligence Report ---", fg=typer.colors.MAGENTA)
        typer.echo(f"Detected Stage: {analysis['stage']}")
        typer.echo(f"Confidence Score: {analysis['confidence']}%")
        typer.echo(f"Architectural Reasoning: {analysis['reasoning']}")
        typer.echo("---------------------------\n")
        
        # 5. Health Analysis
        typer.echo("Executing Health Analysis...")
        health_scores = analyze_repository_health(meta, structure, analysis['stage'])
        save_health_scores(db, repo_record.id, health_scores)
        
        typer.secho("\n--- Health Report ---", fg=typer.colors.BLUE)
        typer.echo(f"Architecture:  {health_scores['architecture_score']}/100")
        typer.echo(f"Testing:       {health_scores['testing_score']}/100")
        typer.echo(f"Security:      {health_scores['security_score']}/100")
        typer.echo(f"Documentation: {health_scores['documentation_score']}/100")
        typer.echo(f"Scalability:   {health_scores['scalability_score']}/100")
        typer.secho(f"Overall Score: {health_scores['maturity_score']}/100", bold=True)
        typer.echo("---------------------------\n")

        # 6. Issue Detection
        typer.echo("Auditing repository for code-level issues...")
        findings = detect_repository_issues(db, repo_record.id, meta, structure, analysis['stage'], health_scores)
        save_findings(db, repo_record.id, findings)
        
        typer.secho("\n--- Discovered Issues ---", fg=typer.colors.RED)
        if not findings:
            typer.echo("No significant issues detected.")
        else:
            for i, issue in enumerate(findings, 1):
                # DEFENSIVE PARSING: Use .get() with safe defaults
                severity = issue.get('severity', 'Medium')
                category = issue.get('category', 'General')
                title = issue.get('title', 'Unknown Issue')
                desc = issue.get('description', 'No description provided.')
                
                severity_color = typer.colors.RED if severity == 'High' else typer.colors.YELLOW
                
                typer.secho(f"{i}. [{category}] {title} (Severity: {severity})", fg=severity_color)
                typer.echo(f"   {desc}\n")
        typer.echo("---------------------------\n")


        # 7. Prioritized Recommendations
        typer.echo("Generating prioritized engineering recommendations...")
        raw_recs = generate_recommendations(meta, analysis['stage'], health_scores, findings)
        saved_recs = save_recommendations(db, repo_record.id, raw_recs)
        
        typer.secho("\n--- Engineering Recommendations ---", fg=typer.colors.GREEN)
        if not saved_recs:
            typer.echo("No recommendations generated.")
        else:
            for rec in saved_recs:
                if rec.is_recommended:
                    typer.secho(f"★ RECOMMENDED NEXT ACTION ★", fg=typer.colors.YELLOW, bold=True)
                
                typer.secho(f"ID: {rec.id}", fg=typer.colors.CYAN)
                typer.secho(f"Title: {rec.title}", bold=True)
                typer.echo(f"Priority: {rec.priority_score}/10 (Impact: {rec.impact_score} | Effort: {rec.effort_score})")
                typer.echo(f"Why: {rec.description}\n")
        typer.echo("---------------------------\n")

        
       
            
    except Exception as e:
        typer.secho(f"Error analyzing repository: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    finally:
        db.close()


@app.command()
def audit(repository_url: str) -> None:

    # Check for existing repo in DB to avoid re-cloning
    db = SessionLocal()
    repo = db.query(Repository).filter(Repository.github_url == repository_url).first()
    
    if not repo or not Path(repo.local_path).exists():
        typer.echo("Repo not found in local cache. Running analyze first...")
        analyze(repository_url) # Re-use established ingestion logic
        repo = db.query(Repository).filter(Repository.github_url == repository_url).first()
    
    registry = []
    repo_path = Path(repo.local_path)
    typer.echo(f"Scanning repository files in: {repo_path}")
    
    for py_file in repo_path.rglob("*.py"):
        # Skip virtual environments and hidden folders
        if 'venv' in str(py_file) or '.git' in str(py_file) or 'node_modules' in str(py_file):
            continue
            
        try:
            # Get the registry for this specific file and add it to the master list
            file_registry = get_function_registry(str(py_file))
            registry.extend(file_registry)
        except Exception as e:
            continue # Skip unparseable files
            
    typer.echo(f"Discovered {len(registry)} functions. Calculating metrics...")
    
    # ... proceed with audit logic ...
    
    # 2. Metrics & Smell Detection (Phases 2 & 3)
    all_findings = []
    rules = load_rules() # Load rules.json
    
    for func in registry:
        # Extract code slice using start/end lines
        code_slice = get_code_slice(func['file'], func['start_line'], func['end_line'])
        metrics = analyze_function_body(code_slice)
        
        # Check against local rules.json
        findings = evaluate_function(metrics, rules)
        if findings:
            all_findings.append({**func, **metrics, "findings": findings})
            
    # 3. Prioritization (Phase 8)
    top_issues = get_top_issues(all_findings, limit=5)
    
    # 4. Synthesis (Phase 9)
    typer.secho("\n--- High-Impact Findings (Manual Audit) ---", fg=typer.colors.RED)
    for issue in top_issues:
        typer.echo(f"Target: {issue['function']} in {issue['file']}")
        typer.echo(f"Metrics: Complexity {issue['complexity']}, Nesting {issue['nesting']}")
        
        explanation = generate_ai_explanation(issue) 
        typer.echo(f"Refactor Logic: {explanation}\n")
        
        # Add a 2-second pause between AI calls to respect API rate limits
        time.sleep(2)


# ... (keep report, blueprint, and version commands the same as before) ...
@app.command()
def report(repository_url: str) -> None:
    """Generate a markdown report for an analyzed repository."""
    db = SessionLocal()
    try:
        typer.echo(f"Locating analysis data for: {repository_url}...")
        
        repo = db.query(Repository).filter(Repository.github_url == repository_url).first()
        if not repo:
            typer.secho("Error: Repository not found. Run 'analyze' first.", fg=typer.colors.RED)
            raise typer.Exit(code=1)
            
        health = db.query(RepositoryHealth).filter(RepositoryHealth.repository_id == repo.id).first()
        findings = db.query(Finding).filter(Finding.repository_id == repo.id).all()
        
        # Sort recommendations by priority score
        recommendations = db.query(Recommendation).filter(Recommendation.repository_id == repo.id).order_by(Recommendation.priority_score.desc()).all()
        
        typer.echo("Generating Markdown report...")
        md_content = generate_analysis_markdown(repo, health, findings, recommendations)
        
        filename = f"analysis_{repo.owner}_{repo.name}.md"
        subfolder = f"{repo.owner}_{repo.name}"
        filepath = save_report(md_content, filename, subfolder)
        
        typer.secho(f"✓ Report successfully exported to: {filepath}", fg=typer.colors.GREEN, bold=True)
        
    except Exception as e:
        typer.secho(f"Error generating report: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    finally:
        db.close()


@app.command()
def blueprint(recommendation_id: str, export: bool = typer.Option(False, "--export", "-e", help="Export the blueprint to a Markdown file")) -> None:
    """Generate an implementation plan from a specific recommendation ID."""
    db = SessionLocal()
    try:

        # 1. Verify the recommendation exists
        rec = db.query(Recommendation).filter(Recommendation.id == recommendation_id).first()
        if not rec:
            typer.secho(f"Error: Recommendation ID '{recommendation_id}' not found.", fg=typer.colors.RED)
            raise typer.Exit(code=1)
            
        # Get the associated repository to organize the export folder
        repo = db.query(Repository).filter(Repository.id == rec.repository_id).first()
        repo_folder = f"{repo.owner}_{repo.name}" if repo else "unknown_repo"
        
        typer.echo(f"Generating blueprint for: {rec.title}...")

        # 2. Generate and Save Blueprint
        blueprint_data = generate_blueprint(str(rec.title), str(rec.description))
        saved_bp = save_blueprint(db, rec.id, blueprint_data)
        
        # 3. Display the Output
        typer.secho("\n=== IMPLEMENTATION BLUEPRINT ===", fg=typer.colors.MAGENTA, bold=True)
        typer.echo(f"Goal: {blueprint_data.get('goal')}\n")
        
        typer.secho("Files to Create:", bold=True)
        for f in blueprint_data.get('files_to_create', []): typer.echo(f"  + {f}")
        
        typer.secho("\nImplementation Steps:", bold=True)
        for i, step in enumerate(blueprint_data.get('implementation_steps', []), 1):
            typer.echo(f"  {i}. {step}")
            
        typer.echo(f"\nEstimated Effort: {blueprint_data.get('estimated_effort')}")
        typer.echo("================================\n")

        if export:
            typer.echo("\nExporting blueprint to Markdown...")
            md_content = generate_blueprint_markdown(blueprint_data, str(rec.title))
            filename = f"blueprint_{str(recommendation_id)[:8]}.md"
            filepath = save_report(md_content, filename, repo_folder)
            typer.secho(f"✓ Blueprint successfully exported to: {filepath}", fg=typer.colors.GREEN, bold=True)

    except Exception as e:
        typer.secho(f"Error generating blueprint: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    finally:
        db.close()


@app.command()
def version() -> None:
    """Display the current application version."""
    typer.echo("RepoMind AI v0.1.0")

if __name__ == "__main__":
    app()
