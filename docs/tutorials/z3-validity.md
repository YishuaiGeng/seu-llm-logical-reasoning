---
title: 用 Z3 检查有效性与反例
type: tutorial
authors: [SEU LLM Logical Reasoning contributors]
status: review
created: 2026-09-27
stage: logic
order: 2
tags: [逻辑基础, 求解器, Python, 一阶逻辑]
summary: 把“有效”转化为“否定结论后不可满足”，用 Z3 检查命题与一阶推理
difficulty: 入门
environment: Python 3.10+ · z3-solver
verified: verified
verified_on: 2026-09-27 · macOS · Python 3.12 · z3-solver 5.1.0；仓库 CI 每次提交运行
---

# 用 Z3 检查有效性与反例

配套代码：[examples/z3-validity](../../examples/z3-validity/README.md)

## 学习目标

[真值表教程](truth-table.md)通过枚举全部赋值来检查推理，变量一多就不可行。本教程把同样的问题交给 SMT 求解器 Z3，并把方法扩展到带量词的一阶逻辑。完成后你能：

- 用“前提 + 结论取反是否不可满足”判断推理是否有效；
- 从求解器返回的模型中读出反例；
- 理解求解器返回“未知”的情况，以及检查结果的适用边界。

背景知识见[可满足性、有效性与等价](../notes/logic-foundations/satisfiability-and-validity.md)。

## 前置条件

- Python 3.10+；
- 安装依赖：`python -m pip install -r examples/z3-validity/requirements.txt`；
- 不需要模型、GPU、数据集或外部 API。

## 操作步骤

### 1. 核心函数

```python
from z3 import Not, Solver, sat, unsat

def check(premises, conclusion):
    solver = Solver()
    solver.add(*premises)          # 前提全部为真
    solver.add(Not(conclusion))    # 结论为假
    result = solver.check()
    if result == unsat:
        return "VALID", None       # 找不到反例：推理有效
    if result == sat:
        return "INVALID", solver.model()   # 模型就是反例
    return "UNKNOWN", solver.reason_unknown()
```

它直接对应下面的等价关系：

$$
\Gamma \models \varphi \iff \Gamma \cup \{\lnot\varphi\}\ \text{不可满足}
$$

### 2. 命题逻辑

```python
from z3 import Bools, Implies

P, Q = Bools("P Q")
check([Implies(P, Q), P], Q)   # 肯定前件 → VALID
check([Implies(P, Q), Q], P)   # 肯定后件 → INVALID，模型给出 P=False, Q=True
```

### 3. 一阶逻辑

声明一个论域 `Thing`、两个谓词和一个常量，再用 `ForAll` 写出全称前提：

```python
from z3 import BoolSort, Const, DeclareSort, ForAll, Function, Implies

Thing = DeclareSort("Thing")
Human = Function("Human", Thing, BoolSort())
Mortal = Function("Mortal", Thing, BoolSort())
socrates, x = Const("socrates", Thing), Const("x", Thing)

all_humans_mortal = ForAll([x], Implies(Human(x), Mortal(x)))
check([all_humans_mortal, Human(socrates)], Mortal(socrates))   # VALID
check([all_humans_mortal, Mortal(socrates)], Human(socrates))   # INVALID
```

```derivation
∀x (Human(x) → Mortal(x))
Mortal(socrates)
--- !逆推
Human(socrates)
```

第二个推理无效：求解器会构造一个论域，其中 `socrates` 会死但不是人。

### 4. 运行完整示例

```bash
python examples/z3-validity/check_validity.py
```

## 预期结果与检查方法

以下为 2026-09-27 在 z3-solver 5.1.0 上的实测输出：

```text
Modus ponens: VALID
Affirming the consequent: INVALID
Counterexample: P=False, Q=True
Modus tollens: VALID
Contradictory premises: VALID but unsatisfiable (not a sound argument)
Syllogism (all humans are mortal; Socrates is human): VALID
Converse (Socrates is mortal, so human?): INVALID
Self-checks: passed
```

脚本用断言检查每个判定，因此“Self-checks: passed”意味着上述结论都已被程序确认。反例的具体取值可能因 Z3 版本而不同，但必须满足“前提全真、结论为假”。

## 常见问题

**返回 `UNKNOWN`。** 一阶逻辑的有效性不可判定，含量词的公式可能超出求解器的能力或资源限制。可以尝试简化公式、给出更具体的实例，或设置超时后如实报告“未知”，不要把它当作“有效”或“无效”。

**前提互相矛盾时也显示有效。** 这是经典逻辑的正确结果。示例中单独检查了前提是否可满足，实际使用时也应这样做。

## 局限与后续练习

- 检查只对写出的公式成立。从自然语言到公式的翻译是否忠实，需要另外评估，这往往才是评测模型推理时最难的一步。
- 练习：检查否定前件（由 $P \to Q$ 和 $\lnot P$ 推出 $\lnot Q$）并读出反例。
- 练习：给一阶例子加上“存在某个不会死的东西”这一前提，观察结论是否改变。
- 进阶：阅读 Logic-LM、LINC 等把语言模型与求解器结合的论文（见[候选论文](../papers/README.md#candidates)），思考翻译错误如何影响最终结果。

## 参考资料

- [Z3 Guide](https://microsoft.github.io/z3guide/)：官方交互式教程。
- [Z3 GitHub 仓库](https://github.com/Z3Prover/z3)：安装方式与 Python API。
- [可满足性、有效性与等价](../notes/logic-foundations/satisfiability-and-validity.md)：本教程的理论背景。
