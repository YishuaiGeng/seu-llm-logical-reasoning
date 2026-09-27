# 论文阅读

围绕**问题、方法、证据、局限**记录阅读过程，保留可以回到原文核实的线索。

## 阅读索引

<!-- lr:index papers -->

## 候选论文 · 待认领 {#candidates}

以下论文与本项目的核心问题直接相关，**尚无组内精读笔记**，欢迎认领。题名、作者与年份已对照 arXiv 记录核实；发表信息取自 arXiv 页面的作者备注，写笔记时请再次核对正式版本。

| 方向 | 论文 | arXiv | 备注 |
| --- | --- | --- | --- |
| 基准 · 规则推理 | Transformers as Soft Reasoners over Language（Clark, Tafjord, Richardson） | [2002.05867](https://arxiv.org/abs/2002.05867) | 作者备注 IJCAI 2020；RuleTaker 数据 |
| 基准 · 证明生成 | ProofWriter: Generating Implications, Proofs, and Abductive Statements over Natural Language（Tafjord et al.） | [2012.13048](https://arxiv.org/abs/2012.13048) | 作者备注 Findings of ACL 2021 |
| 基准 · 一阶逻辑 | FOLIO: Natural Language Reasoning with First-Order Logic（Han et al.） | [2209.00840](https://arxiv.org/abs/2209.00840) | 带一阶逻辑标注的自然语言推理数据 |
| 基准 · 阅读理解 | LogiQA: A Challenge Dataset for Machine Reading Comprehension with Logical Reasoning（Liu et al.） | [2007.08124](https://arxiv.org/abs/2007.08124) | 作者备注 IJCAI 2020 |
| 基准 · 阅读理解 | ReClor: A Reading Comprehension Dataset Requiring Logical Reasoning（Yu et al.） | [2002.04326](https://arxiv.org/abs/2002.04326) | 作者备注 ICLR 2020 |
| 分析 · 思维链 | Language Models Are Greedy Reasoners: A Systematic Formal Analysis of Chain-of-Thought（Saparov, He） | [2210.01240](https://arxiv.org/abs/2210.01240) | 作者备注 ICLR 2023；PrOntoQA |
| 方法 · 提示 | Chain-of-Thought Prompting Elicits Reasoning in Large Language Models（Wei et al.） | [2201.11903](https://arxiv.org/abs/2201.11903) | 思维链提示 |
| 方法 · 采样 | Self-Consistency Improves Chain of Thought Reasoning in Language Models（Wang et al.） | [2203.11171](https://arxiv.org/abs/2203.11171) | 作者备注 ICLR 2023 |
| 方法 · 神经符号 | Logic-LM: Empowering Large Language Models with Symbolic Solvers for Faithful Logical Reasoning（Pan et al.） | [2305.12295](https://arxiv.org/abs/2305.12295) | 作者备注 Findings of EMNLP 2023 |
| 方法 · 神经符号 | LINC: A Neurosymbolic Approach for Logical Reasoning by Combining Language Models with First-Order Logic Provers（Olausson et al.） | [2310.15164](https://arxiv.org/abs/2310.15164) | 作者备注 EMNLP 2023 |
| 训练 · 过程监督 | Let's Verify Step by Step（Lightman et al.） | [2305.20050](https://arxiv.org/abs/2305.20050) | 结果监督与过程监督的比较 |

认领方式：在 [Issues](https://github.com/YishuaiGeng/seu-llm-logical-reasoning/issues/new?template=content.yml) 中说明要读的论文，或在组会上登记。完成的笔记会自动出现在上方索引，本表中对应条目随之删除。新的推荐先放到 [Discussions](https://github.com/YishuaiGeng/seu-llm-logical-reasoning/discussions)。

## 一份笔记应包含什么

- 核实后的题名、作者、版本与原文链接（写在 frontmatter 的 `paper` 字段中，页面顶部会自动生成论文信息卡）。
- 论文如何定义逻辑推理任务，采用哪些输入与评测指标。
- 方法机制、关键实验与证据的适用范围。
- 作者承认的局限、阅读者的疑问和复现状态；用“原文结论 / 复现观察 / 个人理解 / 待验证假设”四类标注区分陈述。

先看[阅读与验证方法](../getting-started/reading-guide.md)，再复制[论文模板](../../templates/paper.md)。按论文发表或预印本年份建立目录；多次讨论链接同一份主笔记。
