import os
import json
from typing import Dict, Any
from google import genai 
from google.genai import types 
from repomind.analyzer import get_code_slice


GROUNDING_RULES = """
You are a repository review assistant operating on deterministic evidence only.
Use only the repository facts supplied in this prompt: metadata, AST findings, code snippets, metrics, and file or function names.
Never invent files, functions, classes, frameworks, dependencies, architectures, metrics, line numbers, or repository structure.
If a detail is not present in the supplied evidence, state that it is not provided rather than infer it.
Do not speculate about runtime behavior, security posture, business domain, or architecture beyond the evidence.
Use concise technical language and return only machine-parseable JSON when requested.
"""


def detect_repository_stage(repo_meta: Dict[str, str], structure: Dict[str, int]) -> Dict[str, Any]:
    """Analyze repository metadata to determine its maturity stage."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is missing.")
        
    client = genai.Client(api_key=api_key)
    
    # Using flash temporarily to bypass the strict free-tier limits on Pro
    model_name = 'gemini-3.1-flash-lite'
    
    prompt = f"""
{GROUNDING_RULES}

You are assessing repository maturity from the deterministic metadata supplied below.
Select exactly one stage from: Idea, Prototype, MVP, Growth, Mature.
Base the decision only on the supplied counts and repository name.
Return only a JSON object with this schema:
{{
  "stage": "Prototype",
  "confidence": 85,
  "reasoning": "Brief justification that cites only the supplied counts."
}}

Repository Data:
- Name: {repo_meta.get('name', 'unknown')}
- Total Files: {structure['files']}
- Total Classes: {structure['classes']}
- Total Functions: {structure['functions']}
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
{GROUNDING_RULES}

You are preparing a technical issue report from deterministic static analysis evidence for the repository "{repo_meta.get('name', 'unknown')}".
Use one object per supplied finding and ground every statement in the evidence below.
Do not infer unlisted defects, architecture issues, or business logic.

Input Evidence:
{evidence}

Return only a JSON array of objects with this schema:
[
  {{
    "issue": "Short, specific issue title",
    "severity": "High|Medium|Low",
    "location": "file:function or file",
    "evidence": "Direct evidence from the supplied snippet and metrics",
    "assessment": "Concise explanation of the observed structural condition",
    "recommendation": "Concrete remediation tied to the supplied evidence",
    "expected_benefit": "Expected effect of the remediation",
    "confidence": "High|Medium|Low",
    "title": "Short issue title",
    "category": "Technical Debt",
    "description": "Concise explanation derived only from the supplied evidence"
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
{GROUNDING_RULES}

You are synthesizing the supplied findings into a small set of concrete engineering recommendations.
Use only the finding payload provided below and reference only the finding IDs that are present in that payload.
Do not introduce new defects, components, or architecture assumptions.

Repository Language: {repo_meta.get('language', 'software')}
Current Analysis Stage: {stage}

Input Findings:
{json.dumps(payload, indent=2)}

Return only a JSON array of 3 to 5 objects with this schema:
[
  {{
    "title": "Concrete recommendation title",
    "description": "Specific remediation tied to the referenced findings",
    "priority_score": 0.0,
    "impact_score": 0.0,
    "effort_score": 0.0,
    "linked_finding_ids": ["id-1", "id-2"]
  }}
]

Rules:
- Each recommendation must be directly traceable to one or more supplied findings.
- The priority_score must be exactly the maximum calculated_priority_score among the linked findings.
- Keep descriptions concise, technical, and action-oriented.
- Do not average, add, or invent scores.
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
{GROUNDING_RULES}

You are producing an implementation blueprint for the supplied refactoring objective.
Use only the repository metadata and the finding evidence provided below.
Do not invent languages, frameworks, libraries, modules, or file paths that are not justified by the supplied evidence.
If the evidence does not support a new file, use an empty array for files_to_create rather than inventing a placeholder name.

Repository Language: {language}
Repository Framework: {framework}
Refactoring Objective: {recommendation_title}
Architectural Context: {recommendation_desc}

Input Evidence:
{evidence}

Return only a JSON object with this schema:
{{
  "goal": "Precise engineering end-state",
  "architecture_changes": ["High-level structural changes"],
  "files_to_create": ["Path only if justified by evidence"],
  "files_to_modify": ["Existing file paths supported by evidence"],
  "target_functions": ["Function names from the supplied evidence"],
  "implementation_steps": ["Concrete implementation steps"],
  "validation_checklist": ["Concrete validation steps"],
  "estimated_effort": "e.g. 2 days",
  "rollback_considerations": "Concrete rollback plan",
  "rollback_strategy": "Concrete rollback plan",
  "migration_steps": ["None required"]
}}

Rules:
- Keep the plan concrete and implementation-oriented.
- Reference only target functions and files present in the evidence.
- Do not assume unprovided technologies or frameworks.
- Keep the output concise and deterministic.
"""
    
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    response = client.models.generate_content(
        model='gemini-3.1-flash-lite',
        contents=prompt,
        config=types.GenerateContentConfig(response_mime_type="application/json", temperature=0.1)
    )
    
    return dict(json.loads(response.text)) if response.text else {}


    
