# Z3 有效性检查示例

用 [Z3](https://github.com/Z3Prover/z3) 检查推理是否有效：把结论取反后与前提一起交给求解器，结果不可满足则推理有效，可满足则得到反例。覆盖命题逻辑与一个带全称量词的一阶逻辑例子。

配套教程：[用 Z3 检查有效性与反例](../../docs/tutorials/z3-validity.md)。

## 运行

需要 Python 3.10+，在仓库根目录执行：

```bash
python -m pip install -r examples/z3-validity/requirements.txt
python examples/z3-validity/check_validity.py
```

脚本会打印每个推理的判定结果并执行自检；任何断言失败都会以非零状态退出。依赖只有 `z3-solver`（版本见 `requirements.txt`），没有外部数据、模型、API 或硬件需求。仓库 CI 会实际运行该脚本。

本程序只检查显式写出的公式，不解析自然语言。代码采用 MIT，本文档采用 CC BY 4.0。
