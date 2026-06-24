import json
from pathlib import Path
from typing import Any

def ensure_reports_dir(subfolder: str = "") -> Path:
    """Ensure the reports directory and specific subfolder exist."""
    reports_dir = Path("reports")
    if subfolder:
        reports_dir = reports_dir / subfolder
        
    # parents=True ensures it creates both 'reports' and 'reports/subfolder' if missing
    reports_dir.mkdir(parents=True, exist_ok=True)
    return reports_dir

def generate_analysis_markdown(repo: Any, health: Any, findings: Any, recommendations: Any) -> str:
    """Format the repository analysis into a Markdown document."""
    md = f"# Repository Intelligence Report: {repo.owner}/{repo.name}\n\n"
    md += f"**Repository:** {repo.github_url}\n"
    md += f"**Generated At:** {repo.updated_at.strftime('%Y-%m-%d %H:%M:%S')} UTC\n\n"
    
    md += "## Health Analysis\n\n"
    if health:
        md += f"- **Overall Maturity:** {health.maturity_score}/100\n"
        md += f"- **Architecture:** {health.architecture_score}/100\n"
        md += f"- **Testing:** {health.testing_score}/100\n"
        md += f"- **Security:** {health.security_score}/100\n"
        md += f"- **Documentation:** {health.documentation_score}/100\n"
        md += f"- **Scalability:** {health.scalability_score}/100\n\n"
        
    md += "## Discovered Issues\n\n"
    if findings:
        for i, issue in enumerate(findings, 1):
            md += f"### {i}. [{issue.category}] {issue.title}\n"
            md += f"**Severity:** {issue.severity}\n\n"
            md += f"{issue.description}\n\n"
    else:
        md += "No significant issues detected.\n\n"
        
    md += "## Prioritized Recommendations\n\n"
    if recommendations:
        for rec in recommendations:
            if rec.is_recommended:
                md += f"### ★ RECOMMENDED NEXT ACTION: {rec.title}\n"
            else:
                md += f"### {rec.title}\n"
            md += f"**Priority:** {rec.priority_score}/10 (Impact: {rec.impact_score} | Effort: {rec.effort_score})\n\n"
            md += f"{rec.description}\n\n"
            md += f"*(To generate a blueprint for this recommendation, run: `repomind blueprint {rec.id}`)*\n\n"
            md += "---\n\n"
            
    return md

def generate_blueprint_markdown(blueprint_data: dict[str, Any], rec_title: str) -> str:
    """Format the blueprint JSON into a Markdown document."""
    md = f"# Implementation Blueprint: {rec_title}\n\n"
    md += f"**Goal:** {blueprint_data.get('goal')}\n\n"
    
    md += "## Files to Create\n"
    for f in blueprint_data.get('files_to_create', []):
        md += f"- `{f}`\n"
    md += "\n"
    
    md += "## Files to Modify\n"
    for f in blueprint_data.get('files_to_modify', []):
        md += f"- `{f}`\n"
    md += "\n"
        
    md += "## Implementation Steps\n\n"
    for step in blueprint_data.get('implementation_steps', []):
        md += f"{step}\n\n"
        
    md += f"**Estimated Effort:** {blueprint_data.get('estimated_effort')}\n"
    return md

def save_report(content: str, filename: str, subfolder: str = "") -> str:
    """Save the markdown content to the specific reports directory."""
    reports_dir = ensure_reports_dir(subfolder)
    filepath = reports_dir / filename
    filepath.write_text(content, encoding="utf-8")
    return str(filepath)