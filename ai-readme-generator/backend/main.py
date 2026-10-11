
from urllib.parse import urlparse

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="AI README Generator API")

# Development configuration.
# Tighten this before deploying the application.
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"chrome-extension://.*",
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


class RepositoryRequest(BaseModel):
    url: str


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "message": "AI README Generator backend is running"
    }


@app.post("/inspect-repo")
def inspect_repository(request: RepositoryRequest):
    parsed = urlparse(request.url)

    if parsed.scheme != "https" or parsed.hostname != "github.com":
        raise HTTPException(
            status_code=400,
            detail="Please open a GitHub repository."
        )

    parts = parsed.path.strip("/").split("/")

    if (
        len(parts) < 2
        or not parts[0]
        or not parts[1]
        or parts[0] in {".", ".."}
        or parts[1] in {".", ".."}
        or parts[1].endswith(".git")
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid GitHub repository URL."
        )

    owner, repo = parts[0], parts[1]

    return {
        "owner": owner,
        "repo": repo,
        "repository_url": f"https://github.com/{owner}/{repo}",
        "message": "Repository identified successfully!"
    }
