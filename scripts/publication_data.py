"""Load manual and automatically discovered publication records."""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

import yaml

from publication_utils import publications_match


def _load_publications(path: Path, required: bool) -> list[dict[str, Any]]:
    if not path.exists():
        if required:
            raise ValueError(f"Required data file does not exist: {path}")
        return []

    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a YAML mapping")
    publications = payload.get("publications")
    if not isinstance(publications, list) or (required and not publications):
        raise ValueError(f"{path} must contain a publications list")
    if not all(isinstance(publication, dict) for publication in publications):
        raise ValueError(f"{path}: each publication must be a mapping")
    return publications


def load_merged_publications(
    manual_path: Path, automatic_path: Path
) -> list[dict[str, Any]]:
    publications = copy.deepcopy(_load_publications(manual_path, required=True))
    for automatic in _load_publications(automatic_path, required=False):
        if any(
            publications_match(manual, automatic) for manual in publications
        ):
            continue
        publications.append(copy.deepcopy(automatic))
    return publications
