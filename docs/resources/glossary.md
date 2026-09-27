# 术语表

常用术语的中英对照与简要说明，写笔记时请尽量沿用这里的译名。定义以经典逻辑的标准用法为准；有争议或多种译法的术语在说明中注出。正文中出现的英文缩写（如 LLM、CoT、SAT、SMT、FOL）会自动显示悬停提示。

## 逻辑基础

| 中文 | English | 说明 |
| --- | --- | --- |
| 命题 | proposition | 有确定真假的陈述。 |
| 赋值 | valuation / assignment | 给每个命题变元指定真或假。 |
| 实质蕴涵 | material implication | 连接词 $P \to Q$，仅在 $P$ 真、$Q$ 假时为假。 |
| 逻辑后承 | logical consequence / entailment | $\Gamma \models \varphi$：所有使前提全真的赋值都使结论为真。 |
| 有效 | valid | 论证：不存在前提全真而结论为假的情形。公式：在所有赋值下为真。 |
| 健全 | sound | 论证有效且前提实际为真；用于证明系统时指“可证的都有效”。 |
| 可满足 | satisfiable | 至少有一个赋值使公式为真。 |
| 重言式 | tautology | 在所有赋值下为真的命题公式。 |
| 矛盾式 | contradiction | 在所有赋值下为假的公式。 |
| 反例 | counterexample | 使前提全真、结论为假的赋值或模型。 |
| 肯定前件 | modus ponens | 由 $P \to Q$ 与 $P$ 推出 $Q$，有效。 |
| 否定后件 | modus tollens | 由 $P \to Q$ 与 $\lnot Q$ 推出 $\lnot P$，有效。 |
| 肯定后件 | affirming the consequent | 由 $P \to Q$ 与 $Q$ 推出 $P$，无效。 |
| 否定前件 | denying the antecedent | 由 $P \to Q$ 与 $\lnot P$ 推出 $\lnot Q$，无效。 |
| 一阶逻辑 | first-order logic (FOL) | 含个体变元、谓词与量词 $\forall$、$\exists$ 的逻辑。 |
| 演绎 / 归纳 / 溯因 | deduction / induction / abduction | 见[演绎、归纳与溯因](../notes/logic-foundations/deduction-induction-abduction.md)。 |
| 单调性 | monotonicity | 增加前提不会使已成立的后承失效；经典逻辑具有此性质。 |

## 求解与验证

| 中文 | English | 说明 |
| --- | --- | --- |
| 可满足性问题 | Boolean satisfiability (SAT) | 判断命题公式是否可满足；NP 完全。 |
| 理论模可满足性 | satisfiability modulo theories (SMT) | 在算术、数组等背景理论下判断可满足性，例如 Z3。 |
| 交互式定理证明 | interactive theorem proving | 人与证明助手协作构造可机器检查的证明，例如 Lean。 |
| 可判定 | decidable | 存在总能在有限步内给出正确答案的算法。 |

## 大模型推理

| 中文 | English | 说明 |
| --- | --- | --- |
| 大语言模型 | large language model (LLM) | 以自回归方式生成文本的大规模神经网络模型。 |
| 思维链 | chain-of-thought (CoT) | 让模型在答案前生成中间推理步骤；步骤可读不等于步骤有效。 |
| 自洽性 | self-consistency | 多次采样推理路径并对答案投票。 |
| 上下文学习 | in-context learning | 仅通过提示中的示例完成任务，不更新参数。 |
| 监督微调 | supervised fine-tuning (SFT) | 用标注的输入输出对继续训练模型。 |
| 结果奖励 / 过程奖励 | outcome / process reward (ORM / PRM) | 分别只评价最终结果，或逐步评价中间步骤。 |
| 验证器 | verifier | 判断答案或推理步骤是否正确的模型或程序。 |
| 神经符号方法 | neuro-symbolic methods | 把神经网络与符号表示、求解器或规则系统结合。 |
| 数据泄漏 | data contamination / leakage | 评测数据出现在训练数据中，导致高估能力。 |
| 忠实性 | faithfulness | 模型给出的解释是否真实反映其得出答案的依据。 |

发现译名或定义有误？请直接编辑本页，或在页面底部留言。
