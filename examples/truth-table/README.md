# Truth-table entailment example

一个仅使用 Python 标准库的教学示例，演示经典命题逻辑中的语义后承、反例与前提可满足性。

配套教程：[用真值表检查一个推理](../../docs/tutorials/truth-table.md)。

## 运行

需要 Python 3.10+，在仓库根目录执行：

```bash
python examples/truth-table/check_entailment.py
```

脚本输出肯定前件的验证结果、肯定后件的反例，并执行基本自检。没有外部数据、模型、API 或硬件需求。

本程序只检查显式给出的命题布尔函数，不解析或验证任意自然语言推理。代码采用 MIT，本文档采用 CC BY 4.0。
