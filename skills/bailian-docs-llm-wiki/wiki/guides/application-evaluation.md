# application evaluation

应用评测是百炼平台用于量化评估大模型应用（尤其是智能体和工作流）效果的核心能力，支持人工打标与大模型自动评分双模式。它通过构建结构化评测集、配置多维评估器、执行端到端推理与对比分析，帮助开发者快速识别 BadCase、定位 RAG 流程瓶颈（如检索、重排、切片、模型理解等），并驱动 Prompt、知识库、模型等环节的持续优化。评测结果可直接用于版本对比、上线准入和质量回归。

## 支持的模型/功能

- **评测模式**：支持[手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)（人工打标）与[自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)（大模型自动评分）两种范式。
- **应用类型支持**：当前仅支持已发布的**智能体应用（Agent 1.0）**；工作流应用需使用新版评测集中的“工作流”类型评测集 [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)。
- **评估器类型**：提供预置模板（通用质量、智能体、文本匹配、文本相似度、格式校验）及自定义能力，包括：
  - **LLM评估器**：基于 `qwen-max` 或 `qwen-plus` 等大模型进行语义评分；
  - **Code评估器**：通过 Python 脚本实现精确规则判断（如 JSON 校验、关键词匹配）；
  - **基于评测任务创建的评估器**：从历史人工标注数据中自动提炼评估逻辑。
- **评测集类型**：支持三种结构化类型——**智能体**（按应用出入参生成）、**工作流**（按工作流节点定义）、**自定义**（任意表结构），取代旧版仅分“对话分析/知识问答”的二元分类 [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)。

> **注意**：文档 2（自动评测）称“仅支持已发布的智能体应用”，而文档 5（新版评测集）明确支持“工作流”类型评测集。实际功能以新版控制台为准，工作流应用评测需通过新版评测集流程启用，旧版自动评测界面不展示工作流选项。

## 关键参数

- **评测集字段**：不同评测集类型与评估器对字段要求不同。例如，使用“问答相关性”预置评估器时，评测集必须包含 `query` 和 `response` 字段；而旧版“知识问答”类型要求 `query`、`referenceAnswer`、`fineKeywords` 等 [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)。
- **评估器参数映射**：创建评测任务时，必须将评估器声明的变量（如 `query`, `reference`, `response`）**一一映射**到评测集字段或应用输出字段，映射错误将导致评估失败。
- **采样与权重**：自动评测中可配置各任务类型（事实型、分析型等）的采样数；新版评测任务支持为每个评估器设置权重，影响综合得分计算。
- **评分范围与阈值**：LLM/Code 评估器均需配置 `评分范围`（如 0–5、0–100）和 `通过阈值`（如 ≥4 判定为 Pass），该配置直接影响结果解读与自动化决策。

## 使用方式

1. **准备评测数据**：
   - 手动上传：支持 `.xls`/`.xlsx`（对话分析）、`.jsonl`（知识问答）；新版支持智能体/工作流类型模板下载。
   - 自动生成：基于知识库，由大模型生成知识问答类评测集（仅限自动评测场景）。
   - 从应用观测导入：将线上真实调用数据直接转为评测样本。

2. **创建与发布评测集**：
   - 上传后需**发布**才可用于评测任务（草稿不可用）；
   - 新版支持**版本管理**，每次发布生成新版本，评测任务可指定使用特定版本。

3. **配置评估体系**：
   - 在[标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)中创建分类/布尔/数字/文本标签，用于人工标注维度（如“回答质量：较差/一般/较好”）；
   - 在[评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)中创建或选用预置评估器，定义自动评分逻辑。

4. **发起评测任务**：
   - 选择已发布评测集、目标应用（单个或最多 8 个横向对比）、评估器与标签；
   - 配置参数映射、采样策略、模型（自动评测固定为 `qwen-max`/`qwen-plus`）；
   - 支持**试运行**验证流程，正式评测前可终止。

5. **分析与迭代**：
   - 查看总正确率、BadCase 归因（模型理解/重排/检索/切片/未获取知识）、RAG 各环节单项得分；
   - 基于归因分析实施优化（如调整切片策略、优化 Prompt），发布新版本后复用同一评测集对比效果。

## 限制和注意事项

- **文件限制**：手动上传评测集单次最多 10 个文件，单个 ≤20 MB；仅支持 `.xls`、`.xlsx`、`.jsonl` 格式。
- **权限要求**：子账号需具备 `管理员` 或 `应用评测-操作` 权限；自动评测还需开通 `应用观测` 并将目标应用加入观测列表。
- **模型依赖**：自动评测与 LLM 评估器强制依赖 `qwen-max` 或 `qwen-plus`，其他模型不可选；Code 评估器无模型调用成本。
- **评测集兼容性**：旧版“知识问答”`.jsonl` 评测集**不能直接用于新版智能体类型评测任务**，字段结构（如 `queryType` vs `query_type`）和映射逻辑存在差异，需按新版模板重构。
- **费用说明**：自动评测、LLM 评估器、手动评测的模型推理阶段均消耗 Tokens，计费 = 实际 Tokens × 模型单价；独占资源部署模型不额外收费，但公共资源调用会产生费用 [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)。
- **状态依赖**：评测任务要求应用处于**已发布**状态；评测集必须为**已发布**状态；基于评测任务创建评估器时，所选任务必须为**已完成评估**状态。

## 来源文档

- [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)
- [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)
- [新版应用评测](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation.md)
- [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)
- [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)
- [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)
- [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)


