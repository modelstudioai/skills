# 模型与应用评测

模型与应用评测是百炼平台面向开发者提供的核心质量保障能力，用于对大模型（Model）及基于其构建的智能体、工作流等上层应用（Application）进行结构化、可复用、可量化的效果评估。它既支持通过标准 Benchmark 或自定义数据集对模型本身的能力进行横向比对与纵向调优，也支持围绕真实业务场景对应用输出质量、链路健壮性与用户体验进行端到端闭环验证。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型评测（Model Evaluation）**：聚焦于文本生成类模型（如 Qwen 系列）的基础能力验证，适用于模型选型、调优效果归因、SFT/RLHF 后效果验收等场景。支持两种路径：  
  - **基线评测**：一键运行 13 个公开 Benchmark（如 GSM8K、MMLU-Pro），无需准备数据或配置，仅限北京地域；  
  - **自定义评测**：上传含 `Prompt`/`Completion` 的评测集，搭配大模型评估（LLM Grader）、规则评估（BLEU/ROUGE/Fuzzy Match）或人工评估维度，实现按需定制的细粒度打分。

- **应用评测（Application Evaluation）**：聚焦于已发布的智能体（Agent 1.0）和工作流（Workflow）应用，评估其在真实交互链路中的综合表现。支持双轨并行：  
  - **自动评测**：基于知识库自动生成评测集，调用 `qwen-max` 或 `qwen-plus` 对应用输出做语义评分，并输出 BadCase 归因（如“检索无效”“逻辑断裂”）与调优建议；  
  - **手动评测**：支持上传 `.xls`/`.xlsx` 格式对话分析集，由人工标注“较差/一般/较好”，用于关键场景的效果终验或 A/B 测试。

- **评测与监控协同使用**：  
  - 应用观测（Application Monitoring）采集的 Span 数据（含 `Prompt`、`Completion`、`Trace ID`、Token 量、延时等）可**一键导出为评测集**，实现从问题发现（监控告警）→ 样本沉淀（Span 导出）→ 质量归因（评测打分）→ 优化验证（重跑评测）的完整闭环；  
  - 模型监控（Model Monitoring）不直接参与评测，但其失败率、首 Token 延时等指标可作为评测任务的前置筛选条件（例如：仅对失败率 < 1% 的时段样本发起评测），提升评测结果的业务代表性。

> ⚠️ 注意：模型评测与应用评测是两个独立功能模块，**不可混用**——模型评测仅支持纯模型调用（无 RAG/Tool/Workflow 编排），应用评测仅支持已发布且启用“应用观测”的 Agent/Workflow 应用。

## 关键参数和配置

| 类别 | 参数/配置项 | 说明 | 开发者须知 |
|--------|--------------|------|-------------|
| **通用** | 评测集字段 | 模型评测：必含 `Prompt` + `Completion`（+ 可选 `ReferenceAnswer`）；应用评测：知识问答类需 `query`/`referenceAnswer`/`queryType`，对话分析类需 `Prompt`/`Completion` | 字段名严格匹配，大小写敏感；上传 `.jsonl` 推荐，`.xls`/.xlsx` 需首行为列名 |
| **评估器/维度** | LLM 评估器 | 必选裁判模型（如 `qwen-max`）、评分 Prompt（必须含 `${[prompt](../guides/prompt.md)}`/`${response}` 变量）、评分范围（推荐 `0~5`）、通过阈值 | Prompt 中避免模糊指令（如“请打分”），应明确标准（如“答案是否完整覆盖所有要点？”） |
| | Code 评估器 | 入参映射（如 `response → Completion`）、Python 函数（返回 `float` 分数）、支持 JSON Schema 校验、正则匹配等确定性逻辑 | 函数需幂等、无副作用；超时默认 3s，复杂逻辑建议拆分为多个轻量评估器 |
| | 标签类型 | 分类（多选枚举）、布尔（True/False）、数字（Double）、文本（String） | 标签用于后续筛选与归因分析，建议在评测任务创建阶段即预设，避免后期补标 |
| **任务级** | 参数映射 | 将评测集字段（如 `Completion`）与评估器变量（如 `response`）显式绑定 | 映射错误将导致评估器跳过执行，控制台提示“未找到输入字段” |
| | 多应用横向评测 | 单次最多支持 8 个应用并行评测 | 适用于版本迭代对比（v1 vs v2）或不同策略 A/B 测试（RAG vs Fine-tuning） |

## 面向开发者，简洁实用

- ✅ **起步建议**：  
  - 新手先用「基线评测」快速摸底模型能力；  
  - 应用评测优先启用「应用观测」，再从高频失败 Span 中导出 50–100 条样本构建最小可行评测集；  
  - 评估器组合推荐：`LLM 语义相关性 + Code JSON 格式校验 + 布尔标签（是否含联系方式）`。

- ✅ **避坑指南**：  
  - 评测集发布后**类型不可修改**（如知识问答 → 对话分析），需删重建；  
  - 评测任务创建后**配置不可编辑**，调整需新建任务；  
  - 自动评测要求应用**已发布 + 已配知识库 + 已开通应用观测**，缺一不可；  
  - LLM 评估器会产生额外 Token 费用（按裁判模型计费），规则/人工评估器免费。

- ✅ **效能提示**：  
  - 使用「评测任务」页面的「BadCase 分析」视图，直接定位低分样本共性（如 70% 低分源于 `fineKeywords` 匹配失败）；  
  - 将评测结果与监控看板联动：当「应用观测」中 `RETRIEVER` 节点平均延时突增时，针对性评测检索模块输出质量；  
  - 所有评测结果支持导出 Excel，便于嵌入团队周会复盘或客户交付报告。

## 关联主题页

- [application evaluation](../guides/application-evaluation.md)
- [model evaluation introduction](../guides/model-evaluation-introduction.md)
- [model monitoring](../guides/model-monitoring.md)
- [application monitoring](../guides/application-monitoring.md)
- [use cases](../guides/use-cases.md)


