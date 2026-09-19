"""Shared helpers for matching publication records."""

from __future__ import annotations

import re
from difflib import SequenceMatcher
from typing import Any


def normalize_title(value: Any) -> str:
    return re.sub(r"[^a-z0-9]+", "", str(value or "").casefold())


def title_tokens(value: Any) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", str(value or "").casefold()))


def titles_match(left: Any, right: Any) -> bool:
    left_normalized = normalize_title(left)
    right_normalized = normalize_title(right)
    if not left_normalized or not right_normalized:
        return False
    if left_normalized == right_normalized:
        return True

    similarity = SequenceMatcher(None, left_normalized, right_normalized).ratio()
    if similarity >= 0.86:
        return True

    left_tokens = title_tokens(left)
    right_tokens = title_tokens(right)
    union = left_tokens | right_tokens
    token_overlap = len(left_tokens & right_tokens) / len(union) if union else 0
    return similarity >= 0.72 and token_overlap >= 0.60


def publication_year(publication: dict[str, Any]) -> str:
    explicit_year = str(publication.get("year") or "").strip()
    if re.fullmatch(r"\d{4}", explicit_year):
        return explicit_year
    match = re.match(r"(\d{4})", str(publication.get("date") or ""))
    return match.group(1) if match else ""


def publication_titles(publication: dict[str, Any]) -> list[str]:
    titles = [str(publication.get("title") or "")]
    aliases = publication.get("aliases") or []
    if isinstance(aliases, list):
        titles.extend(str(alias) for alias in aliases)
    return [title for title in titles if title]


def publications_match(left: dict[str, Any], right: dict[str, Any]) -> bool:
    left_scholar_id = str((left.get("scholar") or {}).get("id") or "")
    right_scholar_id = str((right.get("scholar") or {}).get("id") or "")
    if left_scholar_id and left_scholar_id == right_scholar_id:
        return True

    left_titles = publication_titles(left)
    right_titles = publication_titles(right)
    if any(
        normalize_title(left_title) == normalize_title(right_title)
        for left_title in left_titles
        for right_title in right_titles
    ):
        return True

    left_year = publication_year(left)
    right_year = publication_year(right)
    if left_year and right_year and left_year != right_year:
        return False

    return any(
        titles_match(left_title, right_title)
        for left_title in left_titles
        for right_title in right_titles
    )
