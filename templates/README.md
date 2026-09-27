# 内容模板

| 内容 | 模板 | 保存位置 |
| --- | --- | --- |
| 学习笔记 | [note.md](note.md) | `docs/notes/<主题目录>/<英文短名>.md` |
| 论文阅读 | [paper.md](paper.md) | `docs/papers/<论文年份>/<英文短名>.md` |
| 实践教程 | [tutorial.md](tutorial.md) | `docs/tutorials/<英文短名>.md` |
| 组会记录 | [meeting.md](meeting.md) | `docs/meetings/<年份>/<YYYY-MM-DD>.md` |

复制模板到目标位置后，先填写开头的 frontmatter（两条 `---` 之间的元信息），再按需删除提示文字和不适用章节。模板中的占位字段是待填写内容，不是真实记录。

**只需新增这一个文件。** 网站会根据 frontmatter 和所在目录自动完成导航、栏目索引、学习路线、首页统计、元信息卡片与标签页，不需要再修改 `mkdocs.yml` 或索引页。字段说明见[贡献指南](../CONTRIBUTING.md#frontmatter)。

## 写作组件

- **四类陈述**：`!!! claim "原文结论"`、`!!! reproduced "复现观察"`、`!!! insight "个人理解"`、`!!! hypothesis "待验证假设"`，分别以不同颜色呈现。
- **推导块**：使用 `derivation` 代码块书写前提、规则与结论；规则前加 `!` 表示无效推理。
- **公式**：行内 `$\Gamma \models \varphi$`，独立公式使用 `$$ ... $$`，由本地打包的 KaTeX 渲染。
- **流程图**：使用 `mermaid` 代码块。

效果示例见[阅读与验证方法](../docs/getting-started/reading-guide.md)。图片与其他笔记链接应根据新文件的位置编写相对路径。
