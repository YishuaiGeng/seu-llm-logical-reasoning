"""Check rendered local links, assets and anchors, including custom HTML.

Run after `mkdocs build --strict`. No network or third-party packages needed.
SPDX-License-Identifier: MIT
"""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if "id" in attributes:
            self.ids.add(attributes["id"])
        for key in ("href", "src"):
            if attributes.get(key):
                self.links.append(attributes[key])


def main():
    root = Path(__file__).resolve().parents[1] / "site"
    if not (root / "index.html").is_file():
        raise SystemExit("Build the site with mkdocs build --strict first.")
    pages = {}
    for path in root.rglob("*.html"):
        parser = References()
        parser.feed(path.read_text())
        pages[path] = parser

    errors = []
    checked = 0
    for path, page in pages.items():
        for link in page.links:
            target = urlsplit(link)
            if target.scheme or target.netloc:
                continue
            if target.path.startswith("/"):
                # Project sites live under a repository prefix on GitHub Pages.
                prefix = "/seu-llm-logical-reasoning/"
                relative = target.path.removeprefix(prefix) if target.path.startswith(prefix) else target.path.lstrip("/")
                destination = (root / unquote(relative)).resolve()
            else:
                destination = (path.parent / unquote(target.path)).resolve() if target.path else path
            if destination.is_dir():
                destination /= "index.html"
            checked += 1
            if not destination.exists():
                errors.append(f"{path.relative_to(root)}: missing {link}")
            elif target.fragment and destination in pages:
                if unquote(target.fragment) not in pages[destination].ids:
                    errors.append(f"{path.relative_to(root)}: missing anchor {link}")

    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Checked {len(pages)} HTML pages and {checked} local references: passed")


if __name__ == "__main__":
    main()
