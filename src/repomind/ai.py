import os
import json
from typing import Dict, Any
from google import genai 
from google.genai import types 
from repomind.analyzer import get_code_slice


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




def detect_repository_issues(
    repo_meta: dict[str, str], 
    top_findings: list[dict[str, Any]]
) -> list[dict[str, str]]:
    """Synthesize deterministic AST findings and actual code context into readable issues."""
    
    if not top_findings:
        return []
        
    evidence = ""
    for f in top_findings:
        findings_list: list[dict[str, Any]] = f.get("findings", [])
        finding_types = [issue.get("type", "UNKNOWN") for issue in findings_list]
        
        # --- THE FIX: Robust Context Extraction ---
        start = f.get('start_line')
        end = f.get('end_line')
        
        # Check if we have valid line numbers (Function-level finding)
        if start is not None and end is not None:
            code_snippet = get_code_slice(f['file'], start, end)
        else:
            # Fallback: God File finding (Module-level). Read first 60 lines.
            try:
                with open(f['file'], 'r', encoding='utf-8') as file_obj:
                    lines = file_obj.readlines()
                    code_snippet = "".join(lines[:60]) + "\n... [Full module truncated for Context Limit] ..."
            except Exception:
                code_snippet = "Error: Could not read file content."
        
        # Defensive constraint: Truncate massive snippets
        code_lines = code_snippet.split('\n')
        if len(code_lines) > 60:
            code_snippet = '\n'.join(code_lines[:60]) + "\n... [Code Truncated for Context Limit] ..."
            
        evidence += f"### TARGET: Function `{f['function']}` (File: {f['file']})\n"
        evidence += f"- Metrics: Complexity={f.get('complexity', 'N/A')}, Nesting={f.get('nesting', 'N/A')}\n"
        evidence += f"- Violations: {', '.join(finding_types)}\n"
        evidence += f"- Source Code Evidence:\n```python\n{code_snippet}\n```\n\n"
    
    prompt = f"""
    You are a Senior Staff Auditor. I have run a deterministic AST analysis on the repository "{repo_meta['name']}".
    
    [HARD CODE EVIDENCE]
    {evidence}
    
    Task:
    Write a clear, concise issue report for EACH of the findings provided above. 
    1. Look at the provided source code to see EXACTLY what is causing the high complexity/nesting.
    2. Cite the specific logic (e.g., "The massive switch statement handling user auth...") in your description.
    3. DO NOT invent new issues. Only explain the evidence provided.
    
    Respond ONLY with a valid JSON array matching this exact schema:
    [
        {{
            "title": "High Complexity in [Function Name]",
            "category": "Technical Debt",
            "severity": "High",
            "description": "Specific explanation of the messy logic found in the code snippet..."
        }}
    ]
    """
    
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    response = client.models.generate_content(
        model='gemini-3.1-flash-lite',
        contents=prompt,
        config=types.GenerateContentConfig(response_mime_type="application/json", temperature=0.1)
    )
    
    # ... existing Gemini client call ...
    
    parsed_issues = list(json.loads(response.text)) if response.text else []
    
    # --- PHASE 2.5 FIX: Inject the math back into the AI payload ---
    for i, issue in enumerate(parsed_issues):
        if i < len(top_findings):
            issue["file_path"] = top_findings[i].get("file")
            issue["function_name"] = top_findings[i].get("function")
            issue["complexity"] = top_findings[i].get("complexity")
            issue["nesting"] = top_findings[i].get("nesting")
            
    return parsed_issues



