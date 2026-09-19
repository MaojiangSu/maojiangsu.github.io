#!/usr/bin/env python3
"""Discover publications from an allowed Google Scholar public profile page."""

from __future__ import annotations

import hashlib
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urljoin, urlparse

import requests
import yaml
from bs4 import BeautifulSoup

from publication_utils import normalize_title, publication_year, publications_match


ROOT = Path(__file__).resolve().parents[1]
MANUAL_DATA_FILE = ROOT / "data" / "publications.yml"
SCHOLAR_DATA_FILE = ROOT / "data" / "publications.scholar.yml"
SCHOLAR_ORIGIN = "https://scholar.google.com"
USER_AGENT = "MaojiangSuPublicationsBot/1.0 (+https://maojiangsu.github.io/)"


def load_yaml(path: Path, required: bool = True) -> dict[str, Any]:
    if not path.exists():
        if required:
            raise ValueError(f"Required data file does not exist: {path}")
        return {}
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a YAML mapping")
    return payload


def publications_from(payload: dict[str, Any], path: Path) -> list[dict[str, Any]]:
    publications = payload.get("publications") or []
    if not isinstance(publications, list):
        raise ValueError(f"{path}: publications must be a list")
    if not all(isinstance(publication, dict) for publication in publications):
        raise ValueError(f"{path}: each publication must be a mapping")
    return publications


def scholar_config(payload: dict[str, Any]) -> dict[str, Any]:
    sources = payload.get("sources") or {}
    config = sources.get("google_scholar") or {}
    if not isinstance(config, dict):
        raise ValueError("sources.google_scholar must be a mapping")
    if not config.get("user_id") or not config.get("author_name"):
        raise ValueError(
            "sources.google_scholar requires user_id and author_name fields"
        )
    max_results = int(config.get("max_results", 100))
    if not 1 <= max_results <= 100:
        raise ValueError("sources.google_scholar.max_results must be between 1 and 100")
    return {**config, "max_results": max_results}


def profile_url(config: dict[str, Any]) -> str:
    return (
        f"{SCHOLAR_ORIGIN}/citations?user={config['user_id']}"
        f"&hl=en&pagesize={config['max_results']}"
    )


def clean_text(value: str) -> str:
    cleaned = re.sub(r"\s+", " ", value).strip()
    return re.sub(r"\s+([,.;:])", r"\1", cleaned)


def scholar_id_from_url(url: str, title: str) -> str:
    values = parse_qs(urlparse(url).query).get("citation_for_view") or []
    if values and values[0]:
        return values[0]
    digest = hashlib.sha256(normalize_title(title).encode("utf-8")).hexdigest()[:16]
    return f"title:{digest}"


def slug_from_scholar_id(scholar_id: str, title: str) -> str:
    token = scholar_id.split(":", 1)[-1]
    token = re.sub(r"[^a-z0-9]+", "-", token.casefold()).strip("-")
    if not token:
        token = hashlib.sha256(normalize_title(title).encode("utf-8")).hexdigest()[:16]
    return f"scholar-{token[:48]}"


def parse_profile(html: str, config: dict[str, Any], url: str) -> list[dict[str, Any]]:
    lowered = html.casefold()
    if "g-recaptcha" in lowered or "unusual traffic" in lowered:
        raise RuntimeError("Google Scholar returned a CAPTCHA; existing data was not changed")

    soup = BeautifulSoup(html, "html.parser")
    profile_name_element = soup.select_one("#gsc_prf_in")
    profile_name = clean_text(profile_name_element.get_text(" ", strip=True)) if profile_name_element else ""
    if normalize_title(config["author_name"]) not in normalize_title(profile_name):
        raise RuntimeError(
            f"Unexpected Scholar profile {profile_name!r}; existing data was not changed"
        )

    rows = soup.select("tr.gsc_a_tr")
    if not rows:
        raise RuntimeError("Scholar profile contained no publication rows")

    current_year = datetime.now(timezone.utc).year
    publications: list[dict[str, Any]] = []
    for row in rows:
        title_link = row.select_one("a.gsc_a_at")
        if not title_link:
            continue
        title = clean_text(title_link.get_text(" ", strip=True))
        article_url = urljoin(SCHOLAR_ORIGIN, str(title_link.get("href") or ""))
        scholar_id = scholar_id_from_url(article_url, title)

        secondary_lines = row.select(".gs_gray")
        author_line = clean_text(secondary_lines[0].get_text(" ", strip=True)) if secondary_lines else ""
        venue = clean_text(secondary_lines[1].get_text(" ", strip=True)) if len(secondary_lines) > 1 else ""
        authors = [
            clean_text(author)
            for author in author_line.split(",")
            if normalize_title(clean_text(author))
        ]
        profile_author = str(config["author_name"])
        profile_aliases = {normalize_title(profile_author)}
        profile_name_parts = profile_author.split()
        if profile_name_parts:
            profile_aliases.add(normalize_title(profile_name_parts[0][0] + profile_name_parts[-1]))
        if not any(normalize_title(author) in profile_aliases for author in authors):
            authors.append(profile_author)

        year_element = row.select_one(".gsc_a_y span")
        year_match = re.search(r"\b(19|20)\d{2}\b", year_element.get_text(" ") if year_element else "")
        year = int(year_match.group(0)) if year_match else current_year
        description = venue.rstrip(".") + "." if venue else f"Listed on Google Scholar in {year}."

        publications.append(
            {
                "slug": slug_from_scholar_id(scholar_id, title),
                "title": title,
                "date": f"{year:04d}-01-01",
                "year": year,
                "venue": venue,
                "tags": ["Publication"],
                "authors": authors,
                "description": description,
                "summary": description,
                "edit_post": {
                    "url": article_url,
                    "text": "Google Scholar",
                },
                "scholar": {
                    "id": scholar_id,
                    "user_id": str(config["user_id"]),
                    "url": article_url,
                },
            }
        )

    if not publications:
        raise RuntimeError(f"No publications could be parsed from {url}")
    return publications


