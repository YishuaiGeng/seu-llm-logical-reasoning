---
title: 可满足性、有效性与等价
type: note
authors: [SEU LLM Logical Reasoning contributors]
status: stable
created: 2026-09-27
stage: logic
order: 2
tags: [逻辑基础, 可满足性, 有效性, 求解器]
summary: 理解可满足、有效、不可满足三种性质，以及“检查有效性”如何转化为“检查不可满足”
prerequisites: 蕴涵、有效性与反例
---

# 可满足性、有效性与等价

前置知识：[蕴涵、有效性与反例](implication-and-entailment.md)。本文仍在经典命题逻辑中讨论。

## 本文要回答的问题

求解器通常只回答一个问题：“这组公式能否同时为真？”我们关心的却是“这个推理是否有效”。两者之间有一个简单而重要的转换，理解它之后，就能看懂 SAT、SMT 求解器怎样被用来检查推理。

## 三种性质

对一个命题公式 $\varphi$：

可满足（satisfiable）
:   至少存在一个赋值使 $\varphi$ 为真。例如 $P \land \lnot Q$。

有效（valid），也称重言式
:   所有赋值都使 $\varphi$ 为真。例如 $P \lor \lnot P$。

不可满足（unsatisfiable），也称矛盾式
:   没有任何赋值使 $\varphi$ 为真。例如 $P \land \lnot P$。

有效的公式一定可满足；可满足的公式不一定有效。一个公式要么可满足，要么不可满足，二者必居其一。

## 核心转换：有效 ⇔ 否定不可满足

$\varphi$ 有效，当且仅当 $\lnot\varphi$ 不可满足。

理由很直接：“所有赋值都让 $\varphi$ 为真”等价于“不存在让 $\varphi$ 为假的赋值”，也就是“不存在让 $\lnot\varphi$ 为真的赋值”。

推广到带前提的推理：

$$
\Gamma \models \varphi \quad\Longleftrightarrow\quad \Gamma \cup \{\lnot\varphi\}\ \text{不可满足}
$$

也就是说，**把结论取反后加入前提，如果这组公式无法同时为真，推理就有效**；如果可以同时为真，那个满足赋值就是一个反例：前提全真而结论为假。

```derivation
Γ ∪ {¬φ} 不可满足
--- 反证
Γ ⊨ φ
```

这正是[真值表教程](../../tutorials/truth-table.md)中“寻找前提全真、结论为假的赋值”的另一种表述，也是[Z3 教程](../../tutorials/z3-validity.md)使用的检查方法。

## 逻辑等价

$\varphi$ 与 $\psi$ 逻辑等价，记作 $\varphi \equiv \psi$，当且仅当它们在所有赋值下取值相同，即 $\varphi \leftrightarrow \psi$ 有效。常见例子：

| 名称 | 等价式 |
| --- | --- |
| 蕴涵的析取形式 | $P \to Q \equiv \lnot P \lor Q$ |
| 逆否 | $P \to Q \equiv \lnot Q \to \lnot P$ |
| 德摩根律 | $\lnot(P \land Q) \equiv \lnot P \lor \lnot Q$ |

“逆否等价”说明了为什么否定后件（由 $P \to Q$ 和 $\lnot Q$ 推出 $\lnot P$）有效；而 $P \to Q$ 与它的逆命题 $Q \to P$ 并不等价，这正是肯定后件无效的原因。

## 计算上的代价

判断任意命题公式是否可满足（SAT 问题）是第一个被证明为 NP 完全的问题（Cook–Levin 定理）。目前没有已知算法能在最坏情况下高效求解所有实例，但现代 SAT 求解器在大量实际问题上表现良好。

到了一阶逻辑，有效性问题是不可判定的：不存在对所有公式都能在有限步内给出“有效/无效”答案的算法。它是半可判定的：公式确实有效时，存在能够最终找到证明的过程。因此求解器处理带量词的公式时，除了“可满足”“不可满足”，还可能返回“未知”。

## 对大模型评测的启发

1. 把自然语言推理形式化后，可以用“结论取反后是否不可满足”机械地检查有效性，并得到具体反例。
2. 检查结果只对形式化后的公式成立。从自然语言到公式的翻译本身可能出错，这一步需要单独评估。
3. 前提集合本身不可满足时，它在经典语义下蕴涵任何结论。评测时应先检查前提是否可满足，避免把“前提矛盾”误当作“推理正确”。

!!! hypothesis "待验证假设"
    用求解器验证模型给出的形式化推理，能区分“最终答案碰巧正确”和“推理步骤有效”两种情况；但它能否发现翻译错误，取决于是否另有对照。组内可以设计小规模实验检验。

## 参考资料

- [forall x: Calgary](https://forallx.openlogicproject.org/)：真值表、重言式、等价与有效性的入门讲解。
- [Open Logic Project](https://openlogicproject.org/)：可满足性、紧致性与可判定性等进阶内容。
- [Z3 Guide](https://microsoft.github.io/z3guide/)：Z3 官方交互式教程。
