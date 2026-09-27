"""MkDocs hooks for the knowledge base.

- Publish root guides, templates and example READMEs without duplicate files.
- Build a content catalog from YAML frontmatter and git history.
- Expand the navigation and section indexes automatically, so adding a
  note, paper, tutorial or meeting only requires adding one Markdown file.
- Render page metadata cards, the learning roadmap and derivation blocks.
- Render the member and publication pages from data/members.yml and
  data/publications.yml.

SPDX-License-Identifier: MIT
"""

import copy
import datetime as dt
import html
import posixpath
import re
import subprocess
from pathlib import Path
from urllib.parse import urlsplit

import yaml
from mkdocs.structure.files import File, InclusionLevel
from mkdocs.utils.meta import get_data

ROOT = Path(__file__).resolve().parents[1]
REPO = "https://github.com/YishuaiGeng/seu-llm-logical-reasoning"
ISSUES = f"{REPO}/issues"

GUIDES = {
    "CONTRIBUTING.md": "community/contributing.md",
    "CODE_OF_CONDUCT.md": "community/code-of-conduct.md",
    "SECURITY.md": "community/security.md",
    "PROJECT_PLAN.md": "community/maintenance.md",
    "CHANGELOG.md": "community/changelog.md",
    "examples/README.md": "tutorials/examples/index.md",
    "templates/README.md": "templates/README.md",
}
TEMPLATES = {
    "note": ("学习笔记模板", "docs/notes/<主题目录>/<英文短名>.md"),
    "paper": ("论文阅读模板", "docs/papers/<论文年份>/<英文短名>.md"),
    "tutorial": ("实践教程模板", "docs/tutorials/<英文短名>.md"),
    "meeting": ("组会记录模板", "docs/meetings/<年份>/<YYYY-MM-DD>.md"),
}
GENERATED = dict(GUIDES)
GENERATED.update({f"templates/{name}.md": f"templates/{name}.md" for name in TEMPLATES})
GENERATED.update({
    f"examples/{path.parent.name}/README.md": f"tutorials/examples/{path.parent.name}.md"
    for path in sorted((ROOT / "examples").glob("*/README.md"))
})
SOURCES = {destination: source for source, destination in GENERATED.items()}

CONTENT_TYPES = {"notes": "note", "papers": "paper", "tutorials": "tutorial", "meetings": "meeting"}
TYPE_LABELS = {"note": "主题笔记", "paper": "论文阅读", "tutorial": "实践教程", "meeting": "组会记录"}
STATUS_LABELS = {"draft": "草稿", "review": "待审阅", "stable": "已整理"}
VERIFIED_LABELS = {"unverified": "未验证", "partial": "部分验证", "verified": "已验证"}
READING_LABELS = {"skim": "初读", "close": "精读", "reproduced": "已复现部分实验"}

LINK = re.compile(r"(!?\[[^\]]*\]\()([^\s)]+)(\))")
FENCE = re.compile(r"^(\s*)(`{3,}|~{3,})\s*([\w-]*)")
MARKER = re.compile(r"<!--\s*lr:(index|roadmap|members|publications)\s*(\w*)\s*-->")

DATA = ROOT / "data"
# 投稿状态按展示顺序排列；键名用于 data/publications.yml 的 status 字段。
PUB_STATUS = {
    "published": "已发表", "accepted": "已录用", "preprint": "预印本", "revision": "修改中",
    "under-review": "审稿中", "submitted": "已投稿", "preparing": "准备中",
}
PUB_TYPES = {"conference": "会议论文", "journal": "期刊论文", "workshop": "研讨会论文", "preprint": "预印本", "other": "其他"}
PUB_LINKS = {"paper": "论文", "arxiv": "arXiv", "code": "代码", "slides": "报告", "project": "项目主页"}

CATALOG = {}


# ---------------------------------------------------------------- utilities

def split_fences(markdown):
    """Yield (is_code, text) segments; nested fences stay inside their parent."""
    segments, buffer, fence = [], [], None
    for line in markdown.splitlines(keepends=True):
        match = FENCE.match(line)
        if fence is None and match:
            if buffer:
                segments.append((False, "".join(buffer)))
            buffer, fence = [line], match.group(2)
        elif fence is not None:
            buffer.append(line)
            stripped = line.strip()
            if stripped and set(stripped) == {fence[0]} and len(stripped) >= len(fence):
                segments.append((True, "".join(buffer)))
                buffer, fence = [], None
        else:
            buffer.append(line)
    if buffer:
        segments.append((fence is not None, "".join(buffer)))
    return segments


