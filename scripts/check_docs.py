"""Small offline checks for this documentation repository, not a Markdown parser."""

import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    "README.md", "DTSpect.md", "LICENSE", "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md", ".editorconfig", ".gitattributes", ".gitignore",
    "docs/ROADMAP.md", "docs/adr/0001-annotation-manifest-contract.md",
    ".github/workflows/docs.yml", "scripts/check_docs.py",
)
TEXT_SUFFIXES = {".md", ".yml", ".yaml", ".json", ".py"}
LINK = re.compile(r"!?\[[^\]\n]*\]\(([^)\n]+)\)")
FENCE = re.compile(r"^(`{3,}|~{3,})(.*)$")


def check_markdown(path, text, errors):
    """Check simple inline local links and JSON fences; ignore fragment targets."""
    prose = []
    fence = None
    body = []
    language = ""
    start = 0
    for number, line in enumerate(text.splitlines(), 1):
        match = FENCE.match(line)
        if fence is None:
            if match:
                fence, language = match.groups()
                language = language.strip()
                start = number
                body = []
            else:
                prose.append((number, line))
        elif (match and match[1][0] == fence[0]
              and len(match[1]) >= len(fence) and not match[2].strip()):
            if language == "json":
                try:
                    json.loads("\n".join(body))
                except ValueError as exc:
                    errors.append(f"{path}:{start}: invalid fenced JSON: {exc}")
            fence = None
        else:
            body.append(line)
    if fence is not None:
        errors.append(f"{path}:{start}: unclosed code fence")
    for number, line in prose:
        for match in LINK.finditer(line):
            # Supports simple destinations and optional titles, not nested syntax.
            destination = match[1].split(' "', 1)[0].strip().strip("<>")
            url = urlsplit(destination)
            if url.scheme or url.netloc or not url.path:
                continue
            target = (ROOT / path.parent / unquote(url.path)).resolve()
            if not target.is_relative_to(ROOT) or not target.exists():
                errors.append(f"{path}:{number}: missing/outside local link: {destination}")


def main():
    errors = []
    for name in REQUIRED:
        if not (ROOT / name).is_file():
            errors.append(f"Missing foundation file: {name}")
    try:
        output = subprocess.check_output(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
            cwd=ROOT,
        ).decode("utf-8")
    except (OSError, subprocess.CalledProcessError, UnicodeError) as exc:
        print(f"Cannot enumerate repository files: {exc}", file=sys.stderr)
        return 1
    paths = sorted({Path(name) for name in output.split("\0") if name})
    checked = 0
    for path in paths:
        if path.name == "LICENSE":
            continue  # Preserve the upstream license text verbatim.
        if path.suffix not in TEXT_SUFFIXES and path.as_posix() not in REQUIRED:
            continue
        try:
            data = (ROOT / path).read_bytes()
            text = data.decode("utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"{path}: cannot read UTF-8 text: {exc}")
            continue
        checked += 1
        if data.startswith(b"\xef\xbb\xbf") or b"\r" in data:
            errors.append(f"{path}: use UTF-8 without BOM and LF line endings")
        if not text.endswith("\n"):
            errors.append(f"{path}: missing final newline")
        for number, line in enumerate(text.splitlines(), 1):
            if line.rstrip(" \t") != line:
                errors.append(f"{path}:{number}: trailing whitespace")
        if path.suffix == ".md":
            check_markdown(path, text, errors)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"Documentation checks passed ({checked} text files; license preserved).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
