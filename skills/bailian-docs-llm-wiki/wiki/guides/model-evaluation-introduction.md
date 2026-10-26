# model evaluation introduction

模型评测是百炼平台提供的核心模型能力评估功能，支持通过标准化流程对文本生成类模型进行量化打分与横向对比。它提供自定义评测（基于用户数据与自定义维度）和基线评测（基于公开标准数据集）两种范式，覆盖从快速选型到调优验证、持续监控的全生命周期评估需求。该功能面向开发者设计，强调可复用性、可解释性与成本可控性。

## 支持的模型/功能

- **支持模型类型**：仅支持文本生成类（text-generation）模型，包括预置模型（如千问系列）及用户调优后的模型；不支持多模态、语音、向量等非文本生成模型 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。
- **评测方式**：
  - **自定义评测**：完全由用户控制——上传评测数据集（EvaluationSet 类型）、创建评测维度、配置评分逻辑，支持大模型评估、规则评估、人工评估三类共五种评分器 [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)。
  - **基线评测**：内置 5 大类、13 个公开 Benchmark（如 MMLU-Pro、GSM8K、HumanEval），自动加载数据与评分标准，**仅在北京地域（华北2）可用**；不支持自定义维度或推理结果集输入 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。
- **核心功能模块**：评测维度（可复用评分模板）、评测任务（执行单元）、排行榜（跨任务横向对比）、人工标注（针对人工评估维度）。

> **注意**：文档 1 中称“基线评测仅北京地域可用”，文档 2 未提及地域限制，但文档 1 的“重要”提示与控制台行为一致，应以文档 1 为准。其他地域用户创建评测任务时将不显示基线评测选项，属正常现象。

## 关键参数

| 参数类别 | 参数名 | 说明 | 约束与建议 |
|----------|--------|------|------------|
| **评测维度** | 维度类型 | 必填，5 种之一：`大模型评估-数值型`/`-分类型`/`规则评估-字符串匹配`/`-文本相似度`/`人工评估-分类型`；**创建后不可修改** | 选错需删除重建；详见[评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md) |
| | 裁判模型 | 仅大模型评估类型必填；推荐 `qwen-max`（推理能力强） | 影响评分质量与费用 |
| | 评分器 Prompt | 仅大模型评估类型必填；须含至少一个变量 `${prompt}` / `${output}` / `${completion}` | 变量引用错误将导致提交失败 |
| | 评分范围 & 通过阈值 | 数值型：整数区间（默认 `0-5`），阈值步长 `0.1`；相似度型：`0.00–1.00`，步长 `0.01` | 阈值设定需匹配业务容忍度；范围过宽（如 `0-10`）易降低 LLM 评分一致性 |
| **评测任务** | 数据来源 | `评测数据集`（触发被测模型推理，产生费用）或 `推理结果集`（仅评分，无推理费） | 小规模验证建议先用 `推理结果集` 复用已有输出 |
| | System Prompt | 配置于任务级，作用于被测模型；多数场景可留空 | 与维度级的 `评分器 Prompt` 作用对象不同，勿混淆 |

## 使用方式

1. **准备数据**：在数据管理模块上传 `EvaluationSet` 类型数据集（含 `Prompt` 和 `Completion` 列），或准备已含 `Output` 的推理结果集文件。
2. **创建维度**：在「评测维度」页签创建至少一个维度模板。例如，快速启动可选「大模型评估-数值型」+「综合评测」模板 + 评分范围 `0-5` + 通过阈值 `3.0` [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。
3. **创建任务**：
   - 自定义评测：选择模型、数据来源（数据集/结果集）、关联维度；可选开启排行榜参与。
   - 基线评测：仅北京地域可见，选择模型与 Benchmark（支持多选及子维度勾选）。
4. **查看结果**：
   - 自定义评测：在任务详情页查看「指标统计」（综合得分、通过率、分布图）和「数据明细」（逐条评分）。
   - 基线评测：提供「任务总览」「基线评分明细」「Case 分析」「多任务对比」四页签，支持雷达图与 Bad Case 下钻。

## 限制和注意事项

- **地域限制**：基线评测功能**仅在北京地域（华北2）可用**；其他地域控制台不显示该选项，无法创建 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。
- **模型限制**：当前**仅支持文本生成类模型**；不支持图像生成、语音合成、嵌入模型等非 text-generation 模态。
- **维度不可变性**：评测维度的类型、裁判模型（若适用）创建后不可修改，误配需删除重建；已关联该维度的评测任务不受影响，但新任务需重新关联 [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)。
- **费用关键点**：
  - 使用 `评测数据集` 作为数据来源 → 产生**被测模型推理费用**；
  - 使用 `大模型评估` 类型维度 → 产生**裁判模型评分费用**；
  - `规则评估` 与 `人工评估` 维度 → 无裁判模型费用；
  - `推理结果集` 数据源 → 无被测模型推理费用。
- **结果解读建议**：避免仅依赖综合得分；应结合分数分布图与维度明细分析短板（例如某维度得分显著偏低）；1–3% 的分差通常属评测噪声，不宜作为决策依据 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。

## 来源文档

- [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)
- [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)