def map_prose(markdown, function):
    return "".join(text if code else function(text) for code, text in split_fences(markdown))


def as_date(value):
    if isinstance(value, dt.datetime):
        return value.date()
    if isinstance(value, dt.date):
        return value
    try:
        return dt.date.fromisoformat(str(value))
    except ValueError:
        return None


def as_list(value):
    if not value:
        return []
    return [str(item) for item in value] if isinstance(value, (list, tuple)) else [str(value)]


def git_history():
    """Map repository paths to their (created, updated) commit dates."""
    try:
        log = subprocess.run(
            ["git", "log", "--format=@%cs", "--name-only", "--no-renames"],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError):
        return {}
    dates, current = {}, None
    for line in log.splitlines():
        if line.startswith("@"):
            current = as_date(line[1:])
        elif line and current:
            created, updated = dates.get(line, (current, current))
            dates[line] = (min(created, current), max(updated, current))
    return dates


def reading_minutes(markdown):
    text = re.sub(r"```.*?```", "", markdown, flags=re.S)
    cjk = len(re.findall(r"[一-鿿]", text))
    words = len(re.findall(r"[A-Za-z]+", text))
    return max(1, round(cjk / 400 + words / 220))


def first_heading(markdown):
    match = re.search(r"^#\s+(.+?)\s*$", markdown, flags=re.M)
    return match.group(1) if match else None


def relative_url(target_url, page_url):
    base = page_url if page_url.endswith("/") or not page_url else posixpath.dirname(page_url) + "/"
    path = posixpath.relpath(target_url or ".", base or ".")
    return path + "/" if target_url.endswith("/") and not path.endswith("/") else path


def relative_md(target_src, page_src):
    return posixpath.relpath(target_src, posixpath.dirname(page_src) or ".")


def esc(value):
    return html.escape(str(value), quote=True)


# ------------------------------------------------------------------- events

def on_files(files, config):
    for source, destination in GENERATED.items():
        name = Path(source).stem
        if source.startswith("templates/") and name in TEMPLATES:
            content = wrap_template(name, (ROOT / source).read_text())
        else:
            content = (ROOT / source).read_text()
        generated = File.generated(
            config, destination, content=content, inclusion=InclusionLevel.INCLUDED,
        )
        generated.edit_uri = source
        files.append(generated)

    build_catalog(files, config)
    config["nav"] = expand_nav(copy.deepcopy(config["nav"]), config)
    return files


def on_page_markdown(markdown, page, config, files):
    uri = page.file.src_uri
    source = SOURCES.get(uri, f"docs/{uri}")
    if uri in SOURCES:
        page.edit_url = f"{REPO}/edit/main/{source}"
    if page.meta.get("edit_source"):
        page.edit_url = f"{REPO}/edit/main/{page.meta['edit_source']}"

    wrapped_template = uri.startswith("templates/") and Path(uri).stem in TEMPLATES
    if not wrapped_template:
        markdown = map_prose(markdown, lambda text: LINK.sub(
            lambda match: rewrite_link(match, source, uri), text))
    markdown = render_derivations(markdown)
    markdown = map_prose(markdown, lambda text: MARKER.sub(
        lambda match: render_marker(match, page, config), text))

    entry = CATALOG.get(uri)
    if entry:
        markdown = insert_after_heading(markdown, metadata_card(entry, markdown))

    # Material reserves `status` for navigation icons; keep ours under another key.
    if "status" in page.meta:
        page.meta["lr_status"] = page.meta.pop("status")
    commentable = uri not in {"index.md", "tags.md"} and not uri.startswith("templates/")
    page.meta.setdefault("comments", commentable)
    return markdown


# ------------------------------------------------------------------ catalog

