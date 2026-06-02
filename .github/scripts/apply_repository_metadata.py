#!/usr/bin/env python3
"""Apply repository About metadata to GitHub.

This script intentionally uses only the Python standard library so it can run
in a fresh checkout without installing deployment dependencies.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
METADATA_PATH = ROOT / ".github" / "repository-metadata.yml"
DEFAULT_API_URL = "https://api.github.com"


def strip_value(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def parse_repository_metadata(path: Path = METADATA_PATH) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    repository: dict[str, Any] = {"topics": []}
    in_repository = False
    in_topics = False

    for raw_line in text.splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        if not raw_line.startswith(" "):
            in_repository = raw_line.strip() == "repository:"
            in_topics = False
            continue
        if not in_repository:
            continue

        line = raw_line.rstrip()
        stripped = line.strip()
        if stripped == "topics:":
            in_topics = True
            continue
        if in_topics and stripped.startswith("- "):
            repository["topics"].append(strip_value(stripped[2:]))
            continue
        in_topics = False
        if ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        repository[key.strip()] = strip_value(value)

    return repository


def normalize_repo(value: str) -> str:
    value = value.strip()
    if value.startswith("https://github.com/"):
        value = value.removeprefix("https://github.com/")
    if value.endswith(".git"):
        value = value[:-4]
    value = value.strip("/")
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", value):
        raise ValueError("repository must look like owner/name")
    return value


def repo_from_git_remote() -> str | None:
    try:
        result = subprocess.run(
            ["git", "config", "--get", "remote.origin.url"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return None

    remote = result.stdout.strip()
    if remote.startswith("git@github.com:"):
        remote = remote.removeprefix("git@github.com:").removesuffix(".git")
    elif remote.startswith("https://github.com/"):
        remote = remote.removeprefix("https://github.com/").removesuffix(".git")
    else:
        return None

    try:
        return normalize_repo(remote)
    except ValueError:
        return None


def validate_metadata(metadata: dict[str, Any]) -> None:
    required = ["description", "topics"]
    missing = [key for key in required if not metadata.get(key)]
    if missing:
        raise ValueError(f"repository metadata missing required field(s): {', '.join(missing)}")

    topics = metadata.get("topics", [])
    if not isinstance(topics, list) or not topics:
        raise ValueError("repository metadata must include at least one topic")
    if len(topics) > 20:
        raise ValueError("GitHub supports at most 20 repository topics")
    for topic in topics:
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,49}", topic):
            raise ValueError(f"invalid GitHub topic: {topic}")


def github_request(api_url: str, token: str, method: str, path: str, payload: dict[str, Any]) -> dict[str, Any]:
    url = f"{api_url.rstrip('/')}{path}"
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": "fengshui-master-metadata-sync",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        body = response.read().decode("utf-8")
    return json.loads(body) if body else {}


def build_payloads(metadata: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    repo_payload = {
        "description": metadata["description"],
        "homepage": metadata.get("homepage", ""),
    }
    topics_payload = {"names": metadata["topics"]}
    return repo_payload, topics_payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply FengShui Master GitHub About metadata.")
    parser.add_argument("--repo", default=os.environ.get("GITHUB_REPOSITORY") or repo_from_git_remote())
    parser.add_argument("--metadata", type=Path, default=METADATA_PATH)
    parser.add_argument("--api-url", default=os.environ.get("GITHUB_API_URL", DEFAULT_API_URL))
    parser.add_argument("--token-env", default="GITHUB_TOKEN")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    try:
        if not args.repo:
            raise ValueError("provide --repo owner/name or set GITHUB_REPOSITORY")
        repo = normalize_repo(args.repo)
        metadata = parse_repository_metadata(args.metadata)
        validate_metadata(metadata)
        repo_payload, topics_payload = build_payloads(metadata)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.dry_run:
        print(
            json.dumps(
                {
                    "repo": repo,
                    "repository_patch": repo_payload,
                    "topics_put": topics_payload,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    token = os.environ.get(args.token_env) or os.environ.get("GH_TOKEN")
    if not token:
        print(f"error: set {args.token_env} or GH_TOKEN before updating GitHub", file=sys.stderr)
        return 2

    try:
        github_request(args.api_url, token, "PATCH", f"/repos/{repo}", repo_payload)
        github_request(args.api_url, token, "PUT", f"/repos/{repo}/topics", topics_payload)
    except urllib.error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        print(f"error: GitHub API returned {exc.code}: {details}", file=sys.stderr)
        return 1
    except urllib.error.URLError as exc:
        print(f"error: could not reach GitHub API: {exc.reason}", file=sys.stderr)
        return 1

    print(f"Applied GitHub About metadata to {repo}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
