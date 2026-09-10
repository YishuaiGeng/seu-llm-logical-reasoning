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

以上仅为命名示例，不表示已有对应笔记或会议。论文目录年份按论文发表或预印本年份组织；文中单独记录阅读日期。组会按实际发生日期组织。同日多场会议可加主题后缀。

文件名使用简短英文小写和连字符，正文以中文为主，保留必要英文术语。署名写在正文元信息里。更新已有笔记时保留原作者并补充贡献者。

## GitHub 网页提交

1. 进入仓库，切换到一个新分支。
2. 复制模板，新建相应路径的文件；上传附件时放到对应主题的 `docs/assets/` 子目录。
3. 编辑内容，并使用 Preview 查看渲染效果。
4. 提交到自己的分支，创建面向 `main` 的 PR。
5. 根据审阅意见修改，由维护者合并。

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

- 区分“原论文结论”“自己的复现结果”“个人理解”和“待验证假设”。
- 关键结论附来源链接，尽可能定位章节、图表或实验设置。
- 不把语言流畅、答案正确或思维链很长直接当作逻辑推理可靠的证据。
- 教程写明版本和运行状态；未验证的步骤明确标注“未验证”。
- 组会记录忠实保存不同意见，不把暂定讨论写成已证实结论。
- 引用已有内容使用相对链接，新增文档时更新所属目录索引。
- 模板提示按需删除；不适用项写“不适用”，关键缺失项写“待补充”，不要用猜测补齐。

## 附件与代码

图片放在 `docs/assets/<topic>/`，使用相对路径引用。优先链接论文原文和外部大文件；附件命名应能识别用途。

示例目录应有 README，记录运行方式、依赖、数据来源和预期输出。大型数据、模型权重、训练日志和视频使用外部存储。`.gitignore` 只是基础防误提交规则，提交前仍需检查文件清单。

环境变量的示例值放在 `.env.example`；真实凭据不写入仓库。公开材料还需遵守[维护指南中的发布边界](PROJECT_PLAN.md#publishing-boundary)。

## 审阅与合并

每次 PR 尽量围绕一个主题。推荐一位其他成员审阅，重点检查位置、来源、可读性和结论依据。错别字与链接修复可快速处理，不为轻量笔记设置复杂审批。

组会记录通常由轮值记录人提交，汇报人检查技术内容，维护者合并。发现不确定结论时允许保留明确标注的开放问题。

## 许可与公开范围

原创文档及内容模板采用 [CC BY 4.0](LICENSE-DOCS)，代码采用 [MIT](LICENSE)。提交贡献意味着你有权提供内容，并同意按对应许可发布；版权仍归原作者所有。

请保留作者和第三方来源说明。公开知识库只收录可公开材料，内部组会讨论、未发表实验和私人信息放在独立私有空间。

## 网站与本地检查

网站会从原文件生成贡献指南和模板页面，无需维护两份。新增公开文档时，更新目录索引以及 `mkdocs.yml` 导航。

```bash
uv run --python 3.12 --with-requirements requirements.txt mkdocs build --strict
python scripts/check_site.py
python examples/truth-table/check_entailment.py
```

内容位置、发布方式和维护约定见 [维护指南](PROJECT_PLAN.md)。协作须遵守 [行为准则](CODE_OF_CONDUCT.md)。