def build_catalog(files, config):
    CATALOG.clear()
    dates = git_history()
    for file in files.documentation_pages():
        section = file.src_uri.split("/", 1)[0]
        if section not in CONTENT_TYPES or Path(file.src_uri).name in {"README.md", "index.md"}:
            continue
        if file.src_uri in SOURCES:
            continue
        markdown, meta = get_data(file.content_string)
        created, updated = dates.get(f"docs/{file.src_uri}", (None, None))
        CATALOG[file.src_uri] = {
            "src": file.src_uri,
            "url": file.url,
            "type": CONTENT_TYPES[section],
            "title": meta.get("title") or first_heading(markdown) or Path(file.src_uri).stem,
            "meta": meta,
            "topic": file.src_uri.split("/")[1] if section == "notes" and file.src_uri.count("/") > 1 else None,
            "created": as_date(meta.get("created")) or created,
            "updated": updated or as_date(meta.get("created")),
            "minutes": reading_minutes(markdown),
        }

    entries = list(CATALOG.values())
    recent = sorted(entries, key=lambda e: (e["updated"] or dt.date.min, e["title"]), reverse=True)[:5]
    stages = config["extra"].get("knowledge", {}).get("stages", [])
    config["extra"]["catalog"] = {
        "counts": {kind: sum(e["type"] == kind for e in entries) for kind in TYPE_LABELS},
        "recent": [{
            "title": e["title"], "url": e["url"], "label": TYPE_LABELS[e["type"]],
            "summary": e["meta"].get("summary", ""),
            "updated": e["updated"].isoformat() if e["updated"] else "",
        } for e in recent],
        "members": len(load_data("members").get("members") or []),
        "publications": [{
            "title": pub_title(p), "venue": p.get("venue", ""), "date": str(p.get("date", "")),
            "status": p.get("status"), "label": PUB_STATUS.get(p.get("status"), ""),
        } for p in sorted_publications()[:3]],
        "stages": [{
            "title": stage["title"],
            "count": sum(e["meta"].get("stage") == stage["id"] for e in entries),
        } for stage in stages],
    }


def sort_key(entry):
    meta = entry["meta"]
    return (meta.get("order", 999), entry["created"] or dt.date.max, entry["title"])


def expand_nav(nav, config):
    topics = {t["id"]: t["title"] for t in config["extra"].get("knowledge", {}).get("topics", [])}
    for index, item in enumerate(nav):
        if isinstance(item, dict):
            (title, value), = item.items()
            if isinstance(value, list):
                item[title] = expand_nav(value, config)
            elif isinstance(value, str) and value.endswith("/README.md"):
                section = value.split("/", 1)[0]
                if section in CONTENT_TYPES:
                    item[title] = [value] + section_children(CONTENT_TYPES[section], topics)
        nav[index] = item
    return nav


def section_children(kind, topics):
    entries = [e for e in CATALOG.values() if e["type"] == kind]
    if kind == "note":
        loose = [e["src"] for e in sorted(entries, key=sort_key) if not e["topic"]]
        grouped = []
        for topic in list(topics) + sorted({e["topic"] for e in entries} - set(topics)):
            pages = [e["src"] for e in sorted(entries, key=sort_key) if e["topic"] == topic]
            if pages:
                grouped.append({topics.get(topic, topic): pages})
        return loose + grouped
    if kind in {"paper", "meeting"}:
        by_year = {}
        newest = sorted(entries, key=lambda e: (event_date(e) or dt.date.min, e["title"]), reverse=True)
        for entry in newest:
            by_year.setdefault(entry["src"].split("/")[1], []).append(entry["src"])
        return [{year: pages} for year, pages in by_year.items()]
    children = [e["src"] for e in sorted(entries, key=sort_key)]
    examples = [d for d in sorted(SOURCES) if d.startswith("tutorials/examples/") and not d.endswith("index.md")]
    return children + [{"示例代码": ["tutorials/examples/index.md"] + examples}]


def event_date(entry):
    meta = entry["meta"]
    if entry["type"] == "meeting":
        return as_date(meta.get("date"))
    paper = meta.get("paper") or {}
    year = paper.get("year")
    return dt.date(int(year), 1, 1) if str(year).isdigit() else entry["created"]


# ---------------------------------------------------------------- rendering

