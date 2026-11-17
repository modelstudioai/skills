# model evaluation introduction

模型评测是百炼平台用于量化评估大模型能力的核心功能，支持通过自定义评测集与多类型评分维度对模型输出进行自动化或人工评判。它覆盖从模型选型、调优效果验证到持续质量监控的全生命周期场景，当前仅支持文本生成类模型。评测结果可生成结构化报告、排行榜及难例回流数据，为模型迭代提供可追溯的数据依据。

## 支持的模型/功能

- **支持模型类型**：仅限文本生成类模型（包括预置模型与调优后的 SFT/DPO 模型），视觉理解、图生视频等非文本生成模型暂不支持评测 [训练集与评测集](../../raw/model-user-guide/model-evaluation-introduction/training-set-and-evaluation-set.md)。
- **评测方式**：
  - **自定义评测**：使用用户上传的评测集（EvaluationSet 类型）和自定义/预置评测维度，支持大模型评估、规则评估、人工评估三类评分器 [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)。
  - **基线评测**：内置 5 大类共 13 个公开标准 Benchmark（如 MMLU-Pro、GSM8K、HumanEval），自动完成评测并生成基准分数，**仅北京地域可用** [创建基线评测任务](../../raw/model-user-guide/model-evaluation-introduction/evaluation-task-introduction/create-baseline-evaluation-task.md)。
- **核心功能**：
  - 多轮对话（ChatML）与单轮（[prompt](prompt.md)&completion）格式评测集支持；
  - Pass@K 聚合分析（需设置单样本推理次数 >1）；
  - 结果分桶、导出与回流至数据管理模块；
  - 排行榜跨模型横向对比（绑定统一评测维度）。

> **注意**：文档 3 和文档 6 均指出基线评测“仅北京地域可用”，但文档 6 的标题与正文明确强调该限制属“重要”且“其他地域不显示此选项，属正常现象”，而文档 3 在“自定义评测与基线评测”表格中仅标注“可用范围：仅北京地域”，未加粗提示。此处以文档 6 的强语气为准，确认为硬性地域限制，非配置疏漏。

## 关键参数

| 参数类别 | 参数名 | 说明 | 是否必填 | 约束 |
|----------|--------|------|-----------|------|
| **评测维度** | 维度类型 | 5 种之一：大模型评估-数值型/分类型、规则评估-字符串匹配/文本相似度、人工评估-分类型 | 是 | 创建后不可更改 |
| | 评分范围 | 仅数值型需配置，整数区间（如 `0~5`） | 数值型必填 | 最小值 ≥ 0，最大值 ≥ 1 |
| | 通过阈值 | 判定 Pass/Fail 的分界线（数值型/相似度型必填） | 是 | 步长 0.1（数值型）、0.01（相似度型） |
| **评测任务** | 数据来源 | “评测数据集”（触发模型推理）或“推理结果集”（仅评分） | 是 | 评测数据集须为已发布的 EvaluationSet 类型 [创建自定义评测任务](../../raw/model-user-guide/model-evaluation-introduction/evaluation-task-introduction/create-custom-evaluation-task.md) |
| | 单样本推理次数 | 控制每条样本的推理采样次数（影响 Pass@K 计算） | 否 | 默认 1；>1 时费用与耗时线性增加 |
| | 并发数 | 控制评测执行并发量 | 否 | 可设 1~20，默认 8，不影响结果 |

## 使用方式

1. **准备评测集**：在[数据管理](https://bailian.console.aliyun.com/cn-beijing/model/data)中创建类型为“评测集”的数据集，选择样本格式（`文本生成（prompt&completion）` 或 `文本生成（ChatML-messages）`），按模板上传数据 [训练集与评测集](../../raw/model-user-guide/model-evaluation-introduction/training-set-and-evaluation-set.md)。
2. **创建评测维度**：在[模型评测 → 评测维度](https://bailian.console.aliyun.com/cn-beijing/model/evaluate/dimension_template)中，选择预置模板（47 个）或自定义创建，明确类型、裁判模型（大模型评估）、算法（规则评估）或标签（人工评估） [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)。
3. **创建评测任务**：
   - 自定义评测：选择模型 → 配置数据来源（评测数据集/推理结果集）→ 关联至少一个评测维度 → 设置推理参数与并发数 → 开始评测；
   - 基线评测：选择模型 → 勾选目标 Benchmark（如 GSM8K、HumanEval）→ 开始评测。
4. **查看与分析结果**：任务完成后，在“任务总览”查看综合得分，“Case 分析”中切换“逐次采样”或“按题聚合”视图，支持分桶筛选难例并导出回流 [查看评测结果](../../raw/model-user-guide/model-evaluation-introduction/evaluation-task-introduction/view-evaluation-results.md)。

## 限制和注意事项

- **地域限制**：基线评测功能仅在北京地域可用，其他地域控制台不显示该选项 [创建基线评测任务](../../raw/model-user-guide/model-evaluation-introduction/evaluation-task-introduction/create-baseline-evaluation-task.md)。
- **数据集约束**：评测集仅支持文本生成场景，不支持视觉理解、图生视频等训练场景；评测集不可通过 OSS 导入方式创建 [训练集与评测集](../../raw/model-user-guide/model-evaluation-introduction/training-set-and-evaluation-set.md)。
- **维度类型锁定**：评测维度的“类型”字段创建后不可修改，选错需删除重建；若该维度已被排行榜引用，则必须先移除关联才能删除 [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)。
- **费用关键点**：
  - 使用“评测数据集”作为数据来源时，产生被评测模型的推理费用（按 [Token](../concepts/token.md) 计费）；
  - 仅大模型评估维度产生裁判模型评分费用；规则评估与人工评估无此项费用；
  - 推理结果集方式可规避重复推理费用，推荐用于多轮评测迭代 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。
- **功能缺失**：模型评测当前**不提供公开 API/SDK**，所有操作均需通过控制台完成；如需编程化集成，需参考 PAI Judge Model API 替代方案 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。

## 来源文档

- [训练集与评测集](../../raw/model-user-guide/model-evaluation-introduction/training-set-and-evaluation-set.md)
- [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)
- [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)
- [评测任务](../../raw/model-user-guide/model-evaluation-introduction/evaluation-task-introduction.md)
- [创建自定义评测任务](../../raw/model-user-guide/model-evaluation-introduction/evaluation-task-introduction/create-custom-evaluation-task.md)
- [创建基线评测任务](../../raw/model-user-guide/model-evaluation-introduction/evaluation-task-introduction/create-baseline-evaluation-task.md)
- [查看评测结果](../../raw/model-user-guide/model-evaluation-introduction/evaluation-task-introduction/view-evaluation-results.md)
- [人工标注评测](../../raw/model-user-guide/model-evaluation-introduction/evaluation-task-introduction/evaluation-manual-annotation.md)
- [排行榜](../../raw/model-user-guide/model-evaluation-introduction/evaluation-task-introduction/evaluation-leaderboard.md)
- [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-dimension-introduction.md)
- [大模型评估](../../raw/model-user-guide/model-evaluation-introduction/evaluation-dimension-introduction/evaluation-dimension-llm.md)
- [规则评估](../../raw/model-user-guide/model-evaluation-introduction/evaluation-dimension-introduction/evaluation-dimension-rule.md)
- [人工评估](../../raw/model-user-guide/model-evaluation-introduction/evaluation-dimension-introduction/evaluation-dimension-manual.md)


