from typing import List, Dict, Any
from sqlalchemy.orm import Session
from repomind.models import Repository, Embedding, RepositoryHealth, Finding, Recommendation, Blueprint

def save_repository(db: Session, meta: Dict[str, str], url: str) -> Repository:
    """Save repository metadata to the database."""
    # Check if we already analyzed this repo to avoid duplicates
    existing_repo = db.query(Repository).filter(Repository.github_url == url).first()
    if existing_repo:
        return existing_repo 

    repo = Repository(
        name=meta["name"],
        owner=meta["owner"],
        github_url=url,
        local_path=meta["local_path"],
        # --- PHASE 1 FIX: Capture language & framework ---
        language=meta.get("language"),
        framework=meta.get("framework")
    )

    db.add(repo)
    db.commit()
    db.refresh(repo)
    return repo 

def save_embeddings(
    db: Session, 
    repo_id: Any, 
    file_path: str, 
    chunks: List[str], 
    vectors: List[List[float]]
) -> None:
    """Save text chunks and their vector embeddings to the database."""
    # Delete old embeddings for this specific file if we are re-analyzing
    db.query(Embedding).filter(
        Embedding.repository_id == repo_id,
        Embedding.file_path == file_path
    ).delete()
    
    embeddings_to_save = []
    for i, (chunk, vector) in enumerate(zip(chunks, vectors)):
        emb = Embedding(
            repository_id=repo_id,
            file_path=file_path,
            chunk_index=i,
            content=chunk,
            embedding=vector
        )
        embeddings_to_save.append(emb)
    
    db.add_all(embeddings_to_save)
    db.commit()


def save_health_scores(db: Session, repo_id: Any, scores: Dict[str, int]) -> None:
    """Save the generated health scores to the database."""
    # Remove existing scores if re-analyzing
    db.query(RepositoryHealth).filter(RepositoryHealth.repository_id == repo_id).delete()
    
    health_record = RepositoryHealth(
        repository_id=repo_id,
        architecture_score=scores.get("architecture_score", 0),
        testing_score=scores.get("testing_score", 0),
        security_score=scores.get("security_score", 0),
        documentation_score=scores.get("documentation_score", 0),
        scalability_score=scores.get("scalability_score", 0),
        maturity_score=scores.get("maturity_score", 0),
    )
    db.add(health_record)
    db.commit()


def save_findings(db: Session, repo_id: Any, findings_data: list[Dict[str, Any]]) -> None:
    """Save detected issues and deterministic AST metrics to the database."""
    # Clear out old findings if re-analyzing
    db.query(Finding).filter(Finding.repository_id == repo_id).delete()
    
    findings_to_save = []
    for issue in findings_data:
        finding = Finding(
            repository_id=repo_id,
            title=issue.get("title", "Unknown Issue"),
            category=issue.get("category", "General"),
            severity=issue.get("severity", "Medium"),
            description=issue.get("description", "No description provided."),
            # --- Capture the AST Math ---
            file_path=issue.get("file_path"),
            function_name=issue.get("function_name"),
            complexity=issue.get("complexity"),
            nesting=issue.get("nesting")
        )
        findings_to_save.append(finding)
        
    if findings_to_save:
        db.add_all(findings_to_save)
        db.commit()


def save_recommendations(
    db: Session, 
    repo_id: Any, 
    recommendations_data: list[dict[str, Any]],
    db_findings: list[Finding] | None = None  # <-- Explicitly allow None
) -> list[Recommendation]:
    """Save prioritized recommendations and link them to their AST findings."""
    
    existing_recs = db.query(Recommendation).filter(Recommendation.repository_id == repo_id).all()
    rec_ids = [r.id for r in existing_recs]
    
    if rec_ids:
        db.query(Blueprint).filter(Blueprint.recommendation_id.in_(rec_ids)).delete(synchronize_session=False)
        db.query(Recommendation).filter(Recommendation.repository_id == repo_id).delete(synchronize_session=False)
    
    if not recommendations_data:
        return []
        
    sorted_recs = sorted(recommendations_data, key=lambda x: x.get("priority_score", 0), reverse=True)
    
    saved_recs = []
    for i, rec in enumerate(sorted_recs):
        recommendation = Recommendation(
            repository_id=repo_id,
            title=rec.get("title", "Improvement"),
            description=rec.get("description", ""),
            impact_score=rec.get("impact_score", 0.0),
            effort_score=rec.get("effort_score", 0.0),
            risk_score=rec.get("risk_score", 0.0),
            cost_score=rec.get("cost_score", 0.0),
            priority_score=rec.get("priority_score", 0.0),
            is_recommended=(i == 0)
        )
        
        # --- PHASE 1 FIX: Match LLM IDs to Database Objects ---
        if db_findings:
            for finding_id in rec.get("linked_finding_ids", []):
                # Find the actual database object that matches the UUID the AI returned
                matched_finding = next((f for f in db_findings if str(f.id) == finding_id), None)
                if matched_finding:
                    recommendation.linked_findings.append(matched_finding)
                
        saved_recs.append(recommendation)
        
    db.add_all(saved_recs)
    db.commit()
    
    for r in saved_recs:
        db.refresh(r)
    return saved_recs


def save_blueprint(db: Session, recommendation_id: Any, blueprint_data: Dict[str, Any]) -> Blueprint:
    """Save the generated blueprint to the database."""
    # Delete existing if regenerating
    db.query(Blueprint).filter(Blueprint.recommendation_id == recommendation_id).delete()
    
    blueprint = Blueprint(
        recommendation_id=recommendation_id,
        content=blueprint_data
    )
    db.add(blueprint)
    db.commit()
    db.refresh(blueprint)
    return blueprint