# model evaluation introduction

模型评测是百炼平台提供的核心模型能力评估功能，用于量化文本生成类模型在特定任务上的表现。它支持自定义评测（基于用户数据与自定义维度）和基线评测（基于公开标准数据集）两种范式，覆盖从快速选型、调优验证到持续监控的全生命周期评估需求。评测结果以综合得分、通过率、分数分布及明细报告形式输出，为技术决策提供可复现的数据依据。

## 支持的模型/功能

- **模型类型**：当前仅支持**文本生成类模型**（包括预置模型与调优后的 SFT/DPO 模型），不支持视觉理解、图生视频等多模态模型 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。
- **评测方式**：
  - **自定义评测**：完全由用户控制，支持关联自定义评测集（EvaluationSet）、任意组合的评测维度（5 类），并可选择推理结果集复用已有 Output 以节省成本。
  - **基线评测**：内置 5 大类、13 个公开 Benchmark（如 MMLU-Pro、GSM8K、HumanEval、LongBench-v2、FinanceQA），自动执行、无需准备数据或配置维度，但**仅在北京地域可用** [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。
- **评分范式**：支持三大类共五种评测维度，可复用为模板：
  - *大模型评估*（数值型/分类型）：依赖裁判模型（如千问-Max）进行语义级评判；
  - *规则评估*（字符串匹配/文本相似度）：使用 ROUGE/BLEU/Cosine/Accuracy 等算法全自动计算；
  - *人工评估-分类型*：由人工逐条标注 Pass/Fail 标签 [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)。

> **注意**：文档 1 称“基线评测仅北京地域可用”，而文档 2 未提地域限制；实际以文档 1 的明确声明为准，其他地域控制台不显示基线评测选项属正常现象。

## 关键参数

- **评测维度参数**：
  - `裁判模型`：仅大模型评估类型必填，影响评分质量与费用；
  - `评分器 Prompt`：必须包含至少一个变量 `${prompt}`、`${output}` 或 `${completion}`，定义裁判逻辑；
  - `评分范围`（数值型）：整数区间，推荐 0–5；
  - `通过阈值`：数值型（步长 0.1）、相似度型（0–1）、分类型（标签对）均需设置；
  - `匹配规则`（字符串匹配）：相等 / 不相等 / 包含；
  - `相似度算法`（文本相似度）：7 种可选（ROUGE-L、BLEU、Cosine 等），需按场景匹配（如摘要用 ROUGE-L，翻译用 BLEU）。
- **评测任务参数**：
  - `数据来源`：二选一——**评测数据集**（触发被测模型推理，产生推理费用）或**推理结果集**（仅评分，零推理成本）；
  - `System Prompt`：作用于被测模型，非必填，多数场景可留空；
  - `Temperature/TopP`：推理参数，随所选模型动态加载；
  - `是否参与排行`：开启后需绑定已创建的排行榜，且排行榜维度必须与任务一致。

## 使用方式

1. **前置准备**：
   - 在[数据管理](https://bailian.console.aliyun.com/cn-beijing/model/data)中创建并**发布评测集（EvaluationSet 类型）**，格式需含 `Prompt` 与 `Completion` 两列 [训练集与评测集](../../raw/model-user-guide/model-evaluation-introduction/training-set-and-evaluation-set.md)。
2. **创建评测维度**：
   - 进入「模型评测 → 评测维度」，选择类型（如「大模型评估-数值型」），配置裁判模型、评分器模板（或自定义 Prompt）、评分范围与通过阈值。
3. **创建评测任务**：
   - 进入「模型评测 → 评测任务」，选择「自定义评测」或「基线评测」；
   - 自定义评测：选择目标模型、已发布的评测数据集、关联前述维度；
   - 基线评测：选择模型（官方或我的模型）、勾选 Benchmark（支持子维度筛选）、可选开启数据采样。
4. **执行与查看**：
   - 提交后状态流转为「待执行 → 进行中 → 评测完成」；
   - 完成后进入详情页：「指标统计」查看综合得分与通过率，「数据明细」查看每条样本评分；
   - 基线评测额外提供「Case 分析」与「多任务对比」页签。

## 限制和注意事项

- **地域限制**：基线评测功能仅在北京地域（华北2）可用，其他地域控制台不展示该选项 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。
- **数据集约束**：评测集必须为「EvaluationSet」类型且已**发布版本**；OSS 导入方式**不支持评测集**，仅限训练集 [训练集与评测集](../../raw/model-user-guide/model-evaluation-introduction/training-set-and-evaluation-set.md)。
- **维度不可变性**：评测维度的「类型」创建后不可修改，选错需删除重建；若已被排行榜绑定，须先解除绑定才能删除 [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)。
- **费用说明**：
  - 使用「评测数据集」时，产生**被测模型推理费用**（按输入/输出 [Token](../concepts/token.md) 计费）；
  - 仅「大模型评估」维度产生**裁判模型评分费用**（按 [Token](../concepts/token.md) 计费）；规则评估与人工评估无此项费用；
  - 「推理结果集」方式不产生被测模型推理费用。
- **结果解读建议**：综合得分是各维度平均值，可能掩盖维度间差异；应结合「分数分布图」与「维度明细」定位短板；1–3% 的分差通常属评测噪声，不宜作为决策唯一依据。

## 来源文档

- [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)
- [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)
- [训练集与评测集](../../raw/model-user-guide/model-evaluation-introduction/training-set-and-evaluation-set.md)


