import typer
import time
from pathlib import Path
from dotenv import load_dotenv

import logging

# Core Pipeline
from repomind.loader import clone_repository, validate_github_url
from repomind.parser import analyze_repository_structure


# Database & Storage
from repomind.database import SessionLocal
from repomind.models import Repository, Embedding, RepositoryHealth, Finding, Recommendation
from repomind.storage import save_repository, save_health_scores, save_findings, save_recommendations, save_blueprint

# Intelligence & Math
from repomind.analyzer import run_deterministic_audit, calculate_deterministic_health, classify_maturity
from repomind.prioritizer import get_top_issues
from repomind.ai import detect_repository_stage, detect_repository_issues, generate_recommendations, generate_blueprint

# Reporting
from repomind.reporting import generate_analysis_markdown, generate_blueprint_markdown, save_report


# Load environment variables from .env file
load_dotenv()

# --- ADD THIS LOGGING CONFIGURATION ---
logging.basicConfig(
    filename="repomind.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(module)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)
# --------------------------------------

app = typer.Typer(
    help="RepoMind AI - Repository Intelligence Platform",
    add_completion=False,
)

@app.command()
def analyze(
    repository_url: str,
    rules: str = typer.Option("rules.json", "--rules", "-r", help="Path to custom rules configuration file")
) -> None:
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
        # Directly beneath repo_record = save_repository(db, meta, repository_url)
        if repo_record is None:
            typer.secho("Error: Failed to register repository in the database.", fg=typer.colors.RED)
            raise typer.Exit(code=1)

        typer.echo(f"Database Record ID: {repo_record.id}")
        
        # 2. Parse Architecture
        typer.echo("Parsing repository architecture...")
        structure = analyze_repository_structure(meta["local_path"])
        
        typer.secho("\n--- Repository Metadata ---", fg=typer.colors.CYAN)
        typer.echo(f"Files Parsed: {structure['files']}")
        typer.echo(f"Classes Found: {structure['classes']}")
        typer.echo(f"Functions Found: {structure['functions']}")
        typer.echo("---------------------------\n")


       # ---------------------------------------------------------
        # --- PHASE 6: THE PIPELINE FLIP (Evidence First) ---
        # ---------------------------------------------------------

        # 4. Deterministic AST Audit
        typer.echo(f"Executing deterministic AST code audit using rules from {rules}...")
        raw_audit_findings = run_deterministic_audit(meta["local_path"], rules_path=rules)
        
        # 5. Deterministic Repository Stage Classification
        typer.echo("Classifying repository maturity...")
        analysis = classify_maturity(structure)
        
        # 6. Evidence-Based Health Scores (No AI used here!)
        typer.echo("Calculating deterministic health scores...")
        health_scores = calculate_deterministic_health(structure, raw_audit_findings)
        save_health_scores(db, repo_record.id, health_scores)
        
        typer.secho("\n--- Health & Intelligence Report (Evidence-Based) ---", fg=typer.colors.BLUE)
        typer.echo(f"Detected Stage: {analysis.get('stage', 'Unknown')}")
        typer.echo(f"Architecture:  {health_scores['architecture_score']}/100")
        typer.echo(f"Testing:       {health_scores['testing_score']}/100")
        typer.echo(f"Security:      {health_scores['security_score']}/100")
        typer.echo(f"Documentation: {health_scores['documentation_score']}/100")
        typer.echo(f"Scalability:   {health_scores['scalability_score']}/100")
        typer.secho(f"Overall Score: {health_scores['maturity_score']}/100", bold=True)
        typer.echo("---------------------------\n")

       # 7. AI Synthesis and Display
        typer.echo("Synthesizing code-level issues via AI...")
        top_audit_findings = get_top_issues(raw_audit_findings, limit=5)
        findings = detect_repository_issues(meta, top_audit_findings)
        
        save_findings(db, repo_record.id, findings)
        
        typer.secho("\n--- Discovered Issues (Evidence-Based) ---", fg=typer.colors.RED)
        if not findings:
            typer.echo("No significant issues detected.")
        else:
            for i, issue in enumerate(findings, 1):
                file_path = issue.get('file_path', issue.get('file', 'Unknown'))
                func_name = issue.get('function_name', issue.get('function', 'Unknown'))
                
                # Check for line numbers existence
                start = issue.get('start_line')
                end = issue.get('end_line')
                
                # Construct line info string only if data exists
                line_info = f" (Lines {start}-{end})" if (start and end) else ""
                
                typer.secho(f"{i}. [{issue.get('category', 'Technical Debt')}] {issue.get('title', 'Untitled')}", fg=typer.colors.RED)
                typer.echo(f"   {file_path} -> {func_name}{line_info}")
                typer.echo(f"   {issue.get('description', 'No description provided.')}\n")
        typer.echo("---------------------------\n")
        


        # 8. Prioritized Recommendations
        typer.echo("Generating prioritized engineering recommendations...")
        
        # Fetch the finding objects from the DB so we can enrich them
        saved_findings_objects = db.query(Finding).filter(Finding.repository_id == repo_record.id).all()
        
        # Pass them to the newly updated AI prompt
        raw_recs = generate_recommendations(meta, analysis['stage'], saved_findings_objects)
        
        # Save and map the links
        saved_recs = save_recommendations(db, repo_record.id, raw_recs, saved_findings_objects)
        
        typer.secho("\n--- Engineering Recommendations ---", fg=typer.colors.GREEN)
        if not saved_recs:
            typer.echo("No recommendations generated.")
        else:
            for rec in saved_recs:
                if rec.is_recommended:
                    typer.secho("★ RECOMMENDED NEXT ACTION ★", fg=typer.colors.YELLOW, bold=True)
                
                typer.secho(f"ID: {rec.id}", fg=typer.colors.CYAN)
                typer.secho(f"Title: {rec.title}", bold=True)
                typer.echo(f"Priority: {rec.priority_score}/10 (Impact: {rec.impact_score} | Effort: {rec.effort_score})")
                typer.echo(f"Why: {rec.description}\n")
        typer.echo("---------------------------\n")

        
       
            
    except Exception as e:
        # FIX: Log the full stack trace to the file, but keep the terminal clean
        logger.error(f"Analysis failed for {repository_url}", exc_info=True)
        typer.secho(f"Error analyzing repository: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    finally:
        db.close()


@app.command()
@app.command()
def audit(
    repository_url: str,
    rules: str = typer.Option("rules.json", "--rules", "-r", help="Path to custom rules configuration file")
) -> None:
    """Run a fast, offline, deterministic AST audit without AI synthesis."""
    db = SessionLocal()
    try:
        # 1. Resolve Local Path
        repo = db.query(Repository).filter(Repository.github_url == repository_url).first()
        
        if not repo or not Path(repo.local_path).exists():
            typer.echo("Repo not found in local cache. Cloning now...")
            from repomind.loader import clone_repository
            meta = clone_repository(repository_url)
            local_path = meta["local_path"]
        else:
            # --- THE FIX: Cast the SQLAlchemy column to a string ---
            local_path = str(repo.local_path)
            
        # 2. Run the Engine
        typer.echo(f"Executing deterministic AST code audit on: {local_path} using {rules}...")
        start_time = time.time()
        raw_audit_findings = run_deterministic_audit(local_path, rules_path=rules)
        execution_time = time.time() - start_time
        
        # 3. Output the Math (No AI, just facts)
        if not raw_audit_findings:
            typer.secho(f"✓ No critical issues found in {execution_time:.2f} seconds.", fg=typer.colors.GREEN)
            return
            
        # Sort by worst complexity
        sorted_findings = sorted(raw_audit_findings, key=lambda x: x.get('complexity', 0), reverse=True)
        
        typer.secho(f"\n=== RAW AST AUDIT ({len(sorted_findings)} issues found in {execution_time:.2f}s) ===", fg=typer.colors.RED, bold=True)
        
        # Display the top 10 worst offenders
        for i, issue in enumerate(sorted_findings[:10], 1):
            typer.secho(f"{i}. {issue['function']} (File: {issue['file']})", fg=typer.colors.CYAN, bold=True)
            typer.echo(f"   Complexity: {issue['complexity']} | Nesting: {issue['nesting']}")
            violations = [f.get('type') for f in issue.get('findings', [])]
            typer.secho(f"   Violations: {', '.join(violations)}\n", fg=typer.colors.YELLOW)
            
        if len(sorted_findings) > 10:
            typer.echo(f"...and {len(sorted_findings) - 10} more issues.")
            typer.secho("\nTip: Run `repomind analyze` to have the AI synthesize these findings into actionable refactoring blueprints.", fg=typer.colors.MAGENTA)
            
    except Exception as e:
        logger.error(f"Audit failed for recommendation {repository_url}", exc_info=True)
        typer.secho(f"Error during audit: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    finally:
        db.close()


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
        logger.error(f"Report generation failed for Repository {repository_url}", exc_info=True)
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
        # Ensure we pass the language/framework constraints and the hard evidence!
        repo_meta = {
            "language": str(repo.language) if repo and repo.language else "Unknown",
            "framework": str(repo.framework) if repo and repo.framework else "Unknown"
        }
        blueprint_data = generate_blueprint(
            str(rec.title), 
            str(rec.description), 
            repo_meta, 
            rec.linked_findings # Pass the joined DB evidence!
        )
        save_blueprint(db, rec.id, blueprint_data)
        
        # 3. Display the Output
        typer.secho("\n=== IMPLEMENTATION BLUEPRINT ===", fg=typer.colors.MAGENTA, bold=True)
        typer.echo(f"Goal: {blueprint_data.get('goal')}\n")
        
        typer.secho("Files to Create:", bold=True)
        for f in blueprint_data.get('files_to_create', []): 
            typer.echo(f"  + {f}")
        
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
        logger.error(f"Blueprint generation failed for recommendation {recommendation_id}", exc_info=True)
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
