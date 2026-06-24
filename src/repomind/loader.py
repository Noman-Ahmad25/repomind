import re
from pathlib import Path
from typing import Dict
from git import Repo  

def validate_github_url(url: str) -> bool:
    """Ensure the URL is a valid GitHub repository."""
    pattern = r"^https?://github\.com/[\w.-]+/[\w.-]+/?$"
    return bool(re.match(pattern, url))

def extract_metadata(url: str) -> Dict[str, str]:
    """Extract owner and repository name from the URL."""
    parts = url.rstrip("/").split("/")
    return {"owner": parts[-2], "name": parts[-1]}

def clone_repository(url: str, storage_path: str = "./repositories") -> Dict[str, str]:
    """Clone the repo and return metadata including the local path."""
    if not validate_github_url(url):
        raise ValueError("Invalid GitHub URL. Format: https://github.com/owner/repo")
        
    meta = extract_metadata(url)
    clone_target = Path(storage_path) / f"{meta['owner']}_{meta['name']}"
    
    # If it already exists, skip cloning to save time during testing
    if clone_target.exists():
        meta["local_path"] = str(clone_target)
        return meta
        
    Repo.clone_from(url, clone_target)
    meta["local_path"] = str(clone_target)
    return meta