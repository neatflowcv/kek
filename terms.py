import re
from pathlib import Path


def load_terms(terms_file: Path) -> list[str]:
    if not terms_file.exists():
        return []
    terms = []
    for line in terms_file.read_text().splitlines():
        term = line.strip()
        if term and not term.startswith("#"):
            terms.append(term)
    return sorted(terms, key=len, reverse=True)


def protect_terms(text: str, terms: list[str]) -> tuple[str, dict[str, str]]:
    placeholders = {}
    protected = text
    idx = 0
    for term in terms:
        pattern = re.compile(re.escape(term), re.IGNORECASE)
        matches = pattern.findall(protected)
        for match in matches:
            if match not in placeholders.values():
                placeholder = f"TERM{idx}"
                placeholders[placeholder] = match
                protected = protected.replace(match, placeholder, 1)
                idx += 1
    return protected, placeholders


def restore_terms(text: str, placeholders: dict[str, str]) -> str:
    restored = text
    for placeholder, term in placeholders.items():
        restored = restored.replace(placeholder, term)
    return restored