def wrap_template(name, raw):
    title, target = TEMPLATES[name]
    fence = "`" * max(4, max((len(m) for m in re.findall(r"`{3,}", raw)), default=0) + 1)
    return (
        f"# {title}\n\n"
        f"复制下方全部内容，保存为 `{target}`，然后逐项替换〈〉中的占位文字。"
        "文件开头两条 `---` 之间的 frontmatter 会被网站读取，用来生成导航、栏目索引、元信息卡片和标签；"
        "字段含义见[贡献指南](../community/contributing.md#frontmatter)。\n\n"
        f"{fence}markdown\n{raw.rstrip()}\n{fence}\n"
    )


def rewrite_link(match, source, uri):
    target = match.group(2)
    parsed = urlsplit(target)
    if parsed.scheme or parsed.netloc or not parsed.path or target.startswith("/"):
        return match.group(0)
    resolved = posixpath.normpath(posixpath.join(posixpath.dirname(source), parsed.path))
    if resolved in GENERATED:
        destination = GENERATED[resolved]
    elif resolved.startswith("docs/"):
        destination = resolved[5:]
    elif (ROOT / resolved).exists():
        kind = "tree" if (ROOT / resolved).is_dir() else "blob"
        return match.group(1) + f"{REPO}/{kind}/main/{resolved}" + (
            f"#{parsed.fragment}" if parsed.fragment else ""
        ) + match.group(3)
    else:
        return match.group(0)
    rewritten = posixpath.relpath(destination, posixpath.dirname(uri) or ".")
    if parsed.fragment:
        rewritten += f"#{parsed.fragment}"
    return match.group(1) + rewritten + match.group(3)


def render_derivations(markdown):
    """Turn ```derivation fences into proof cards.

    Lines before a `---` rule are premises, the text after `---` names the
    rule, and lines after it are conclusions. Prefix the rule with `!` to mark
    an invalid inference.
    """
    output = []
    for code, text in split_fences(markdown):
        lines = text.splitlines()
        if not code or FENCE.match(lines[0]).group(2) != "```" or FENCE.match(lines[0]).group(3) != "derivation":
            output.append(text)
            continue
        indent = FENCE.match(lines[0]).group(1)
        body = [line.strip() for line in lines[1:-1] if line.strip()]
        rule_index = next((i for i, line in enumerate(body) if line.startswith("---")), len(body))
        premises, conclusions = body[:rule_index], body[rule_index + 1:]
        rule = body[rule_index].lstrip("-").strip() if rule_index < len(body) else ""
        invalid = rule.startswith("!")
        rule = rule.lstrip("!").strip()
        label = f"推导：由 {'；'.join(premises)} 推出 {'；'.join(conclusions)}"
        label += f"（{'无效' if invalid else ''}{rule}）" if rule else ""
        output.append(
            f'{indent}<div class="lr-derivation{" lr-derivation--invalid" if invalid else ""}" role="figure" aria-label="{esc(label)}">'
            f'<div class="lr-derivation__premises">{"".join(f"<span>{esc(p)}</span>" for p in premises)}</div>'
            f'<div class="lr-derivation__rule"><span>{"无效 · " if invalid else ""}{esc(rule)}</span></div>'
            f'<div class="lr-derivation__conclusion"><span class="lr-derivation__therefore">{"⊭" if invalid else "∴"}</span> '
            f'{"<br>".join(esc(c) for c in conclusions)}</div></div>\n'
        )
    return "".join(output)


def insert_after_heading(markdown, block):
    match = re.search(r"^#\s+.+$", markdown, flags=re.M)
    if not match:
        return block + "\n\n" + markdown
    return markdown[:match.end()] + "\n\n" + block + "\n" + markdown[match.end():]


