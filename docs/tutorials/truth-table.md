---
title: 用真值表检查一个推理
type: tutorial
authors: [SEU LLM Logical Reasoning contributors]
status: stable
created: 2026-09-10
stage: logic
order: 1
tags: [逻辑基础, Python, 有效性]
summary: 枚举赋值，验证肯定前件并找到肯定后件的反例
difficulty: 入门
environment: Python 3.10+ · 仅标准库
verified: verified
verified_on: 仓库 CI（Ubuntu · Python 3.12）每次提交运行
---

# 用真值表检查一个推理

## 你会完成什么

用穷举赋值检查两个命题推理：验证肯定前件有效，并找到肯定后件的反例。这个练习展示“前提全真、结论为假”的检查方法，不涉及模型训练或调用。

先读：[蕴涵、有效性与反例](../notes/logic-foundations/implication-and-entailment.md)。

## 运行示例

在仓库根目录执行：

```bash
python examples/truth-table/check_entailment.py
```

[查看完整代码](../../examples/truth-table/check_entailment.py)。无需下载模型、数据集或安装第三方库。

## 预期输出

```text
Modus ponens: VALID (1 satisfying assignment)
Affirming the consequent: INVALID
Counterexample: P=False, Q=True
Self-checks: passed
```

脚本自检覆盖蕴涵的四种真值组合、有效与无效推理，以及前提不可满足的情况。仓库 CI 会实际运行该脚本。

## 理解检查过程

1. 枚举 `P`、`Q` 的四种赋值。
2. 只保留使所有前提为真的赋值。
3. 检查这些赋值是否也让结论为真。
4. 一旦发现结论为假，返回该赋值作为反例。

代码还返回满足前提的赋值数量。数量为零时，经典语义上的后承虽然成立，但应该额外提醒自己：前提不可满足。

## 可以继续尝试

- 验证否定后件：由 `P → Q` 与 `¬Q` 推出 `¬P`。
- 检查否定前件：由 `P → Q` 与 `¬P` 是否能推出 `¬Q`。
- 增加第三个命题变量，观察枚举规模如何变化。

## 局限

枚举对 `n` 个变量需要检查至多 `2^n` 个赋值，不适合直接扩展到很大的公式。本示例没有自然语言解析、量词、概率或因果语义；逻辑检查的可靠性依赖于正确的形式化。

更复杂的任务可以使用求解器：下一篇[用 Z3 检查有效性与反例](z3-validity.md)把同样的问题交给 Z3，并扩展到一阶逻辑。
