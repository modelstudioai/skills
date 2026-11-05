# model evaluation introduction

模型评测是百炼平台用于量化评估大语言模型能力的核心功能，支持自定义评测与基线评测两种模式。它通过可复用的评测维度（如大模型评估、规则评估、人工评估）对模型输出进行打分或分类，并基于评测集生成结构化报告与排行榜，帮助开发者完成模型选型、调优效果验证和持续质量监控。整个流程围绕数据集、评测维度、评测任务三要素展开，强调配置可复用、结果可对比、成本可优化。

## 支持的模型/功能

- **支持的模型类型**：当前仅支持文本生成类模型（包括预置模型与调优后的 SFT/DPO 模型），不支持视觉理解、图生视频等多模态模型的评测 [训练集与评测集](../../raw/model-user-guide/model-evaluation-introduction/training-set-and-evaluation-set.md)。
- **核心评测方式**：
  - **自定义评测**：使用用户上传的评测集（`EvaluationSet` 类型）和自定义/预置评测维度，支持单轮（`prompt&completion`）与多轮对话（`ChatML-messages`）格式；
  - **基线评测**：内置 5 大类、13 个公开标准 Benchmark（如 MMLU-Pro、GSM8K、HumanEval），无需准备数据集或维度，但**仅在北京地域可用** [创建基线评测任务](../../raw/model-user-guide/model-evaluation-introduction/evaluation-task-introduction/create-baseline-evaluation-task.md)。
- **评分器类型**：共五种，覆盖全自动与人工场景：
  - 大模型评估（分类型/数值型）：由裁判模型（如千问-Max）按 Prompt 语义评分；
  - 规则评估（字符串匹配/文本相似度）：算法直接计算，零裁判模型费用；
  - 人工评估（分类型）：人工逐条标注 Pass/Fail 标签 [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)。

> **注意**：文档 3 与文档 7 均指出基线评测“仅北京地域可用”，但文档 3 在“自定义评测与基线评测”表格中将“可用范围”列为“全地域”（对应基线评测列），该处存在矛盾；以文档 7 的明确声明为准——基线评测**仅限北京地域**，其他地域控制台不显示该选项。

## 关键参数

| 参数类别 | 参数名 | 说明 | 是否必填 | 约束与建议 |
|----------|--------|------|-----------|-------------|
| **评测维度** | 类型 | 5 种评分器类型之一，创建后不可更改 | 是 | 选错需删除重建；有标准答案优先选规则评估，无标准答案需语义理解则选大模型评估 [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md) |
| | 裁判模型 | 仅大模型评估类型需指定 | 是（大模型评估） | 推荐 `qwen-max`，当前限时免费调用 [大模型评估](../../raw/model-user-guide/model-evaluation-introduction/evaluation-dimension-introduction/evaluation-dimension-llm.md) |
| | 评分范围 / 通过阈值 | 数值型：整数区间（如 `0~5`）；所有类型均需设通过阈值（如 `3.0`） | 是（数值型必填范围；所有类型必填阈值） | 评分范围建议 ≤10；阈值步长 0.1，需结合业务容忍度设定 [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md) |
| **评测任务** | 数据来源 | “评测数据集”（触发模型推理）或“推理结果集”（仅评分） | 是 | 评测数据集须为已发布的 `EvaluationSet` 类型；推理结果集可复用降低费用 [创建自定义评测任务](../../raw/model-user-guide/model-evaluation-introduction/evaluation-task-introduction/create-custom-evaluation-task.md) |
| | 单样本推理次数 | 每条样本执行推理的次数（默认 1） | 否 | >1 时支持计算 `Pass@K`，用于难例挖掘；费用与次数成正比 [查看评测结果](../../raw/model-user-guide/model-evaluation-introduction/evaluation-task-introduction/view-evaluation-results.md) |
| | 并发数 | 控制评测执行并发量（默认 8） | 否 | 范围 1~20，影响速度但不影响结果 |

## 使用方式