def metadata_card(entry, markdown):
    meta, kind = entry["meta"], entry["type"]
    status = str(meta.get("status", ""))
    chips = [f'<span class="lr-chip lr-chip--type">{TYPE_LABELS[kind]}</span>']
    if status in STATUS_LABELS:
        chips.append(f'<span class="lr-chip lr-chip--{status}">{STATUS_LABELS[status]}</span>')
    facts = []
    authors = as_list(meta.get("authors"))
    if authors:
        facts.append(("作者", "、".join(authors)))
    contributors = as_list(meta.get("contributors"))
    if contributors:
        facts.append(("贡献者", "、".join(contributors)))
    if kind == "tutorial":
        facts += [(k, meta[f]) for k, f in (("难度", "difficulty"), ("环境", "environment")) if meta.get(f)]
        verified = VERIFIED_LABELS.get(str(meta.get("verified")))
        if verified:
            chips.append(f'<span class="lr-chip lr-chip--verified-{meta["verified"]}">{verified}</span>')
    if kind == "meeting":
        facts += [(k, meta[f]) for k, f in (("日期", "date"), ("汇报人", "presenter"), ("记录人", "recorder")) if meta.get(f)]
    if entry["created"]:
        facts.append(("创建", entry["created"].isoformat()))
    if entry["updated"] and entry["updated"] != entry["created"]:
        facts.append(("更新", entry["updated"].isoformat()))
    facts.append(("阅读", f"约 {entry['minutes']} 分钟"))

    card = (
        '<div class="lr-meta">'
        f'<div class="lr-meta__chips">{"".join(chips)}</div>'
        '<dl class="lr-meta__facts">'
        + "".join(f"<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>" for k, v in facts)
        + "</dl></div>"
    )
    paper = meta.get("paper") if kind == "paper" else None
    if isinstance(paper, dict):
        rows = [
            ("原文", f'<a href="{esc(paper["url"])}">{esc(paper.get("title", "原文链接"))}</a>' if paper.get("url") else esc(paper.get("title", ""))),
            ("原文作者", esc("、".join(as_list(paper.get("authors"))))),
            ("年份与版本", esc(" · ".join(str(paper[k]) for k in ("year", "venue") if paper.get(k)))),
            ("代码与数据", f'<a href="{esc(paper["code"])}">{esc(paper["code"])}</a>' if paper.get("code") else "未提供"),
            ("阅读状态", esc(READING_LABELS.get(str(meta.get("reading")), meta.get("reading", "")))),
        ]
        card += '<dl class="lr-paper">' + "".join(
            f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in rows if v) + "</dl>"
    return card


def render_marker(match, page, config):
    kind, argument = match.groups()
    if kind == "members":
        return render_members(page)
    if kind == "publications":
        return render_publications()
    if kind == "roadmap":
        return render_roadmap(page, config)
    return render_index(argument, page, config)


def render_index(section, page, config):
    kind = CONTENT_TYPES.get(section)
    if not kind:
        return f"<!-- unknown index {section} -->"
    entries = [e for e in CATALOG.values() if e["type"] == kind]
    link = lambda e: f"[{e['title']}]({relative_md(e['src'], page.file.src_uri)})"
    status = lambda e: STATUS_LABELS.get(str(e["meta"].get("status")), "—")
    claim = f"[认领选题]({ISSUES}?q=is%3Aopen+label%3A%22good+first+issue%22)"

    if kind == "note":
        topics = config["extra"].get("knowledge", {}).get("topics", [])
        known = {t["id"] for t in topics}
        extra = sorted({e["topic"] or "" for e in entries} - known)
        blocks = []
        for topic in topics + [{"id": t, "title": t or "其他", "summary": ""} for t in extra]:
            rows = sorted((e for e in entries if (e["topic"] or "") == topic["id"]), key=sort_key)
            blocks.append(f"### {topic['title']}\n\n" + (f"{topic['summary']}\n\n" if topic.get("summary") else ""))
            if rows:
                blocks[-1] += "| 笔记 | 你会理解什么 | 状态 |\n| --- | --- | --- |\n" + "".join(
                    f"| {link(e)} | {e['meta'].get('summary', '')} | {status(e)} |\n" for e in rows)
            else:
                template = relative_md("templates/note.md", page.file.src_uri)
                blocks[-1] += f"本主题的笔记正在整理中，可{claim}或使用[学习笔记模板]({template})撰写。\n"
        return "\n".join(blocks)

    if not entries:
        empty = {
            "paper": "论文精读笔记正在整理中。",
            "meeting": "当前尚未归档公开的组会记录。",
            "tutorial": "教程正在整理中。",
        }[kind]
        return f'!!! note "尚无内容"\n\n    {empty}新增内容后本表自动更新。\n'

    if kind == "paper":
        rows = sorted(entries, key=lambda e: (event_date(e) or dt.date.min, e["title"]), reverse=True)
        return "| 论文 | 年份 | 阅读人 | 阅读状态 | 笔记状态 |\n| --- | --- | --- | --- | --- |\n" + "".join(
            f"| {link(e)} | {(e['meta'].get('paper') or {}).get('year', '—')} | {'、'.join(as_list(e['meta'].get('authors')))} "
            f"| {READING_LABELS.get(str(e['meta'].get('reading')), '—')} | {status(e)} |\n" for e in rows)
    if kind == "meeting":
        rows = sorted(entries, key=lambda e: (event_date(e) or dt.date.min), reverse=True)
        return "| 日期 | 主题 | 汇报人 | 记录人 |\n| --- | --- | --- | --- |\n" + "".join(
            f"| {e['meta'].get('date', '—')} | {link(e)} | {e['meta'].get('presenter', '—')} | {e['meta'].get('recorder', '—')} |\n"
            for e in rows)
    rows = sorted(entries, key=sort_key)
    return "| 教程 | 你会完成什么 | 难度 | 环境 | 验证状态 |\n| --- | --- | --- | --- | --- |\n" + "".join(
        f"| {link(e)} | {e['meta'].get('summary', '')} | {e['meta'].get('difficulty', '—')} | {e['meta'].get('environment', '—')} "
        f"| {VERIFIED_LABELS.get(str(e['meta'].get('verified')), '—')} |\n" for e in rows)