def generate_recommendations(
    repo_meta: dict[str, str], 
    stage: str, 
    db_findings: list[Any] # Accepts SQLAlchemy Finding objects
) -> list[dict[str, Any]]:
    """Generate engineering recommendations explicitly linked to deterministic findings."""
    
    # --- PHASE 2.5 & 3: Finding Enrichment & Deterministic Priority Math ---
    # --- PHASE 2.5 & 3: Finding Enrichment & Deterministic Priority Math ---
    payload = []
    for f in db_findings:
        # Map string severities to mathematical weights
        sev_map = {"High": 10, "Medium": 5, "Low": 2}
        sev = sev_map.get(str(f.severity), 5)
            
        comp = f.complexity or 0
        nest = f.nesting or 0
        
        # The Math: Higher complexity, nesting, and severity = higher priority
        raw_score = (comp * 2) + (nest * 3) + (sev * 2)
        p_score = min(10.0, round(raw_score / 10.0, 1))
        
        payload.append({
            "finding_id": str(f.id),
            "file": f.file_path,
            "function": f.function_name,
            "issue": f.title,
            "calculated_priority_score": p_score
        })

    prompt = f"""
    You are a Lead Staff Engineer analyzing a {repo_meta.get('language', 'software')} repository.
    Stage: {stage}
    
    [DETERMINISTIC CODE FINDINGS]
    {json.dumps(payload, indent=2)}
    
    Task:
    1. Group the provided findings into 3 to 5 high-level architectural Recommendations (e.g., "Refactor Routing Complexity").
    2. Assign the exact 'finding_id' strings of the grouped findings to the recommendation.
    3. DO NOT INVENT priority scores. The recommendation's 'priority_score' MUST be exactly the highest 'calculated_priority_score' out of its linked findings.
    
    Respond ONLY with a valid JSON array of objects matching this schema:
    [
        {{
            "title": "Refactor Routing Complexity",
            "description": "Decompose the deeply nested request handlers to improve maintainability.",
            "priority_score": 9.8,
            "impact_score": 9.0,
            "effort_score": 5.0,
            "linked_finding_ids": ["uuid-string-1", "uuid-string-2"]
        }}
    ]
    """
    
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    response = client.models.generate_content(
        model='gemini-3.1-flash-lite',
        contents=prompt,
        config=types.GenerateContentConfig(response_mime_type="application/json", temperature=0.1)
    )
    
    return list(json.loads(response.text)) if response.text else []

def generate_blueprint(
    recommendation_title: str, 
    recommendation_desc: str,
    repo_meta: dict[str, str],
    linked_findings: list[Any]
) -> dict[str, Any]:
    """Generate an implementation blueprint bounded by rigid repository constraints."""
    
    # --- PHASE 4 & 5: The Anti-Hallucination Box ---
    language = repo_meta.get('language', 'Unknown')
    framework = repo_meta.get('framework', 'Unknown')
    
    evidence = ""
    for f in linked_findings:
        evidence += f"- Target: {f.file_path} (Function: {f.function_name}) | Issue: {f.title}\n"
        
    prompt = f"""
    You are a Senior Staff {language} Engineer. Create an implementation blueprint.
    
    Task: {recommendation_title}
    Context: {recommendation_desc}
    
    [RIGID CONSTRAINTS]
    - Target Language: {language}
    - Target Framework: {framework}
    - CRITICAL: You MUST NOT generate file paths, extensions (like .ts for Python), or design patterns that do not belong in a standard {language} ecosystem.
    
    [HARD EVIDENCE TO REFACTOR]
    {evidence}
    
    Respond ONLY with a valid JSON object matching this exact schema:
    {{
        "goal": "Clear statement of what will be achieved.",
        "architecture_changes": ["List of high-level changes"],
        "files_to_create": ["List of new file paths"],
        "files_to_modify": ["List of existing files to change"],
        "estimated_effort": "e.g., 2 weeks, 3 days",
        "implementation_steps": ["Step 1:...", "Step 2:..."],
        "validation_checklist": ["List of specific tests/checks to ensure the refactor works"],
        "rollback_strategy": "Clear instructions on how to safely revert this change if it fails in production",
        "migration_steps": ["Data or state migration steps, if any. Otherwise ['None required']"]
    }}
    """
    
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    response = client.models.generate_content(
        model='gemini-3.1-flash-lite',
        contents=prompt,
        config=types.GenerateContentConfig(response_mime_type="application/json", temperature=0.1)
    )
    
    return dict(json.loads(response.text)) if response.text else {}


    
