import re
from git import exc
from typing import Dict, Optional
from pathlib import Path
from git import Repo  

def validate_github_url(url: str) -> bool:
    """Ensure the URL is a valid GitHub repository."""
    pattern = r"^https?://github\.com/[\w.-]+/[\w.-]+/?$"
    return bool(re.match(pattern, url))

def extract_metadata(url: str) -> Dict[str, str]:
    """Extract owner and repository name from the URL."""
    parts = url.rstrip("/").split("/")
    return {"owner": parts[-2], "name": parts[-1]}


def clone_repository(
    url: str, 
    storage_path: str = "./repositories", 
    branch: Optional[str] = None,  # Fixed duplicate "= None" syntax error
    force_update: bool = False
) -> Dict[str, str]:
    """Clone the repo and return metadata including the local path."""
    
    if not validate_github_url(url):
        raise ValueError("Invalid GitHub URL. Format: https://github.com/owner/repo")
        
    meta = extract_metadata(url)
    clone_target = Path(storage_path) / f"{meta['owner']}_{meta['name']}"

    try:
        if clone_target.exists():
            if force_update:
                repo = Repo(clone_target)
                origin = repo.remotes.origin
                
                # Pull specific branch if provided, otherwise pull active branch
                if branch:
                    origin.pull(branch)
                else:
                    origin.pull()
                    
            meta["local_path"] = str(clone_target)
            return meta
            
        # Clone specific branch if provided, otherwise auto-detect default (main/master)
        if branch:
            Repo.clone_from(url, clone_target, branch=branch)
        else:
            Repo.clone_from(url, clone_target)
            
        meta["local_path"] = str(clone_target)
        return meta
        
    except exc.GitCommandError as e:
        error_msg = f"Failed to clone/pull repository: {e.stderr.strip()}"
        raise RuntimeError(error_msg) from e
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred during repository setup: {str(e)}") from e