def render_roadmap(page, config):
    stages = config["extra"].get("knowledge", {}).get("stages", [])
    items = []
    for number, stage in enumerate(stages, 1):
        entries = sorted((e for e in CATALOG.values() if e["meta"].get("stage") == stage["id"]),
                         key=lambda e: (list(TYPE_LABELS).index(e["type"]), sort_key(e)))
        links = "".join(
            f'<li><a href="{esc(relative_url(e["url"], page.url))}"><span>{TYPE_LABELS[e["type"]]}</span>{esc(e["title"])}</a></li>'
            for e in entries
        ) or f'<li class="lr-roadmap__empty"><a href="{ISSUES}?q=is%3Aopen+label%3A%22good+first+issue%22">内容建设中 · 可认领撰写</a></li>'
        state = "lr-roadmap__stage--ready" if entries else ""
        items.append(
            f'<li class="lr-roadmap__stage {state}"><div class="lr-roadmap__marker">{number:02d}</div>'
            f'<div class="lr-roadmap__body"><h3>{esc(stage["title"])}</h3><p>{esc(stage.get("summary", ""))}</p>'
            f'<ul>{links}</ul></div></li>'
        )
    return f'<ol class="lr-roadmap">{"".join(items)}</ol>\n'


# ------------------------------------------------------ members & outputs

def load_data(name):
    path = DATA / f"{name}.yml"
    return (yaml.safe_load(path.read_text()) or {}) if path.exists() else {}


def member_names():
    names = set()
    for member in load_data("members").get("members") or []:
        names.update(str(member[k]) for k in ("name", "name_en") if member.get(k))
    return names


def initials(name):
    name = str(name).strip()
    if re.match(r"[一-鿿]", name):
        return name[0]
    return "".join(part[0] for part in name.split()[:2]).upper()


def render_members(page):
    data = load_data("members")
    groups, members = data.get("groups") or [], data.get("members") or []
    if not members:
        return '!!! note "成员信息"\n\n    成员信息正在整理中。\n'
    blocks = []
    known = [g["id"] for g in groups]
    for group in groups + [{"id": g, "title": "其他成员"} for g in sorted({m.get("group") for m in members} - set(known))]:
        people = [m for m in members if m.get("group") == group["id"]]
        if people:
            cards = "".join(member_card(m, page) for m in people)
            blocks.append(f'## {group["title"]} {{#{group["id"]}}}\n\n<div class="lr-members">{cards}</div>\n')
    return "\n".join(blocks)


