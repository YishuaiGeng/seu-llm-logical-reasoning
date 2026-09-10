"""Publish repository guides without maintaining duplicate Markdown files."""

import posixpath
import re
from pathlib import Path
from urllib.parse import urlsplit

from mkdocs.structure.files import File, InclusionLevel

ROOT = Path(__file__).resolve().parents[1]
REPO = "https://github.com/YishuaiGeng/seu-llm-logical-reasoning"
GENERATED = {
    "CONTRIBUTING.md": "community/contributing.md",
    "CODE_OF_CONDUCT.md": "community/code-of-conduct.md",
    "SECURITY.md": "community/security.md",
    "PROJECT_PLAN.md": "community/maintenance.md",
    "examples/README.md": "tutorials/examples.md",
    "examples/truth-table/README.md": "tutorials/truth-table-example.md",
    **{f"templates/{name}.md": f"templates/{name}.md"
       for name in ("README", "note", "paper", "tutorial", "meeting")},
}
SOURCES = {destination: source for source, destination in GENERATED.items()}
LINK = re.compile(r"(!?\[[^\]]*\]\()([^\s)]+)(\))")


def on_files(files, config):
    for source, destination in GENERATED.items():
        generated = File.generated(
            config, destination, content=(ROOT / source).read_text(),
            inclusion=InclusionLevel.INCLUDED,
        )
        generated.edit_uri = source
        files.append(generated)
    return files


def on_page_markdown(markdown, page, config, files):
    uri = page.file.src_uri
    source = SOURCES.get(uri, f"docs/{uri}")
    if uri in SOURCES:
        page.edit_url = f"{REPO}/edit/main/{source}"

    def replace(match):
        target = match.group(2)
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc or not parsed.path or target.startswith("/"):
            return match.group(0)
        resolved = posixpath.normpath(posixpath.join(posixpath.dirname(source), parsed.path))
        if resolved in GENERATED:
            destination = GENERATED[resolved]
        elif resolved.startswith("docs/"):
            destination = resolved[5:]
        elif (ROOT / resolved).is_file():
            return match.group(1) + f"{REPO}/blob/main/{resolved}" + (
                f"#{parsed.fragment}" if parsed.fragment else ""
            ) + match.group(3)
        else:
            return match.group(0)
        rewritten = posixpath.relpath(destination, posixpath.dirname(uri) or ".")
        if parsed.fragment:
            rewritten += f"#{parsed.fragment}"
        return match.group(1) + rewritten + match.group(3)

    return LINK.sub(replace, markdown)
