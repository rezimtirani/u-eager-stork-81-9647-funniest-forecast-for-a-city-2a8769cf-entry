"""Upload main.py and README.md for the Forecast City entry to GitHub.

Creates or updates the two files in the entry repository via the GitHub
Contents API, using the stored custom.github credential. Run from anywhere;
the entry folder is resolved relative to this script's location.
"""
import base64
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
from dynamic_credentials import add_surrogate_to_request  # noqa: E402

OWNER = "rezimtirani"
REPO = "u-eager-stork-81-9647-funniest-forecast-for-a-city-2a8769cf-entry"
API = "https://api.github.com"
ENTRY_DIR = Path(__file__).resolve().parent
FILES = ["main.py", "README.md"]


def github_request(method, url, payload=None):
    body = None
    headers = {"Accept": "application/vnd.github+json"}
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=body, method=method, headers=headers)
    add_surrogate_to_request(request, "custom.github", allowed_hosts=["api.github.com"])
    with urllib.request.urlopen(request) as response:
        return json.loads(response.read().decode("utf-8"))


def existing_sha(path):
    try:
        info = github_request("GET", f"{API}/repos/{OWNER}/{REPO}/contents/{path}")
    except urllib.error.HTTPError as error:
        if error.code == 404:
            return None
        raise
    return info.get("sha")


def push_file(path):
    local = ENTRY_DIR / path
    encoded = base64.b64encode(local.read_bytes()).decode("ascii")
    payload = {
        "message": f"Add {path} — Funniest Forecast for a City That Isn't entry",
        "content": encoded,
    }
    sha = existing_sha(path)
    if sha:
        payload["sha"] = sha
    result = github_request(
        "PUT", f"{API}/repos/{OWNER}/{REPO}/contents/{path}", payload
    )
    print(f"{path}: {result['commit']['sha']}")
    return result["commit"]["sha"]


def main():
    for name in FILES:
        push_file(name)
    print(f"Done: {OWNER}/{REPO}")


if __name__ == "__main__":
    main()