def member_card(member, page):
    if member.get("avatar"):
        avatar = f'<img src="{esc(relative_url(member["avatar"], page.url))}" alt="{esc(member["name"])}" loading="lazy">'
    else:
        avatar = f'<span aria-hidden="true">{esc(initials(member["name"]))}</span>'
    english = f' <span class="lr-member__en">{esc(member["name_en"])}</span>' if member.get("name_en") else ""
    position = " · ".join(esc(x) for x in (member.get("position"), member.get("cohort")) if x)
    role = f'<span class="lr-chip lr-chip--type">{esc(member["role"])}</span>' if member.get("role") else ""
    tags = "".join(f"<li>{esc(t)}</li>" for t in member.get("research") or [])
    links = []
    if member.get("homepage"):
        links.append(f'<a href="{esc(member["homepage"])}">个人主页</a>')
    if member.get("github"):
        links.append(f'<a href="https://github.com/{esc(member["github"])}">GitHub</a>')
    if member.get("scholar"):
        links.append(f'<a href="{esc(member["scholar"])}">Google Scholar</a>')
    if member.get("email"):
        links.append(f'<span>{esc(member["email"])}</span>')
    return (
        f'<article class="lr-member"><div class="lr-member__avatar">{avatar}</div><div class="lr-member__body">'
        f'<h3>{esc(member["name"])}{english}</h3>'
        + (f'<p class="lr-member__position">{position}</p>' if position else "")
        + (f'<div class="lr-member__role">{role}</div>' if role else "")
        + (f'<ul class="lr-member__tags">{tags}</ul>' if tags else "")
        + (f'<p class="lr-member__links">{" · ".join(links)}</p>' if links else "")
        + "</div></article>"
    )


def pub_date(pub):
    value = str(pub.get("date", ""))
    return value if re.match(r"^\d{4}-\d{2}(-\d{2})?$", value) else "0000-00"


def sorted_publications():
    return sorted(load_data("publications").get("publications") or [], key=pub_date, reverse=True)


def pub_title(pub):
    return pub.get("title", "") if pub.get("public", True) else "论文（题目暂不公开）"


def render_publications():
    items = sorted_publications()
    if not items:
        return '!!! note "研究成果"\n\n    暂无公开的研究成果。成果在获得全体作者同意后发布于此。\n'
    members = member_names()
    counts = {status: sum(p.get("status") == status for p in items) for status in PUB_STATUS}
    filters = '<button type="button" class="lr-pub-filter is-active" data-filter="all">全部 <span>' + str(len(items)) + "</span></button>" + "".join(
        f'<button type="button" class="lr-pub-filter" data-filter="{status}">{label} <span>{counts[status]}</span></button>'
        for status, label in PUB_STATUS.items() if counts[status]
    )
    years = {}
    for pub in items:
        years.setdefault(pub_date(pub)[:4], []).append(pub)
    sections = []
    for year, pubs in years.items():
        rows = "".join(publication_item(p, members) for p in pubs)
        heading = year if year != "0000" else "日期待定"
        sections.append(f'<section class="lr-pub-year"><h2 class="lr-pub-year__title">{heading}</h2><ol class="lr-pubs">{rows}</ol></section>')
    return f'<div class="lr-pub-filters" role="group" aria-label="按状态筛选">{filters}</div>\n' + "".join(sections) + "\n"


def publication_item(pub, members):
    status = pub.get("status", "")
    public = pub.get("public", True)
    authors = ""
    if public and pub.get("authors"):
        names = [f"<strong>{esc(a)}</strong>" if str(a).rstrip("*†") in members else esc(a) for a in as_list(pub["authors"])]
        authors = f'<p class="lr-pub__authors">{", ".join(names)}</p>'
    links = " · ".join(
        f'<a href="{esc(url)}">{PUB_LINKS.get(key, key)}</a>' for key, url in (pub.get("links") or {}).items() if url
    ) if public else ""
    meta = [f'<span class="lr-pub-status lr-pub-status--{esc(status)}">{PUB_STATUS.get(status, status)}</span>']
    if pub.get("type"):
        meta.append(f"<span>{PUB_TYPES.get(pub['type'], pub['type'])}</span>")
    if pub.get("date"):
        meta.append(f"<time>{esc(pub['date'])}</time>")
    return (
        f'<li class="lr-pub" data-status="{esc(status)}"><div class="lr-pub__meta">{"".join(meta)}</div>'
        f'<h3 class="lr-pub__title{"" if public else " lr-pub__title--private"}">{esc(pub_title(pub))}</h3>'
        + authors
        + (f'<p class="lr-pub__venue">{esc(pub["venue"])}</p>' if pub.get("venue") else "")
        + (f'<p class="lr-pub__links">{links}</p>' if links else "")
        + (f'<p class="lr-pub__note">{esc(pub["note"])}</p>' if pub.get("note") else "")
        + "</li>"
    )
