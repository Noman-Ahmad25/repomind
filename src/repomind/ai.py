import os, time
import json
from typing import Dict, Any
from google import genai 
from google.genai import types 
from sqlalchemy.orm import Session
from uuid import UUID 
from repomind.embedding import get_relevant_chunks


def detect_repository_stage(repo_meta: Dict[str, str], structure: Dict[str, int]) -> Dict[str, Any]:
    """Analyze repository metadata to determine its maturity stage."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is missing.")
        
    client = genai.Client(api_key=api_key)
    
    # Using flash temporarily to bypass the strict free-tier limits on Pro
    model_name = 'gemini-3.1-flash-lite'
    
    rules = """
    You are an expert Software Architect. Evaluate the repository architecture metrics and classify its maturity stage into EXACTLY ONE of the following:
    - Idea: Minimal code, mostly documentation.
    - Prototype: Basic structure, functional but lacks extensive architecture.
    - MVP: Core features implemented, moderate file/function count.
    - Growth: Scaling architecture, high file count, complex module separation.
    - Mature: Enterprise-ready, massive codebase, highly optimized.
    """
    
    prompt = f"""
    {rules}
    
    Repository Data:
    - Name: {repo_meta['name']}
    - Total Files: {structure['files']}
    - Total Classes: {structure['classes']}
    - Total Functions: {structure['functions']}
    
    Respond ONLY with a valid JSON object matching this exact schema:
    {{
        "stage": "Prototype",
        "confidence": 85,
        "reasoning": "Brief architectural justification based strictly on the provided numbers."
    }}
    """
    
    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.1
        )
    )
    
    if response.text:
        return dict(json.loads(response.text))
    
    return {"stage": "Unknown", "confidence": 0, "reasoning": "API returned empty response."}


def analyze_repository_health(repo_meta: Dict[str, str], structure: Dict[str, int], stage: str) -> Dict[str, int]:
    """Evaluate repository health scores."""
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    prompt = f"""
    You are an expert Software Auditor. Evaluate the repository health based on the following metadata.
    
    Repository: {repo_meta['name']}
    Detected Stage: {stage}
    Total Files: {structure['files']}
    Total Classes: {structure['classes']}
    Total Functions: {structure['functions']}
    
    Estimate the health scores (0-100) for this repository based on its stage and size.
    Respond ONLY with a valid JSON object matching this exact schema:
    {{
        "architecture_score": 85,
        "testing_score": 60,
        "security_score": 75,
        "documentation_score": 80,
        "scalability_score": 70,
        "maturity_score": 74
    }}
    """
    
    response = client.models.generate_content(
        model='gemini-3.1-flash-lite',
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.1
        )
    )
    
    if response.text:
        return dict(json.loads(response.text))
        
    # Fallback in case of failure
    return {k: 0 for k in ["architecture_score", "testing_score", "security_score", "documentation_score", "scalability_score", "maturity_score"]}




def detect_repository_issues(
    db: Session, 
    repo_id: UUID,
    repo_meta: Dict[str, str], 
    structure: Dict[str, int], 
    stage: str, 
    health_scores: Dict[str, int]
) -> list[Dict[str, str]]:
    
    # Corrected: Combined context and audit instructions into a single variable
    chunks = get_relevant_chunks(db, repo_id, "complex logic, deep nesting, missing error handling", limit=3)
    code_context = "\n\n".join([f"File: {c.file_path}\nCode: {c.content}" for c in chunks])
    
    prompt = f"""
    You are a Senior Staff Auditor. Analyze the repository metrics and code evidence.
    
    [METRICS] {json.dumps(health_scores)}
    [CODE EVIDENCE] {code_context}
    
    Identify 3-5 issues. Cite files. Respond ONLY in JSON.
    """
    
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    response = client.models.generate_content(
        model='gemini-3.1-flash-lite',
        contents=prompt,
        config=types.GenerateContentConfig(response_mime_type="application/json", temperature=0.2)
    )
    return list(json.loads(response.text)) if response.text else []



def generate_recommendations(
    repo_meta: Dict[str, str], 
    stage: str, 
    health_scores: Dict[str, int], 
    findings: list[Dict[str, str]]
) -> list[Dict[str, Any]]:
    """Generate and prioritize engineering recommendations."""
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    prompt = f"""
    You are a Lead Staff Engineer. Analyze this repository and provide actionable engineering recommendations.
    
    Repository: {repo_meta['name']}
    Stage: {stage}
    Health Scores: {json.dumps(health_scores)}
    Discovered Issues: {json.dumps(findings)}
    
    Task:
    1. Address the most critical "Discovered Issues" with concrete solutions.
    2. Discover and recommend 1 or 2 missing features or capabilities appropriate for a "{stage}" stage repository (e.g., CI/CD pipelines, Search, Analytics, Audit Logs, Caching).
    3. Score every recommendation from 1.0 to 10.0 for Impact, Effort, Risk, and Cost.
    4. Calculate a 'priority_score' (out of 10.0). High impact and low effort should yield a high priority score.
    
    Respond ONLY with a valid JSON array of objects matching this exact schema:
    [
        {{
            "title": "Implement Integration Test Suite",
            "description": "Establish a core integration testing pipeline to address the low testing coverage and prevent regressions.",
            "impact_score": 9.0,
            "effort_score": 5.0,
            "risk_score": 2.0,
            "cost_score": 3.0,
            "priority_score": 8.5
        }}
    ]
    """
    
    response = client.models.generate_content(
        model='gemini-3.1-flash-lite',
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.2
        )
    )
    
    if response.text:
        return list(json.loads(response.text))
        
    return []

def generate_blueprint(recommendation_title: str, recommendation_desc: str) -> Dict[str, Any]:
    """Generate a step-by-step implementation blueprint."""
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    prompt = f"""
    You are a Senior Staff Software Engineer. Create a detailed implementation blueprint for the following engineering task:
    
    Task: {recommendation_title}
    Context: {recommendation_desc}
    
    Respond ONLY with a valid JSON object matching this exact schema:
    {{
        "goal": "Clear statement of what will be achieved.",
        "architecture_changes": ["List of high-level changes"],
        "files_to_create": ["List of new file paths"],
        "files_to_modify": ["List of existing files to change"],
        "database_changes": ["List of schema changes or 'None'"],
        "api_changes": ["List of endpoint changes or 'None'"],
        "testing_requirements": ["Specific tests to write"],
        "estimated_effort": "e.g., 2 weeks, 3 days",
        "implementation_steps": [
            "Step 1: Detailed action...",
            "Step 2: Detailed action..."
        ]
    }}
    """
    
    response = client.models.generate_content(
        model='gemini-3.1-flash-lite',
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.1
        )
    )
    
    if response.text:
        return dict(json.loads(response.text))
        
    return {}


def generate_ai_explanation(issue: dict) -> str:
    """
    Synthesize pre-discovered findings into actionable engineering advice.
    Includes exponential backoff for API rate limits (503 errors).
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    finding_types = [f.get("type", "UNKNOWN") for f in issue.get('findings', [])]
    
    prompt = f"""
    You are a Senior Staff Engineer. I have performed a static analysis on this function:
    
    Function: {issue['function']}
    File: {issue['file']}
    Metrics: Complexity={issue['complexity']}, Nesting={issue['nesting']}
    Detected Issues: {', '.join(finding_types)}
    
    Task:
    1. Explain concisely why these specific metrics indicate a maintenance risk.
    2. Provide 1-2 concrete, high-level refactoring strategies.
    
    Respond in plain text. Keep it under 100 words.
    """
    
    max_retries = 3
    base_delay = 3 # Start with a 3-second wait
    
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model='gemini-3.1-flash-lite',
                contents=prompt,
                config=types.GenerateContentConfig(temperature=0.3)
            )
            return response.text or "No explanation generated."
            
        except Exception as e:
            # If it's a 503 or 429 error and we have retries left, wait and try again
            if attempt < max_retries - 1:
                sleep_time = base_delay * (2 ** attempt) # 3s, then 6s
                time.sleep(sleep_time)
                continue
                
            # If we are out of retries, return the error string
            return f"[API Error: The AI service is currently busy. ({type(e).__name__})]"