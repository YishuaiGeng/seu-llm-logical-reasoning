<p align="center">
  <img src="docs/assets/brand/banner.svg" alt="SEU LLM Logical Reasoning — Foundations. Evidence. Practice. Together." width="100%">
</p>

<h1 align="center">SEU 大模型逻辑推理知识库</h1>

<p align="center">肖家军学习小组共建 · 逻辑基础 · 论文共读 · 实践教程 · 组会记录</p>

<p align="center">
  <a href="https://yishuaigeng.github.io/seu-llm-logical-reasoning/">阅读网站</a> ·
  <a href="docs/getting-started/README.md">开始学习</a> ·
  <a href="CONTRIBUTING.md">参与共建</a> ·
  <a href="https://github.com/YishuaiGeng/seu-llm-logical-reasoning/discussions">讨论交流</a>
</p>

<p align="center">
  <a href="https://github.com/YishuaiGeng/seu-llm-logical-reasoning/actions/workflows/ci.yml"><img src="https://github.com/YishuaiGeng/seu-llm-logical-reasoning/actions/workflows/ci.yml/badge.svg" alt="Documentation and example checks"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/code-MIT-234f3e" alt="Code: MIT License"></a>
  <a href="LICENSE-DOCS"><img src="https://img.shields.io/badge/docs-CC_BY_4.0-98753e" alt="Documentation: CC BY 4.0"></a>
</p>

## 关于这个项目

本知识库由东南大学课题组成员共同维护，聚焦**大模型的逻辑推理能力**：模型能否依据前提可靠地推导结论？什么训练与推理机制有帮助？怎样用可检验的证据评估这些能力？

我们将主题笔记、论文阅读、可运行教程与组会讨论连接起来，让个人理解成为可追溯、可修订的共同积累。项目由学习小组维护，SEU 用于说明成员背景。

## 从一个问题开始

**答案正确，推理就有效吗？**

- 阅读 [蕴涵、有效性与反例](docs/notes/logic-foundations/implication-and-entailment.md)，区分命题真值、推理有效性与论证健全性。
- 跟随 [真值表教程](docs/tutorials/truth-table.md)，用 Python 找到一个无效推理的反例。
- 参考 [论文阅读方法](docs/getting-started/reading-guide.md)，把结论、证据与个人假设分开记录。

## 知识导航

| 栏目 | 内容 | 入口 |
| --- | --- | --- |
| 开始学习 | 学习路线、研究范围与阅读方法 | [入门指南](docs/getting-started/README.md) |
| 主题笔记 | 逻辑基础、推理方法、训练与评测 | [浏览笔记](docs/notes/README.md) |
| 论文阅读 | 问题、方法、证据、局限与复现记录 | [论文索引](docs/papers/README.md) |
| 实践教程 | 有环境说明与验证结果的动手教程 | [教程索引](docs/tutorials/README.md) |
| 组会记录 | 汇报材料、讨论分歧与后续行动 | [会议索引](docs/meetings/README.md) |
| 资源导航 | 逻辑教材、论文检索与形式化工具 | [资源索引](docs/resources/README.md) |

## 如何参与

1. 选择一个小问题，复制[对应模板](templates/README.md)。
2. 在自己的分支编写内容，标注来源和待验证之处。
3. 提交 Pull Request，由另一位成员审阅后合并。
4. 合并后网站自动更新；长期问题通过 Issues 跟踪。

可以直接使用 GitHub 网页编辑。论文推荐和开放讨论放在 Discussions，错误报告与明确任务放在 Issues。完整要求见[贡献指南](CONTRIBUTING.md)与[行为准则](CODE_OF_CONDUCT.md)。

## 本地预览

需要 Python 3.10+。以下命令在仓库根目录运行：

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
mkdocs serve
```

Windows 激活命令为 `.venv\Scripts\activate`。浏览器打开终端给出的本地地址。已经安装 `uv` 时，也可以使用：

```bash
uv run --python 3.12 --with-requirements requirements.txt mkdocs serve
```

构建与示例检查：

```bash
mkdocs build --strict
python scripts/check_site.py
python examples/truth-table/check_entailment.py
```

部署方式、文件分工和维护约定见[维护指南](PROJECT_PLAN.md)。文档网站使用 [MkDocs Material](https://squidfunk.github.io/mkdocs-material/)，通过 GitHub Actions 发布到 GitHub Pages。

## 开放内容与许可

- **原创文档、笔记与项目自绘图形**：采用 [CC BY 4.0](LICENSE-DOCS)，允许分享与改编，须署名、链接许可证并标注修改。
- **代码、脚本与网站模板**：采用 [MIT License](LICENSE)。
- 第三方材料遵循其原有许可；不默认纳入本项目授权。许可不授予校名、校徽或其他商标使用权，也不表示学校背书。

引用具体笔记时，请保留作者、标题、来源链接及可识别的版本。完整范围与署名示例见[许可说明](docs/community/license.md)。内部讨论与未发表资料应保存在独立私有空间，不提交到公开知识库。
