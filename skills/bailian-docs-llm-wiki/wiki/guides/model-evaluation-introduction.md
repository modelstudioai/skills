# model evaluation introduction

模型评测是百炼平台提供的核心模型能力评估功能，支持通过标准化或自定义方式对文本生成类模型的推理结果进行量化打分与横向对比。它服务于模型选型、调优效果验证、能力基线建立和持续质量监控等关键研发场景。评测结果以综合得分、通过率及明细数据形式输出，为技术决策提供客观依据。

## 支持的模型/功能

- **支持模型类型**：仅限文本生成类（text-generation）模型，包括预置模型（如千问系列）和用户调优后的模型；不支持多模态、语音、向量模型等其他模态 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。
- **评测方式**：
  - **自定义评测**：使用用户上传的评测数据集（EvaluationSet 类型，含 `Prompt` 和 `Completion` 字段）或已有的推理结果集，搭配自定义创建的评测维度进行评分。
  - **基线评测**：内置覆盖通用知识、数学、代码、上下文推理、领域专项 5 大类共 13 个公开标准 benchmark（如 MMLU-Pro、GSM8K、HumanEval），自动执行、无需准备数据或配置维度；**仅在北京地域可用** [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。
- **评分器类型（即评测维度）**：共 5 种，分为三类范式：
  - *大模型评估*（需裁判模型）：数值型（0–5 整数分）、分类型（Pass/Fail 标签）；
  - *规则评估*（无裁判模型费用）：字符串匹配（相等/不相等/包含）、文本相似度（ROUGE/BLEU/Cosine 等 7 种算法）；
  - *人工评估*（无裁判模型费用）：分类型（人工标注 Pass/Fail） [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)。

> **注意**：文档 1 称“当前仅支持文本生成类模型评测”，而文档 2 未明确限定模型类型，但其所有示例与参数说明均基于 text-generation 场景。应以文档 1 的明确声明为准，后续文档若扩展支持需同步更新此限制。

## 关键参数

| 参数类别 | 关键字段 | 说明 | 约束与建议 |
|----------|----------|------|------------|
| **评测维度** | 维度类型 | 创建后不可修改，选错需删除重建 | 必须在创建前确认场景：有确定答案 → 规则评估；需语义理解 → 大模型评估；主观判断 → 人工评估 [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md) |
| | 裁判模型（大模型评估） | 如千问-Max，影响评分质量与费用 | 推荐千问-Max，推理能力强；费用按 Token 计费 |
| | 评分范围 / 通过阈值（数值型） | 默认 0–5，阈值默认 3.0，步长 0.1 | 范围建议 ≤10；阈值需结合业务容忍度设定（如 3.0=基础合格，4.0=优质） |
| | 匹配规则 / 相似度算法（规则评估） | 字符串匹配支持相等/不相等/包含；相似度支持 ROUGE-1/2/L、BLEU、Cosine 等 | 翻译→BLEU，摘要→ROUGE-L，语义相关→Cosine [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md) |
| **评测任务** | 数据来源 | “评测数据集”（触发被测模型推理，产生推理费）或“推理结果集”（仅评分，零推理费） | 小规模验证建议用数据集；正式批量评测推荐复用已下载的推理结果集降本 |
| | System Prompt | 配置于任务级，作用于被测模型，非裁判模型 | 多数场景可留空；用于设定角色或行为约束（如“你是一名金融分析师”） |
| | 排行榜参与 | 开启后需绑定已有排行榜（排行榜绑定维度不可变） | 为确保公平对比，**强烈建议排行榜内所有任务使用相同数据集和维度** |

## 使用方式

1. **准备数据**：在数据管理模块上传 `EvaluationSet` 类型数据集（至少含 `Prompt` 和 `Completion` 两列），或准备已含 `Output` 的推理结果集文件。
2. **创建评测维度**：进入「评测维度」页签 → 「创建评测维度」→ 选择类型 → 配置参数（如裁判模型、评分器 Prompt、标签、算法等）。Prompt 中**必须包含至少一个变量**（`${prompt}` / `${output}` / `${completion}`），否则提交失败 [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)。
3. **创建评测任务**：
   - 自定义评测：选择「自定义评测」→ 指定被测模型 → 选择数据来源（数据集或结果集）→ 关联已创建的维度 → 设置推理参数（Temperature/TopP 等，System Prompt 可选）→ 提交。
   - 基线评测：选择「基线评测」→ 选择被测模型 → 勾选目标 benchmark（如 GSM8K、HumanEval）→ 可选开启数据采样 → 提交。
4. **查看结果**：
   - 自定义评测：任务完成后，「指标统计」页查看综合得分、通过率、分数分布；「数据明细」页查看每条样本的 Prompt/Output/Completion 及各维度评分。
   - 基线评测：提供「任务总览」「基线评分明细」「Case 分析」「多任务对比」四页签，支持雷达图、Bad Case 定位与多模型横向对比。

## 限制和注意事项

- **地域限制**：基线评测**仅在北京地域（华北2）可用**，其他地域控制台不显示该选项，属正常现象 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。
- **模型限制**：仅支持文本生成类模型；多模态、语音等模型暂不支持。
- **维度限制**：维度类型创建后不可修改；已被排行榜绑定的维度删除后，将导致该排行榜无法新建任务（绑定维度为空）。
- **费用说明**：
  - 被测模型推理费：使用「评测数据集」时产生；使用「推理结果集」时为 0。
  - 裁判模型评分费：仅大模型评估维度（数值型/分类型）产生；规则评估与人工评估无此项费用。
  - 成本优化建议：先用 50–100 条数据小规模验证配置；保存并复用推理结果集；优先选用规则评估降低开销。
- **结果解读**：综合得分是各维度平均分，可能掩盖维度间差异；**务必结合分数分布与明细分析短板**；1–3% 的分差通常属评测噪声，不宜作为决策唯一依据。

## 来源文档

- [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)
- [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)


