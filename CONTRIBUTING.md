# 贡献指南

## 选择位置与模板

先查看[内容边界](docs/getting-started/scope.md)，然后复制[对应模板](templates/README.md)。

| 内容 | 路径示例 |
| --- | --- |
| 主题笔记 | `docs/notes/logic-foundations/deduction-induction-abduction.md` |
| 论文阅读 | `docs/papers/2026/short-paper-title.md` |
| 教程 | `docs/tutorials/run-a-logic-evaluation.md` |
| 组会 | `docs/meetings/2026/2026-09-10.md` |
| 示例代码 | `examples/logic-evaluation/` |

小组成员与研究成果不使用 Markdown 文件，分别登记在 `data/members.yml` 与 `data/publications.yml` 中，字段说明见文件开头的注释与[维护手册](docs/community/maintainers.md)。

以上仅为命名示例，不表示已有对应论文或会议。主题笔记按 `docs/notes/<主题目录>/` 归档，主题目录列表见 `mkdocs.yml` 的 `extra.knowledge.topics`。论文目录年份按论文发表或预印本年份组织；组会按实际发生日期组织，同日多场会议可加主题后缀。

文件名使用简短英文小写和连字符，正文以中文为主，保留必要英文术语。署名写在 frontmatter 的 `authors` 中；更新已有笔记时保留原作者，并把自己加入 `contributors`。

**新增内容只需新建这一个文件。** 导航、栏目索引、学习路线、首页统计、元信息卡片和标签页都会根据 frontmatter 自动生成，不需要修改 `mkdocs.yml` 或索引页。

<a id="frontmatter"></a>

## 填写 frontmatter

每篇笔记、论文、教程和组会记录都以一段 YAML 元信息开头，位于两条 `---` 之间。模板里已经列出全部字段。

| 字段 | 适用 | 说明 |
| --- | --- | --- |
| `title` | 全部 | 标题，与正文一级标题一致。 |
| `type` | 全部 | `note` / `paper` / `tutorial` / `meeting`，须与所在目录一致。 |
| `authors` | 全部 | 作者列表，例如 `[张三]`；组会填记录人。 |
| `contributors` | 可选 | 后续修订者列表。 |
| `status` | 全部 | `draft` 草稿 / `review` 待审阅 / `stable` 已整理。 |
| `created` | 全部 | 创建日期 `YYYY-MM-DD`。更新日期由 Git 历史自动生成，无需手填。 |
| `summary` | 全部 | 一句话摘要，显示在索引和首页“最近更新”中。 |
| `stage` | 笔记、论文、教程 | 学习阶段：`logic` / `llm` / `methods` / `training` / `evaluation`，用于汇总学习路线。 |
| `tags` | 可选 | 标签列表，出现在[标签索引](docs/tags.md)。 |
| `order` | 可选 | 同一栏目内的排序数字，越小越靠前。 |
| `paper` | 论文 | `title`、`authors`、`year`、`url` 必填，`venue`、`code` 可选。 |
| `reading` | 论文 | `skim` 初读 / `close` 精读 / `reproduced` 已复现部分实验。 |
| `difficulty` / `environment` | 教程 | 难度（入门 / 进阶 / 高级）与运行环境。 |
| `verified` | 教程 | `unverified` 未验证 / `partial` 部分验证 / `verified` 已验证；已验证时用 `verified_on` 记录日期与环境。 |
| `date` / `presenter` / `recorder` | 组会 | 开会日期、汇报人、记录人。 |
| `comments` | 可选 | 设为 `false` 可关闭本页评论区。 |

CI 会运行 `scripts/check_content.py` 检查这些字段；缺失或取值错误时，检查结果会指出文件和字段。

## 写作组件

- **四类陈述**：`!!! claim "原文结论"`、`!!! reproduced "复现观察"`、`!!! insight "个人理解"`、`!!! hypothesis "待验证假设"`。
- **推导块**：`derivation` 代码块中，`---` 之前是前提，`---` 后面写规则名，之后是结论；规则名前加 `!` 表示无效推理。
- **公式**：行内 `$\Gamma \models \varphi$`，独立公式用 `$$ ... $$`。
- **脚注**：`[^1]` 引用、`[^1]: 来源` 定义，适合标注出处。
- **流程图**：`mermaid` 代码块。