def fetch_profile(config: dict[str, Any]) -> tuple[str, list[dict[str, Any]]]:
    url = profile_url(config)
    response = requests.get(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "en-US,en;q=0.8",
        },
        timeout=30,
    )
    response.raise_for_status()
    return url, parse_profile(response.text, config, url)


def find_match(
    publication: dict[str, Any], candidates: list[dict[str, Any]]
) -> dict[str, Any] | None:
    return next(
        (candidate for candidate in candidates if publications_match(publication, candidate)),
        None,
    )


def merge_fetched_records(
    existing: list[dict[str, Any]], fetched: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    merged = [dict(publication) for publication in existing]
    for publication in fetched:
        match = find_match(publication, merged)
        if match is None:
            merged.append(publication)
            continue
        publication["slug"] = match.get("slug") or publication["slug"]
        merged[merged.index(match)] = publication

    return sorted(
        merged,
        key=lambda publication: (
            -int(publication_year(publication) or 0),
            normalize_title(publication.get("title")),
        ),
    )


def render_payload(
    config: dict[str, Any], url: str, publications: list[dict[str, Any]]
) -> str:
    payload = {
        "version": 1,
        "source": {
            "provider": "google_scholar",
            "user_id": str(config["user_id"]),
            "profile_url": url,
        },
        "publications": publications,
    }
    return yaml.safe_dump(
        payload,
        allow_unicode=True,
        sort_keys=False,
        width=1000,
    )


def set_github_output(name: str, value: str) -> None:
    output_file = os.environ.get("GITHUB_OUTPUT")
    if not output_file:
        return
    delimiter = "SCHOLAR_SYNC_EOF"
    with Path(output_file).open("a", encoding="utf-8") as stream:
        stream.write(f"{name}<<{delimiter}\n{value}\n{delimiter}\n")


def main() -> int:
    manual_payload = load_yaml(MANUAL_DATA_FILE)
    config = scholar_config(manual_payload)
    manual_publications = publications_from(manual_payload, MANUAL_DATA_FILE)

    existing_payload = load_yaml(SCHOLAR_DATA_FILE, required=False)
    existing_publications = publications_from(existing_payload, SCHOLAR_DATA_FILE)
    url, fetched_publications = fetch_profile(config)

    known_publications = manual_publications + existing_publications
    new_publications = [
        publication
        for publication in fetched_publications
        if find_match(publication, known_publications) is None
    ]
    merged_publications = merge_fetched_records(
        existing_publications, fetched_publications
    )
    rendered = render_payload(config, url, merged_publications)
    current = (
        SCHOLAR_DATA_FILE.read_text(encoding="utf-8")
        if SCHOLAR_DATA_FILE.exists()
        else None
    )
    changed = current != rendered
    if changed:
        SCHOLAR_DATA_FILE.write_text(rendered, encoding="utf-8", newline="\n")

    new_titles = "\n".join(
        f"- {publication['title']}" for publication in new_publications
    )
    set_github_output("changed", str(changed).lower())
    set_github_output("new_count", str(len(new_publications)))
    set_github_output("new_titles", new_titles)
    set_github_output("profile_url", url)

    print(
        f"Fetched {len(fetched_publications)} Scholar publications; "
        f"{len(new_publications)} new; data changed: {str(changed).lower()}"
    )
    if new_titles:
        print(new_titles)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (
        OSError,
        RuntimeError,
        TypeError,
        ValueError,
        requests.RequestException,
        yaml.YAMLError,
    ) as exc:
        print(f"Scholar synchronization failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
