# model evaluation introduction

模型评测是百炼平台提供的核心模型能力评估功能，支持通过标准化流程对文本生成类模型进行量化打分与横向对比。它提供自定义评测（基于用户数据与自定义维度）和基线评测（基于公开标准数据集）两种范式，覆盖从快速选型、调优验证到持续质量监控的全场景需求。该功能面向开发者设计，强调可复用性、可解释性与成本可控性。

## 支持的模型与功能

- **支持模型类型**：仅支持文本生成类（text-generation）模型，包括预置模型（如千问系列）及用户调优后的模型；不支持多模态、语音、向量等其他模态模型 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。
- **评测方式**：
  - **自定义评测**：完全由用户控制——上传评测数据集（EvaluationSet 类型）、创建评测维度、配置评分逻辑，支持大模型评估、规则评估、人工评估三类共五种评分器 [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)。
  - **基线评测**：内置 5 大类、13 个公开 Benchmark（如 MMLU-Pro、GSM8K、HumanEval、LongBench-v2、FinanceQA），自动加载数据与评分标准，无需准备数据或配置维度；**仅在北京地域（华北2）可用** [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。
- **核心功能模块**：评测维度（模板化评分规则）、评测任务（执行单元）、排行榜（跨任务横向对比）、人工标注（支持人工评估维度）、结果分析（指标统计 + 数据明细 + Case 下钻）。

> **注意**：文档1中称“基线评测仅北京地域可用”，文档2未提地域限制，但文档2为维度专项文档，不涉及地域逻辑。以文档1为准，该限制为平台真实约束，非过时信息。

## 关键参数

| 参数类别 | 参数名 | 说明 | 约束与建议 |
|----------|--------|------|------------|
| **评测维度** | 维度类型 | 必填，5 种之一：`大模型评估-数值型`/`-分类型`、`规则评估-字符串匹配`/`-文本相似度`、`人工评估-分类型`；**创建后不可修改** | 选错需删除重建；人工评估不产生裁判模型费用 [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md) |
| | 裁判模型 | 仅大模型评估类型必填；推荐 `qwen-max`（推理能力强） | 影响评分质量与费用；费用按 Token 计费 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md) |
| | 评分器 Prompt | 大模型评估类型必填；至少含 `${prompt}`、`${output}`、`${completion}` 中一个变量 | 变量引用错误或缺失将导致提交失败；预置模板（如“综合评测”）可快速启动 [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md) |
| | 评分范围 / 通过阈值 | 数值型：整数区间（默认 `0–5`）；通过阈值步长 `0.1`；相似度型：`0–1` 区间，步长 `0.01` | 阈值设定需匹配业务容忍度；范围过宽（如 `0–100`）会降低 LLM 评分一致性 [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md) |
| **评测任务** | 数据来源 | `评测数据集`（触发被测模型推理，产生推理费）或 `推理结果集`（仅评分，无推理费） | 小规模验证建议先用 `评测数据集`，后续复用 `推理结果集` 降本 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md) |
| | System Prompt | 作用于被测模型，定义其角色/行为规范；**非评分器 Prompt** | 多数场景可留空；与评分器 Prompt 作用对象、费用归属均不同 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md) |

## 使用方式

1. **准备数据**：在数据管理模块上传 `EvaluationSet` 类型数据集（含 `Prompt` 和 `Completion` 列），或准备已含 `Output` 的推理结果集文件。
2. **创建维度**：进入「评测维度」页签 → 「创建评测维度」→ 选择类型 → 配置参数（如裁判模型、Prompt、标签、阈值等）→ 保存。*建议先用预置模板（如“综合评测”）小样本验证（10–20 条），再迭代优化 Prompt* [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)。
3. **创建任务**：
   - 自定义评测：选择「自定义评测」→ 指定被测模型 → 选择数据来源（数据集 or 结果集）→ 关联已建维度 → （可选）开启排行榜 → 「开始评测」。
   - 基线评测：选择「基线评测」→ 选择被测模型 → 勾选 Benchmark（支持多选及子维度筛选）→ （可选）开启数据采样 → 「开始评测」。
4. **查看结果**：
   - 自定义任务：详情页含「指标统计」（综合得分、通过率、分布图）和「数据明细」（逐条 Prompt/Output/Completion/各维度评分）。
   - 基线任务：含「任务总览」（雷达图）、「基线评分明细」、「Case 分析」（含裁判依据）、「多任务对比」。
   - 所有结果支持下载 CSV/Excel。

## 限制和注意事项

- **地域限制**：基线评测功能**仅在北京地域（华北2）可用**；其他地域控制台不显示该选项，属正常现象 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。
- **模型限制**：当前**仅支持文本生成类模型**；不支持图像生成、语音合成、嵌入等其他模态模型 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。
- **维度不可变**：评测维度的「类型」创建后不可修改，选错需删除重建；删除维度前须确保无排行榜绑定，否则将阻止新任务创建 [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)。
- **费用说明**：
  - 费用 = 被测模型推理费 + 裁判模型评分费（仅大模型评估维度产生）。
  - 规则评估（字符串匹配/文本相似度）和人工评估**无裁判模型费用**。
  - 使用「推理结果集」作为数据源时，**不产生被测模型推理费用** [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。
- **结果解读**：综合得分是各维度平均分，可能掩盖维度间差异；**务必结合分数分布图与各维度明细分析短板**；1–3% 的分差通常属评测噪声，不宜作为决策依据 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。

## 来源文档

- [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)
- [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)


