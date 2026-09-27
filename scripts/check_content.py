"""Validate frontmatter of notes, papers, tutorials and meetings.

Run before `mkdocs build`. Requires MkDocs (for its YAML frontmatter parser).
SPDX-License-Identifier: MIT
"""

import datetime as dt
import re
from pathlib import Path

import yaml
from mkdocs.utils.meta import get_data

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
TYPES = {"notes": "note", "papers": "paper", "tutorials": "tutorial", "meetings": "meeting"}
STATUS = {"draft", "review", "stable"}
READING = {"skim", "close", "reproduced"}
VERIFIED = {"unverified", "partial", "verified"}
DIFFICULTY = {"入门", "进阶", "高级"}
NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*\.md$")


def as_date(value):
    if isinstance(value, dt.date):
        return value
    try:
        return dt.date.fromisoformat(str(value))
    except ValueError:
        return None


def known(key):
    config = yaml.load((ROOT / "mkdocs.yml").read_text(), Loader=yaml.BaseLoader)
    return {item["id"] for item in config["extra"]["knowledge"][key]}


def check(path, stages, topics):
    relative = path.relative_to(DOCS)
    section, kind = relative.parts[0], TYPES[relative.parts[0]]
    markdown, meta = get_data(path.read_text())
    problems = []

    def need(field, allowed=None):
        value = meta.get(field)
        if value in (None, "", []):
            problems.append(f"缺少字段 `{field}`")
        elif allowed and str(value) not in allowed:
            problems.append(f"`{field}: {value}` 不在允许值 {sorted(allowed)} 中")
        return value

    if not meta:
        return [f"{relative}: 缺少 frontmatter（参见 templates/{kind}.md）"]
    if meta.get("type") != kind:
        problems.append(f"`type` 应为 `{kind}`（由所在目录 {section}/ 决定）")
    for field in ("title", "summary"):
        need(field)
    need("status", STATUS)
    authors = need("authors")
    if authors and not isinstance(authors, list):
        problems.append("`authors` 应为列表，例如 `[张三]`")
    if not as_date(need("created")):
        problems.append("`created` 应为 YYYY-MM-DD 日期")
    if meta.get("stage") and meta["stage"] not in stages:
        problems.append(f"`stage: {meta['stage']}` 不在 {sorted(stages)} 中")
    if meta.get("tags") and not isinstance(meta["tags"], list):
        problems.append("`tags` 应为列表")
    if "〈" in path.read_text():
        problems.append("仍包含模板占位符〈〉")
    if not NAME.match(relative.name) and kind != "meeting":
        problems.append("文件名应使用英文小写字母、数字和连字符")
    heading = re.search(r"^#\s+(.+?)\s*$", markdown, flags=re.M)
    if not heading:
        problems.append("正文缺少一级标题")

    if kind == "note":
        if len(relative.parts) != 3:
            problems.append("主题笔记应放在 docs/notes/<主题目录>/ 下")
        elif relative.parts[1] not in topics:
            problems.append(f"主题目录 `{relative.parts[1]}` 未在 mkdocs.yml 的 extra.knowledge.topics 中登记")
    elif kind == "paper":
        need("reading", READING)
        paper = meta.get("paper")
        if not isinstance(paper, dict):
            problems.append("缺少 `paper` 字段（title、authors、year、url）")
        else:
            for field in ("title", "authors", "year", "url"):
                if not paper.get(field):
                    problems.append(f"缺少字段 `paper.{field}`")
            if paper.get("year") and relative.parts[1] != str(paper["year"]):
                problems.append(f"论文年份 {paper['year']} 与目录 {relative.parts[1]}/ 不一致")
    elif kind == "tutorial":
        need("difficulty", DIFFICULTY)
        need("environment")
        verified = need("verified", VERIFIED)
        if verified == "verified" and not meta.get("verified_on"):
            problems.append("`verified: verified` 时需填写 `verified_on`")
    elif kind == "meeting":
        day = as_date(need("date"))
        need("presenter")
        need("recorder")
        if day and (len(relative.parts) != 3 or relative.parts[1] != str(day.year)
                    or not relative.name.startswith(day.isoformat())):
            problems.append(f"组会记录应保存为 docs/meetings/{day.year}/{day.isoformat()}.md")
    return [f"{relative}: {problem}" for problem in problems]


def main():
    stages, topics = known("stages"), known("topics")
    errors, checked = [], 0
    for section in TYPES:
        for path in sorted((DOCS / section).rglob("*.md")):
            if path.name in {"README.md", "index.md"}:
                continue
            checked += 1
            errors += check(path, stages, topics)
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Checked frontmatter of {checked} content pages: passed")


if __name__ == "__main__":
    main()
