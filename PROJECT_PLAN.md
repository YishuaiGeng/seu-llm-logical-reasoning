# 维护与发布指南

## 项目定位

- 仓库：`seu-llm-logical-reasoning`。
- 名称：SEU 大模型逻辑推理知识库。
- 团队：东南大学肖家军学习小组共建。
- 范围：逻辑基础、推理机制、训练与验证、评测与误差分析。
- 内容：主题笔记、论文阅读、实践教程、可公开组会记录与资源索引。

当前正式版使用 MkDocs Material，原创文档采用 CC BY 4.0，代码采用 MIT。仓库归属与线上地址以 [GitHub](https://github.com/YishuaiGeng/seu-llm-logical-reasoning) 的实际状态为准。

## 文件分工

| 位置 | 用途 |
| --- | --- |
| `docs/` | 网站主要内容和静态素材 |
| `templates/` | 学习、论文、教程和组会模板 |
| `examples/` | 小型可运行教学代码 |
| `overrides/` | 网站首页模板 |
| `docs/stylesheets/` | 自定义视觉样式 |
| `scripts/site_hooks.py` | 将根目录指南与模板发布到网站，避免双份维护 |
| `mkdocs.yml` | 导航、主题、搜索与网站地址 |
| `.github/workflows/` | 构建检查与 Pages 自动发布 |
| `LICENSE` / `LICENSE-DOCS` | MIT / CC BY 4.0 完整文本 |

目录按用途组织，作者写在正文。一份内容只有一个主要位置，组会引用论文或教程，不重复复制。

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
python scripts/check_site.py
python examples/truth-table/check_entailment.py
```

## GitHub Pages 发布

1. 在仓库 Settings → Pages 中将 Source 设为 **GitHub Actions**。
2. 推送到 `main` 后，`Deploy documentation` 工作流执行严格构建并上传站点。
3. GitHub Pages 环境发布构建产物，工作流提供实际网站地址。
4. 也可以在 Actions 页面手动运行该工作流。

`Documentation checks` 对 PR 与主分支运行构建和示例检查。PR 的检查任务只有读取权限；发布任务仅对主分支开放 Pages 和 OIDC 权限。

自定义域名、用户统计和在线评论均未引入。搜索索引由静态构建生成，中文分词使用打包的搜索依赖；网站不依赖外部字体服务。

迁移仓库或更换账号时，同时更新 `mkdocs.yml`、README、`scripts/site_hooks.py` 中的仓库地址与其他绝对 GitHub 链接，并重新检查 Pages 配置。

## 协作与权限

初期由个人账号持有仓库。推荐指定负责人和备份维护者，组员按需要给予 Write 权限，外部贡献者使用 Fork 和 PR。

开启 Issues 和 Discussions。公开仓库可配置 `main` 分支保护：通过 PR、另一位成员审阅、构建通过、禁止强制推送与删除。具体启用状态以仓库 Settings 为准。

组会按次轮值记录。会后由汇报人确认技术内容，维护者检查公开范围，再合并发布。明确任务进入 Issues，开放问题进入 Discussions。

<a id="publishing-boundary"></a>

## 公开与内部资料的边界

公开知识库仅收录可以对外分享的内容。内部实验、未发表想法和完整内部会议记录使用独立私有仓库或组内协作空间。

同一仓库的不同文件夹不能设置不同访问权限。当前文件删除后，Git 历史和已发布站点仍可能包含旧内容；误提交时按[安全说明](SECURITY.md)处理。

Pages 是静态阅读入口，提交使用 GitHub 编辑和 PR。私有仓库的 Pages 支持及访问控制取决于套餐与设置，不能默认继承仓库权限。

## 内容维护节奏

- 每次提交：检查来源、内部链接、署名、分享范围。
- 每次组会：整理公开记录，跟进前次行动项。
- 每月：清理失效链接、合并重复主题、补充学习路线。
- 更新依赖时：重新构建，检查移动端、深色模式、中文搜索与在线编辑入口。

不虚构论文阅读量、会议记录、实验结果、成员名单或机构背书。尚未形成内容的栏目保留清晰的贡献入口。
