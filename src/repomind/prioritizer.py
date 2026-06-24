# src/repomind/prioritizer.py

def calculate_impact(findings, criticality_multiplier=1.5):
    # Base score from metrics
    raw_score = findings["complexity"] + (findings["nesting"] * 2)
    
    # Scale by criticality
    return raw_score * criticality_multiplier

def get_top_issues(all_findings, limit=10):
    # Sort findings by the calculated impact score
    sorted_issues = sorted(
        all_findings, 
        key=lambda x: calculate_impact(x), 
        reverse=True
    )
    return sorted_issues[:limit]