效果示例见[阅读与验证方法](docs/getting-started/reading-guide.md)与[蕴涵、有效性与反例](docs/notes/logic-foundations/implication-and-entailment.md)。

## GitHub 网页提交

1. 进入仓库，切换到一个新分支。
2. 复制模板，新建相应路径的文件；上传附件时放到对应主题的 `docs/assets/` 子目录。
3. 编辑内容，并使用 Preview 查看渲染效果。
4. 提交到自己的分支，创建面向 `main` 的 PR。
5. PR 检查完成后，可以在检查结果页下载 `site-preview` 构建产物，解压后在浏览器中打开 `index.html` 预览。
6. 根据审阅意见修改，由维护者合并。

有 Write 权限的组员直接在共享仓库创建分支即可。没有写权限的公开仓库贡献者可使用 Fork；私有仓库需先获得访问权限。

## 本地提交

以下示例假定已经克隆仓库，并处于干净的工作区：

```bash
git switch main
git pull --ff-only
git switch -c docs/your-topic
# 编辑或新增资料，然后仅添加本次相关文件
git add docs/notes/your-topic.md
git diff --cached
git commit -m "docs: add notes on your topic"
git push -u origin docs/your-topic
```

随后在 GitHub 创建 PR。分支名和文件路径需要替换为实际内容；不要提交他人尚未完成的修改。

## 内容质量

- 区分“原论文结论”“自己的复现结果”“个人理解”和“待验证假设”，使用对应的四类陈述组件。
- 关键结论附来源链接，尽可能定位章节、图表或实验设置。
- 不把语言流畅、答案正确或思维链很长直接当作逻辑推理可靠的证据。
- 教程写明版本和运行状态；未验证的步骤明确标注“未验证”。
- 组会记录忠实保存不同意见，不把暂定讨论写成已证实结论。
- 引用已有内容使用相对链接。
- 模板提示按需删除；不适用项写“不适用”，关键缺失项写“待补充”，不要用猜测补齐。

## 附件与代码

图片放在 `docs/assets/<topic>/`，使用相对路径引用。优先链接论文原文和外部大文件；附件命名应能识别用途。

示例目录应有 README，记录运行方式、依赖、数据来源和预期输出，并提供至少一个 `check_*.py` 自检脚本；CI 会自动发现并运行它们。第三方依赖写在示例目录的 `requirements.txt` 中。大型数据、模型权重、训练日志和视频使用外部存储。`.gitignore` 只是基础防误提交规则，提交前仍需检查文件清单。

环境变量的示例值放在 `.env.example`；真实凭据不写入仓库。公开材料还需遵守[维护指南中的发布边界](PROJECT_PLAN.md#publishing-boundary)。

## 审阅与合并

每次 PR 尽量围绕一个主题。推荐一位其他成员审阅，重点检查位置、来源、可读性和结论依据。错别字与链接修复可快速处理，不为轻量笔记设置复杂审批。

组会记录通常由轮值记录人提交，汇报人检查技术内容，维护者合并。发现不确定结论时允许保留明确标注的开放问题。

页面底部的评论区适合提问、补充线索和讨论分歧；需要修改正文时，请直接提交 PR。

## 许可与公开范围

原创文档及内容模板采用 [CC BY 4.0](LICENSE-DOCS)，代码采用 [MIT](LICENSE)。东南大学校徽不适用上述许可，详见[许可与署名](docs/community/license.md)。提交贡献意味着你有权提供内容，并同意按对应许可发布；版权仍归原作者所有。

请保留作者和第三方来源说明。公开知识库只收录可公开材料，内部组会讨论、未发表实验和私人信息放在独立私有空间。

## 网站与本地检查

网站会从原文件生成贡献指南、模板和示例说明页面，无需维护两份。

```bash
uv run --python 3.12 --with-requirements requirements.txt python scripts/check_content.py
uv run --python 3.12 --with-requirements requirements.txt mkdocs build --strict
python scripts/check_site.py
python scripts/run_examples.py
```

`run_examples.py` 会运行所有示例的自检脚本；运行前需安装各示例目录中的 `requirements.txt`。内容位置、发布方式和维护约定见[维护指南](PROJECT_PLAN.md)。协作须遵守[行为准则](CODE_OF_CONDUCT.md)。
