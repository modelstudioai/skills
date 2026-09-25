# model evaluation introduction

模型评测是百炼平台提供的核心模型能力评估功能，支持通过标准化或自定义方式对文本生成类模型的推理结果进行量化打分与横向对比。它服务于模型选型、调优效果验证、能力基线建立和持续质量监控等关键研发场景。评测结果以综合得分、通过率及明细数据形式输出，支撑数据驱动的模型决策。

## 支持的模型/功能

- **支持模型类型**：仅限文本生成类（Text Generation）模型，包括预置模型（如千问系列）和用户调优后的模型；不支持多模态、语音、向量等非文本生成类模型 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。
- **评测方式**：
  - **自定义评测**：使用用户上传的评测数据集（EvaluationSet 类型）或已有的推理结果集，配合自定义创建的评测维度进行评分；
  - **基线评测**：直接调用平台内置的 13 个公开标准 Benchmark（覆盖通用知识、数学、代码、上下文推理、领域专项 5 大类），无需准备数据或配置维度，但**仅在北京地域可用** [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。
- **评分器类型（即评测维度）**：共 5 种，分为三类范式：
  - *大模型评估*（需裁判模型）：数值型（0–5 整数分）、分类型（Pass/Fail 标签）；
  - *规则评估*（无裁判模型）：字符串匹配（相等/不相等/包含）、文本相似度（ROUGE/BLEU/Cosine 等 7 种算法）；
  - *人工评估*（无裁判模型）：分类型（人工标注 Pass/Fail） [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)。

> **注意**：文档 1 称“当前仅支持文本生成类模型评测”，而文档 2 未明确限定模型类型，但其所有示例与参数说明均围绕文本生成展开，且文档 1 为产品概览主文档，故以文档 1 的表述为准。

## 关键参数

| 参数类别 | 参数名 | 说明 | 是否必填 | 约束 |
|----------|--------|------|-----------|------|
| **通用** | 维度名称 | 评测模板标识，用于任务中引用 | 是 | ≤20 字符 |
| | 描述 | 补充说明评判目标 | 否 | ≤100 字符 |
| **大模型评估** | 裁判模型 | 执行评分的 LLM（如千问-Max） | 是（该类型下） | 影响费用与质量 |
| | 评分器 Prompt | 指导裁判模型打分的提示词 | 是（该类型下） | 必须含 `${prompt}` / `${output}` / `${completion}` 至少一个变量 |
| | 评分范围（数值型） | 如 `0–5`，整数区间 | 是（数值型） | 最小值 ≥ 0，最大值 ≥ 1 |
| | 通过阈值 | 判定 Pass 的最低分（数值型）或相似度（规则型） | 是（数值型/相似度型） | 步长 0.1（数值型）或 0.01（相似度型） |
| | Pass/Fail 标签（分类型） | 明确互斥、穷尽的分类标签 | 是（分类型） | 标签间不可重复 |
| **规则评估** | 比较操作符（字符串匹配） | 相等 / 不相等 / 包含 | 是（该类型下） | — |
| | 评估指标（文本相似度） | ROUGE-1/2/L、BLEU、Cosine、Fuzzy Match、Accuracy 等 | 是（该类型下） | — |

## 使用方式

1. **前置准备**：
   - 开通百炼账号并进入北京地域控制台（基线评测强制要求）；
   - 在**数据管理**模块上传评测数据集（类型为 `EvaluationSet`，含 `Prompt` 和 `Completion` 两列）或准备推理结果集（含 `Prompt`、`Output`、`Completion`）。

2. **创建评测维度**（必选）：
   - 进入**模型评测 → 评测维度**页签 → **创建评测维度**；
   - 选择类型（如“大模型评估-数值型”），按需配置裁判模型、Prompt、评分范围等；
   - 注意：类型创建后不可修改，选错需删除重建 [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)。

3. **创建评测任务**：
   - 进入**模型评测 → 评测任务**页签 → **创建评测任务**；
   - 选择方式（自定义 or 基线）→ 选择被评测模型 → 配置数据来源（评测数据集 or 推理结果集）→ 关联已创建的维度；
   - （可选）开启“参与排行”并绑定排行榜。

4. **查看与分析结果**：
   - 任务状态变为“评测完成”后，点击任务名进入详情页；
   - **指标统计**页查看综合得分、通过率、分数分布；
   - **数据明细**页逐条查看 Prompt / Output / Completion 及各维度评分；
   - 基线评测额外提供“Case 分析”“多任务对比”等深度分析页签 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。

## 限制和注意事项

- **地域限制**：基线评测功能仅在北京地域（华北2）可用，其他地域控制台不显示该选项，属正常行为 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。
- **模型限制**：仅支持文本生成类模型；多模态、Embedding、Speech 等模型暂不支持评测。
- **维度不可变性**：评测维度的类型创建后不可更改，误选需删除后重建；若已被排行榜绑定，需先解除绑定才能删除。
- **费用说明**：
  - 使用**评测数据集**作为数据源时，产生被评测模型的推理费用；
  - 使用**大模型评估**维度时，产生裁判模型的评分费用（按 [Token](../concepts/token.md) 计费）；
  - 规则评估与人工评估无裁判模型费用；
  - 使用**推理结果集**可避免重复推理费用 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。
- **结果解读建议**：综合得分是各维度平均值，可能掩盖维度间差异；应结合分数分布图与明细数据定位短板；1–3% 的分差通常属评测噪声，不宜作为决策依据 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。

## 来源文档

- [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)
- [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)


