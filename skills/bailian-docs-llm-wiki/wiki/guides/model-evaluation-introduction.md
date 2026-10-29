# model evaluation introduction

模型评测是百炼平台提供的核心模型能力评估功能，用于量化文本生成类模型在特定任务上的表现。它支持两种评测范式：基于用户自有数据与标准的**自定义评测**，以及基于公开基准的**基线评测**。通过多维度评分、排行榜对比和结构化报告，帮助开发者完成模型选型、调优验证与持续质量监控。

## 支持的模型/功能

- **支持模型类型**：仅限文本生成类模型（包括预置模型与调优后的模型），不支持视觉理解、图生视频等多模态模型 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。
- **评测方式**：
  - **自定义评测**：使用用户上传的评测集（EvaluationSet）或已有的推理结果集，支持大模型评估（AI 自动打分）、规则评估（ROUGE/BLEU/字符串匹配等算法）和人工评估三种评分方式。
  - **基线评测**：内置 5 大类、13 个公开标准 Benchmark（如 MMLU-Pro、GSM8K、HumanEval、LongBench-v2、FinanceQA），自动执行、无需准备数据或配置维度，但**仅在北京地域可用** [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。
- **复用能力**：评测维度可创建为模板，被多个评测任务复用；排行榜支持跨任务横向对比相同维度下的模型表现。

> **注意**：文档 2 中提到“评测集仅支持文本生成场景”，与文档 1 中“当前仅支持文本生成类模型评测”完全一致；但文档 1 明确指出基线评测“仅北京地域可用”，而文档 2 未提及其地域限制——该关键约束应以文档 1 为准，已在上文强调。

## 关键参数

| 参数类别 | 参数名 | 说明 | 必填性 | 注意事项 |
|----------|--------|------|--------|----------|
| **通用** | 维度名称 / 描述 | 维度模板标识与说明 | 名称必填 | 名称 ≤20 字符，描述 ≤100 字符 |
| **大模型评估** | 裁判模型 | 执行评判的 LLM（如千问-Max） | 是（仅大模型评估类型） | 影响评分质量与费用 [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md) |
| | 评分器 Prompt | 指导裁判模型打分的提示词 | 是（大模型评估） | 必须含 `${prompt}`、`${output}` 或 `${completion}` 至少一个变量 |
| | 评分范围（数值型） | 如 `0–5`，整数区间 | 是（数值型） | 范围过大（如 >10）会降低 LLM 评分一致性 |
| | 通过阈值 | ≥该值即判定为 Pass | 是（数值型/相似度型） | 步长 0.1（数值型）或 0.01（相似度型） |
| **规则评估** | 算法类型（文本相似度） | ROUGE-1/2/L、BLEU、Cosine、Fuzzy Match、Accuracy | 是（文本相似度） | 摘要推荐 ROUGE-L，翻译推荐 BLEU，语义相关推荐 Cosine |
| | 匹配规则（字符串匹配） | 相等 / 不相等 / 包含 | 是（字符串匹配） | Function Calling 场景常用“包含” |
| **人工评估** | Pass/Fail 标签 | 人工标注时选择的分类标签 | 是 | 标签间不可重复，且需互斥穷尽 |

## 使用方式

1. **准备数据**：在[数据管理](https://bailian.console.aliyun.com/cn-beijing/model/data)中创建并发布**评测集**（类型必须为“评测集”，场景为“文本生成”），包含 `Prompt` 与 `Completion` 两列 [训练集与评测集](../../raw/model-user-guide/model-evaluation-introduction/training-set-and-evaluation-set.md)。
2. **创建维度**：进入**模型评测 → 评测维度**，选择一种类型（如“大模型评估-数值型”），配置裁判模型、评分器 Prompt、评分范围与通过阈值等 [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)。
3. **创建任务**：
   - *自定义评测*：选择模型、数据来源（评测集或推理结果集）、关联维度，可选开启排行榜参与；
   - *基线评测*：仅北京地域可见，选择模型与 Benchmark（如 GSM8K + MATH-500），支持子维度勾选与数据采样。
4. **查看结果**：任务完成后，在详情页查看**指标统计**（综合得分、通过率、分布图）与**数据明细**（逐条 Prompt/Output/Completion/评分）；基线评测额外提供“Case 分析”与“多任务对比”。

## 限制和注意事项

- **地域限制**：基线评测功能仅在北京地域可用，其他地域控制台不显示该选项，属正常设计 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。
- **维度不可变**：评测维度创建后，其类型不可修改；选错需删除重建，且已绑定的排行榜将失效。
- **数据集约束**：评测集不支持从 OSS 导入；仅支持文本生成场景；名称/描述长度、导入方式等详见 [训练集与评测集](../../raw/model-user-guide/model-evaluation-introduction/training-set-and-evaluation-set.md)。
- **费用说明**：
  - 使用“评测数据集”作为数据源时，产生被评测模型的推理费用；
  - “大模型评估”维度产生裁判模型评分费用（按 [Token](../concepts/token.md) 计费）；“规则评估”与“人工评估”无裁判模型费用；
  - “推理结果集”作为数据源时不产生被评测模型推理费用。
- **结果解读建议**：避免仅依赖综合得分；应结合分数分布、Bad Case 分析及维度级得分定位短板；1–3% 的分差通常属于评测噪声，不宜作为决策依据。

## 来源文档

- [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)
- [训练集与评测集](../../raw/model-user-guide/model-evaluation-introduction/training-set-and-evaluation-set.md)
- [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)


