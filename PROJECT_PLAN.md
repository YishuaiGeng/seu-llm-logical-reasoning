# 维护与发布指南

## 项目定位

- 仓库：`seu-llm-logical-reasoning`。
- 名称：SEU 大模型逻辑推理知识库。
- 团队：东南大学大模型逻辑推理学习小组共建，组内成员共同维护。
- 范围：逻辑基础、推理机制、训练与验证、评测与误差分析。
- 内容：主题笔记、论文阅读、实践教程、可公开组会记录与资源索引。

当前正式版使用 MkDocs Material 9.7，原创文档采用 CC BY 4.0，代码采用 MIT，东南大学校徽版权归学校所有。仓库归属与线上地址以 [GitHub](https://github.com/YishuaiGeng/seu-llm-logical-reasoning) 的实际状态为准。

## 文件分工

| 位置 | 用途 |
| --- | --- |
| `docs/` | 网站主要内容和静态素材 |
| `templates/` | 学习、论文、教程和组会模板 |
| `examples/` | 小型可运行教学代码 |
| `overrides/` | 首页、评论区、页脚与 404 模板 |
| `docs/stylesheets/`、`docs/javascripts/` | 自定义视觉样式、本地打包的 KaTeX |
| `docs/assets/brand/` | 项目横幅与东南大学校徽 |
| `includes/abbreviations.md` | 全站缩写悬停提示 |
| `scripts/site_hooks.py` | 发布根目录指南、模板与示例说明；根据 frontmatter 生成导航、栏目索引、学习路线、首页数据、元信息卡片与推导块 |
| `scripts/check_content.py` | 校验内容页 frontmatter |
| `scripts/check_site.py` | 校验构建后的站内链接与锚点 |
| `scripts/run_examples.py` | 运行全部 `examples/*/check_*.py` 自检 |
| `mkdocs.yml` | 固定导航、主题、主题目录与学习阶段、评论区配置 |
| `.github/workflows/` | PR 检查与预览、Pages 发布、每月外部链接巡检 |
| `LICENSE` / `LICENSE-DOCS` | MIT / CC BY 4.0 完整文本 |

目录按用途组织，作者写在 frontmatter。一份内容只有一个主要位置，组会引用论文或教程，不重复复制。

## 自动生成的部分

`mkdocs.yml` 的 `nav` 只列固定页面。“主题笔记”“论文阅读”“实践教程”“组会记录”四个栏目的子页面由 `site_hooks.py` 按目录与 frontmatter 自动展开：笔记按 `extra.knowledge.topics` 分组，论文与组会按年份倒序，教程按 `order` 排序。栏目索引页中的 `<!-- lr:index ... -->` 与入门页中的 `<!-- lr:roadmap -->` 会被替换为自动生成的表格和路线图，首页统计与“最近更新”也来自同一份目录数据。

新增主题目录或学习阶段时，修改 `mkdocs.yml` 的 `extra.knowledge`；`check_content.py` 会拒绝未登记的主题目录。

## 本地构建

要求 Python 3.10+，推荐与 CI 一致使用 Python 3.12。

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
mkdocs serve
```

已经安装 uv 时：

```bash
uv run --python 3.12 --with-requirements requirements.txt mkdocs serve
uv run --python 3.12 --with-requirements requirements.txt mkdocs build --strict
```

生产静态文件生成到 `site/`，不提交到主分支。构建后的页面链接与教程检查：

```bash
python scripts/check_content.py
python scripts/check_site.py
python scripts/run_examples.py   # 需先安装 examples/*/requirements.txt
```

## GitHub Pages 发布

1. 在仓库 Settings → Pages 中将 Source 设为 **GitHub Actions**。
2. 推送到 `main` 后，`Deploy documentation` 工作流执行严格构建并上传站点。
3. GitHub Pages 环境发布构建产物，工作流提供实际网站地址。
4. 也可以在 Actions 页面手动运行该工作流。

`Documentation checks` 对每个 PR 运行 frontmatter 校验、严格构建、链接检查与示例自检，并上传 `site-preview` 构建产物供审阅者下载预览；它是 `main` 分支保护要求的检查。`Deploy documentation` 在推送到 `main` 时重复同样的检查后发布。PR 的检查任务只有读取权限；发布任务仅对主分支开放 Pages 和 OIDC 权限。`External link check` 每月检查一次外部链接，发现失效链接时自动开 Issue。

构建需要完整 Git 历史（`fetch-depth: 0`），页面“更新”日期由最后一次提交时间生成。

## 评论区

页面评论使用 [giscus](https://giscus.app/zh-CN)，每个页面对应仓库 Discussions 中的一条讨论。首次启用需要仓库管理员完成：

1. 安装 [giscus GitHub App](https://github.com/apps/giscus) 并授权本仓库；
2. 建议在 Discussions 中新建“页面评论”分类（格式选 Announcement，只有维护者和 giscus 能新建讨论），在 giscus 网站生成配置，把分类名称与 ID 填入 `mkdocs.yml` 的 `extra.giscus`；未新建分类时默认使用 Announcements。

评论需要 GitHub 账号登录，并会加载 giscus.app 的脚本。首页、模板页与标签页不显示评论；其他页面可在 frontmatter 中写 `comments: false` 关闭。自定义域名与用户统计未引入。搜索索引由静态构建生成，中文分词使用打包的搜索依赖；公式由本地打包的 KaTeX 渲染；Mermaid 图表由 Material 从 unpkg 按需加载；网站不依赖外部字体服务。

## 平台演进

Material for MkDocs 自 2025 年 11 月起进入维护模式，9.7 是最后一个带新功能的版本，关键修复按官方公告延续到 2027 年 5 月。原团队的继任项目 Zensical 兼容现有 `mkdocs.yml`，但尚未发布 1.0。建议在 Zensical 1.0 发布后、2027 年 5 月前评估迁移，重点验证 `scripts/site_hooks.py` 与 `overrides/` 的兼容性。

迁移仓库或更换账号时，同时更新 `mkdocs.yml`、README、`scripts/site_hooks.py` 中的仓库地址与其他绝对 GitHub 链接，并重新检查 Pages 配置。

## 协作与权限

初期由个人账号持有仓库。推荐指定负责人和备份维护者，组员按需要给予 Write 权限，外部贡献者使用 Fork 和 PR。

开启 Issues 和 Discussions。公开仓库可配置 `main` 分支保护：通过 PR、另一位成员审阅、构建通过、禁止强制推送与删除。具体启用状态以仓库 Settings 为准。

角色分工、PR 审阅要点与定期维护事项见[维护手册](docs/community/maintainers.md)。

组会按次轮值记录。会后由汇报人确认技术内容，维护者检查公开范围，再合并发布。明确任务进入 Issues，开放问题进入 Discussions。

<a id="publishing-boundary"></a>

## 公开与内部资料的边界

公开知识库仅收录可以对外分享的内容。内部实验、未发表想法和完整内部会议记录使用独立私有仓库或组内协作空间。

同一仓库的不同文件夹不能设置不同访问权限。当前文件删除后，Git 历史和已发布站点仍可能包含旧内容；误提交时按[安全说明](SECURITY.md)处理。

Pages 是静态阅读入口，提交使用 GitHub 编辑和 PR。私有仓库的 Pages 支持及访问控制取决于套餐与设置，不能默认继承仓库权限。

## 内容维护节奏

- 每次提交：检查来源、内部链接、署名、分享范围。
- 每次组会：整理公开记录，跟进前次行动项。
- 每月：处理链接巡检自动创建的 Issue，合并重复主题，从候选论文中安排认领。
- 更新依赖时：重新构建，检查移动端、深色模式、中文搜索与在线编辑入口。

不虚构论文阅读量、会议记录、实验结果、成员名单或机构背书。尚未形成内容的栏目保留清晰的贡献入口。
