# agenteval

`agenteval` 是百炼平台 Evolution 体系中面向 AI Agent 全生命周期质量保障的核心模块，提供可观测性（Observability）、自动化评测（Evaluation）与 Prompt 持续优化（Optimization）三位一体的能力。它不依赖特定开发框架，基于 OpenTelemetry GenAI 标准实现链路采集，并支持从线上 Trace 沉淀评测样本、多维评估器量化输出质量、以及基于调试反馈智能迭代 Prompt，形成“观测 → 评测 → 优化”闭环。该能力已集成于百炼控制台，当前为 Web 控制台功能，暂无公开 API [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)。

## 支持的模型/功能

- **可观测性**：支持智能体应用（Agent 1.0 / 2.0）和工作流应用的全链路追踪，覆盖 Prompt 解析、大模型调用（含 TTFT、耗时、Token）、工具执行（MCP）、向量检索、记忆读写等节点；支持分钟级监控指标（QPM、错误率、Token 分析）与限流统计 [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)。
- **评测能力**：
  - **评测集**：支持智能体/工作流/自定义类型，字段结构可编辑，需发布后方可使用 [评测集](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-set.md)。
  - **评估器**：提供预置模板（通用质量、智能体、文本匹配、相似度、格式校验）及自定义能力：
    - *LLM 评估器*：支持选择百炼托管模型（限时免费），配置 Prompt、评分范围（如 0–100）、通过阈值；
    - *Code 评估器*：支持 Python 3.10 脚本，函数须返回数值评分，无额外 Token 成本；
    - *基于评测任务创建*：从已完成标注的历史任务中自动提炼 LLM 评估规则。
- **优化能力**：支持两种路径：
  - *版本对比优化*：并行调试多组 Prompt 变体，直观比对输出差异；
  - *调试&反馈优化*：基于单条或多条调试对话 + 人工反馈（需明确描述问题现象与期望行为），生成优化版 Prompt。

> **注意**：文档 4 明确指出“应用观测目前暂无 API”，但文档 1 中“框架中立、即插即用”表述易被误解为支持 SDK 接入。实际当前仅支持控制台配置与 OpenTelemetry 链路上报，**不提供 agenteval 功能的独立 SDK 或 REST API**。

## 关键参数

| 参数类别 | 关键项 | 说明 |
|----------|--------|------|
| **评估器通用** | 评分范围 | 决定打分尺度（如 `0–1` 用于二分类，`0–100` 用于精细区分）；必须与 Prompt 中的指令一致。 |
| | 通过阈值 | 评分 ≥ 阈值为 Pass；建议设为评分范围中位数（如范围 `0–100`，阈值设 `50`）。 |
| **LLM 评估器** | 模型选择 | 建议选用 32B+ 参数量模型以提升语义理解准确性；评估模型调用按实际 Token 计费。 |
| | Prompt 设计 | 需明确评分标准、步骤、输出格式；支持插入预置模板；试运行验证必做。 |
| **Code 评估器** | 函数签名 | 必须包含所有入参（如 `query`, `response`），返回数值类型结果。 |
| **评测任务** | 字段映射 | 所有评估器变量（如 `query`, `reference`, `response`）必须映射到评测集字段或模型输出；映射错误将导致评估失败。 |
| **标签** | 类型 | 分类/布尔/数字/文本四类；数字标签支持筛选（`>`, `<=` 等），文本标签支持模糊搜索（`包含`/`不包含`）。 |

## 使用方式

1. **接入准备**：
   - 主账号完成可观测链路 OpenTelemetry 服务授权、开通与 LogStore 初始化（子账号需主账号授予权限）；
   - 应用需已发布，且属于当前业务空间。

2. **核心流程**：
   - **观测**：在[应用观测](https://bailian.console.aliyun.com/loop/app-observe)开启目标应用观测 → 查看 Trace 列表与监控统计 → 可导出 JSONL/Excel 数据 → 支持将 Span 直接添加至评测集 [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)。
   - **评测**：
     - 创建并发布评测集（类型需匹配应用）；
     - 创建评估器（预置或自定义），注意字段要求；
     - 创建评测任务：关联评测集、应用、评估器（≤10 个），完成参数映射；
     - 查看数据明细（自动评分 + 人工标签）与指标统计（综合得分、进度、分布）。
   - **优化**：
     - 进入应用优化页，选择目标应用；
     - 选择「对比模式」调试多版本 Prompt，或「根据调试结果优化 Prompt」输入问题与人工反馈；
     - 采纳优化结果 → **手动调试验证**（原问题、正常场景、边界场景）→ 点击发布生效。

3. **告警与标注**：
   - 告警管理支持基于预置/自定义模板配置 QPM、错误率等指标阈值告警 [告警管理](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-alert-management.md)；
   - 标签可用于评测任务人工标注及应用观测 Span 标注，支持四类类型与多维筛选。

## 限制和注意事项

- **功能限制**：
  - 应用观测**不支持通过 Assistant API 创建的智能体应用**；
  - 评测集最大文件上传 20 MB（xls/xlsx），单次最多映射 50 个字段；
  - 每个评测任务最多添加 10 个评估器，最多关联 50 个应用至单条告警规则；
  - 基于评测任务创建的评估器**不支持试运行**，需在真实评测中验证效果。

- **关键注意事项**：
  - **评测集必须发布后才能用于评测任务**，草稿状态不可用；
  - **评测任务创建后配置不可修改**（应用、评测集、评估器映射），需新建任务；
  - “不关联应用”的评测任务仅支持纯人工标注，不触发模型调用；
  - 采纳优化结果**不会自动发布应用**，必须手动验证后点击“发布”；
  - LLM 评估器与评测任务均产生 Token 消耗，费用按百炼计费规则结算；
  - 多条调试结果用于优化时，应聚焦同一问题目标，避免反馈冲突降低优化质量。

## 来源文档

- [概览](../../raw/application-user-guide/agenteval/agenteval-introduction.md)
- [快速开始](../../raw/application-user-guide/agenteval/agenteval-quick-start.md)
- [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability.md)
- [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)
- [告警管理](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-alert-management.md)
- [应用评测](../../raw/application-user-guide/agenteval/agenteval-evaluation.md)
- [评测集](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-set.md)
- [评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md)
- [评测任务](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)
- [应用优化](../../raw/application-user-guide/agenteval/agenteval-optimization.md)
- [标签管理](../../raw/application-user-guide/agenteval/agenteval-tags.md)
- [更新日志](../../raw/application-user-guide/agenteval/agenteval-changelog.md)
- [标签管理](../../raw/application-user-guide/agenteval/agenteval-tags/agenteval-tag-management.md)


