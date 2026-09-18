# agenteval

`agenteval` 是百炼平台 Evolution 体系中面向 AI Agent 全生命周期管理的核心能力模块，聚焦于**可观测性（Observability）** 与**系统化评测（Evaluation）** 两大支柱。它通过 OpenTelemetry 标准实现框架中立的链路采集，支持对智能体/工作流应用的端到端执行过程进行可视化追踪、指标监控、异常告警，并提供基于评测集、评估器和标签的多维自动化质量评估能力。开发者可将线上真实调用数据（Span）直接沉淀为评测样本，实现观测与评测闭环。

## 支持的模型/功能

- **可观测能力**：完整支持智能体应用（Agent 1.0 / Agent 2.0）和工作流应用的全链路追踪，覆盖 Prompt 解析、大模型调用（含 TTFT、耗时、Token）、MCP 工具执行、向量检索、记忆读写等节点 [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)。  
- **评测能力**：支持智能体、工作流、自定义三类评测集；提供预置评估器（通用质量、智能体、文本匹配、相似度、格式校验）及自定义 LLM/Code 评估器；支持人工标签（分类/布尔/数字/文本）与自动评估协同分析 [评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md)。  
- **告警能力**：基于预置或自定义模板配置 QPM、错误率、TTFT 等指标的阈值告警，支持邮件等多渠道通知 [告警管理](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-alert-management.md)。  
- **标注能力**：支持在应用观测 Span 和评测任务数据上添加结构化标签，用于质量归因与维度分析 [标签管理](../../raw/application-user-guide/agenteval/agenteval-tags/agenteval-tag-management.md)。

> **注意**：应用观测明确说明“暂不支持通过 Assistant API 创建的智能体应用”[应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)，但概览文档未提及此限制。实际接入前请确认应用创建方式。

## 关键参数

| 参数类别 | 关键项 | 说明 |
|----------|--------|------|
| **评估器配置** | `评分范围`、`通过阈值` | 决定打分尺度（如 0–100 或 1–5）与 Pass/Fail 判定基准；LLM 与 Code 评估器均需配置，且须与 Prompt 中的规则一致 [评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md)。 |
| **评测集字段** | `query`、`response`、`reference_response` 等 | 预置评估器对字段名有强依赖（如「问答相关性」必含 `query` 和 `response`），构建评测集前需按目标评估器要求规划表结构 [评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md)。 |
| **告警规则** | `持续时间`、`告警检查周期`、`统计周期` | 告警触发需满足指标在指定持续时间内持续越界；检查周期默认 60 秒，统计周期单位为分钟（1–10080） [告警管理](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-alert-management.md)。 |

## 使用方式

1. **开启观测**：主账号完成 OpenTelemetry 服务角色授权、开通服务及初始化 LogStore 后，在[应用观测](https://bailian.console.aliyun.com/loop/app-observe)页面为已发布应用开启观测，数据以分钟级频率同步 [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)。  
2. **构建评测集**：在[评测集](https://bailian.console.aliyun.com/loop/app-evaluate/eval-set)页面创建并**发布**评测集（草稿不可用），支持空集创建或 Excel 导入（≤20 MB），需按评估器要求配置字段 [评测集](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-set.md)。  
3. **创建评测任务**：在[评测任务](https://bailian.console.aliyun.com/loop/app-evaluate/eval-task)页面选择已发布评测集、关联应用（或选“不关联应用”用于纯人工标注），并至少添加 1 个评估器（最多 10 个）；所有评估器变量必须完成字段映射后方可保存 [评测任务](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)。  
4. **配置告警**：在[告警管理](https://bailian.console.aliyun.com/loop/alert-manage)页面基于预置模板快速创建规则，或自定义复合条件；限流告警需结合限流统计页签配置 [告警管理](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-alert-management.md)。  

## 限制和注意事项

- **API 限制**：应用观测功能当前**无开放 API**，所有操作需通过控制台完成 [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)。  
- **评测任务不可修改**：任务创建后，其关联的评测集、应用、评估器配置均不可变更；如需调整，必须新建任务 [评测任务](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)。  
- **评估器依赖约束**：被评测任务引用的评估器无法删除；基于评测任务创建的评估器**不支持试运行**，需在实际任务中验证效果 [评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md)。  
- **数据时效性**：观测数据同步延迟为分钟级；监控与限流统计数据最长支持查询 30 天，聚合粒度支持分钟/小时/天 [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)。  
- **权限要求**：首次开通应用观测需主账号操作；子账号需主账号授予相应 OpenTelemetry 权限 [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)。

## 来源文档

- [概览](../../raw/application-user-guide/agenteval/agenteval-introduction.md)
- [快速开始](../../raw/application-user-guide/agenteval/agenteval-quick-start.md)
- [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability.md)
- [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)
- [告警管理](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-alert-management.md)
- [评测集](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-set.md)
- [应用评测](../../raw/application-user-guide/agenteval/agenteval-evaluation.md)
- [评测任务](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)
- [评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md)
- [标签管理](../../raw/application-user-guide/agenteval/agenteval-tags.md)
- [标签管理](../../raw/application-user-guide/agenteval/agenteval-tags/agenteval-tag-management.md)
- [更新日志](../../raw/application-user-guide/agenteval/agenteval-changelog.md)