1. **准备数据**：在[数据管理](https://bailian.console.aliyun.com/cn-beijing/model/data)中创建并发布 `EvaluationSet` 类型数据集，格式支持 `prompt&completion`（单轮）或 `ChatML-messages`（多轮） [训练集与评测集](../../raw/model-user-guide/model-evaluation-introduction/training-set-and-evaluation-set.md)。
2. **定义维度**：在**模型评测 > 评测维度**页创建评测维度模板，选择类型并配置参数（如裁判模型、Prompt、评分范围、匹配规则等）；推荐先试用预置模板（共 47 个：19 个大模型评估 + 28 个规则评估）快速启动 [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)。
3. **创建任务**：在**模型评测 > 评测任务**页选择“自定义评测”，依次选择被评测模型、数据来源（评测数据集或推理结果集）、关联已创建的评测维度，并设置推理参数（如 `temperature`）、并发数与单样本推理次数 [创建自定义评测任务](../../raw/model-user-guide/model-evaluation-introduction/evaluation-task-introduction/create-custom-evaluation-task.md)。
4. **查看与分析**：任务完成后，在详情页的**任务总览**查看综合得分与 Bad Case 数，在**Case 分析**页切换“逐次采样”或“按题聚合”视图，结合 `Pass@K` 和分桶定位难例；支持导出结果或回流至数据集用于后续调优 [查看评测结果](../../raw/model-user-guide/model-evaluation-introduction/evaluation-task-introduction/view-evaluation-results.md)。

## 限制和注意事项

- **地域限制**：基线评测功能仅在北京地域可用；DPO/CPT 训练方法及云存储挂载也仅限北京地域 [训练集与评测集](../../raw/model-user-guide/model-evaluation-introduction/training-set-and-evaluation-set.md)。
- **不可变性约束**：评测维度的“类型”、数据集的“类型”（训练集/评测集）、已发布数据集的版本均创建后不可修改，选错需删除重建 [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)。
- **费用关键点**：
  - 大模型评估维度产生**裁判模型评分费用**（按 [Token](../concepts/token.md) 计费）；
  - 规则评估与人工评估**无裁判模型费用**，是成本最低方案；
  - 使用“评测数据集”会触发被评测模型推理并产生**推理费用**；使用“推理结果集”可规避此费用 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。
- **人工评估特殊流程**：使用人工评估维度的任务，必须完成全部样本的人工标注后，任务状态才变为“评测完成”；未标注完前始终为“进行中” [人工标注评测](../../raw/model-user-guide/model-evaluation-introduction/evaluation-task-introduction/evaluation-manual-annotation.md)。
- **配置验证建议**：首次使用务必用小规模数据（50–100 条）验证维度配置与任务参数，避免大规模无效消耗 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。

## 来源文档

- [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)
- [训练集与评测集](../../raw/model-user-guide/model-evaluation-introduction/training-set-and-evaluation-set.md)
- [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)
- [创建自定义评测任务](../../raw/model-user-guide/model-evaluation-introduction/evaluation-task-introduction/create-custom-evaluation-task.md)
- [评测任务](../../raw/model-user-guide/model-evaluation-introduction/evaluation-task-introduction.md)
- [查看评测结果](../../raw/model-user-guide/model-evaluation-introduction/evaluation-task-introduction/view-evaluation-results.md)
- [创建基线评测任务](../../raw/model-user-guide/model-evaluation-introduction/evaluation-task-introduction/create-baseline-evaluation-task.md)
- [排行榜](../../raw/model-user-guide/model-evaluation-introduction/evaluation-task-introduction/evaluation-leaderboard.md)
- [人工标注评测](../../raw/model-user-guide/model-evaluation-introduction/evaluation-task-introduction/evaluation-manual-annotation.md)
- [大模型评估](../../raw/model-user-guide/model-evaluation-introduction/evaluation-dimension-introduction/evaluation-dimension-llm.md)
- [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-dimension-introduction.md)
- [规则评估](../../raw/model-user-guide/model-evaluation-introduction/evaluation-dimension-introduction/evaluation-dimension-rule.md)
- [人工评估](../../raw/model-user-guide/model-evaluation-introduction/evaluation-dimension-introduction/evaluation-dimension-manual.md)


