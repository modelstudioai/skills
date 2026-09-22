# agenteval

`agenteval` 是百炼 Evolution 平台中面向 AI Agent 全生命周期管理的核心能力模块，提供可观测性（Observability）、自动化评测（Evaluation）与 Prompt 智能优化（Optimization）三位一体的闭环能力。它不依赖特定开发框架，基于 OpenTelemetry GenAI 标准实现链路接入，支持从线上 Trace 沉淀到评测集、从多维评估到版本化 Prompt 迭代的完整工程化路径，专为开发者设计，聚焦问题定位、质量量化与效果提升。

## 支持的模型/功能

- **观测能力**：支持智能体应用（Agent 1.0 / 2.0）和工作流应用的全链路追踪，覆盖 Prompt 解析、大模型调用（含 TTFT、[Token](../concepts/token.md) 消耗）、工具执行（MCP）、向量检索、记忆读写等节点；但**暂不支持通过 Assistant API 创建的智能体应用** [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)。
- **评测能力**：支持多维度自动化评估，包括准确性、相关性、合规性、简洁性、格式规范性等。提供两类核心组件：
  - **预置评估器**：按「通用质量」「智能体」「文本匹配」「文本相似度」「格式校验」分类，开箱即用；
  - **自定义评估器**：支持 LLM 评估器（调用大模型语义评分）和 Code 评估器（Python 脚本规则判断），可基于历史评测任务的标注结果自动反演生成 LLM 评估器 [评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md)。
- **优化能力**：提供 Prompt 多版本对比调试、基于调试对话+人工反馈的智能优化、以及基于优质评测集数据的定向优化。所有优化操作均作用于草稿态 Prompt，**不会自动发布应用**，需人工验证后显式发布 [应用优化](../../raw/application-user-guide/agenteval/agenteval-optimization.md)。

> **注意**：文档 1 中称“支持任意框架、任意运行时快速接入”，但文档 3 明确指出“应用观测目前暂不支持通过 Assistant API 创建的智能体应用”。该限制适用于整个 `agenteval` 观测链路，属实际运行约束，非文档过时，应以文档 3 为准。

## 关键参数

| 参数类别 | 关键项 | 说明 |
|----------|--------|------|
| **评估器配置** | 评分范围、通过阈值 | 决定打分尺度（如 0–100 或 1–5）与 Pass/Fail 判定基准；LLM 评估器中需确保 Prompt 与评分范围一致 [评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md) |
| **评测任务** | 字段映射 | 必须将评估器所需参数（如 `query`, `response`, `reference`）准确映射至评测集字段或模型输出；映射错误将导致评估失败 [评测任务](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-task.md) |
| **标签管理** | 标签类型（分类/布尔/数字/文本） | 影响标注方式与筛选能力；例如分类标签支持多选，数字标签支持范围筛选，文本标签用于自由备注 [标签管理](../../raw/application-user-guide/agenteval/agenteval-tags/agenteval-tag-management.md) |
| **告警规则** | 持续时间、检查周期、阈值、统计周期 | 告警触发依赖指标在指定统计周期内持续满足阈值条件；预置模板已覆盖 QPM、错误率、TTFT 等常见场景 [告警管理](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-alert-management.md) |

## 使用方式

1. **观测接入**：  
   - 主账号完成可观测链路 OpenTelemetry 服务授权、开通与 LogStore 初始化；  
   - 在应用观测页面开启目标应用的观测，Trace 数据分钟级同步；  
   - 可直接将 Span 数据批量导入评测集，构建真实业务评测样本 [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)。

2. **评测构建**：  
   - 创建评测集（需发布后方可使用），选择类型（智能体/工作流/自定义）并规划表结构；  
   - 创建或选用评估器，严格按其必选参数（如 `query`+`response`）设计评测集字段；  
   - 创建评测任务，关联评测集、应用及 ≥1 个评估器，完成参数映射后发起批量评测。

3. **Prompt 优化**：  
   - 在应用优化页面发起任务，支持两种路径：  
     - **版本对比**：设置基准组与对照组 Prompt，输入问题并对比输出差异，一键采纳最优配置；  
     - **调试反馈**：输入测试问题 → 选择代表性调试结果 → 描述具体问题与期望行为 → 生成优化 Prompt → 采纳并验证。

## 限制和注意事项

- **API 缺失**：应用观测模块当前**无公开 API**，所有操作需通过控制台完成 [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)。  
- **评测集状态约束**：评测集必须处于**已发布**状态才能用于评测任务；草稿状态不可用，且发布后无法直接编辑表结构 [评测集](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-set.md)。  
- **评估器依赖限制**：自定义评估器被评测任务引用后，**无法删除**；删除前需确认无任务依赖 [评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md)。  
- **优化生效流程**：所有 Prompt 采纳操作仅更新草稿，**必须手动调试验证 + 点击发布**才生效；未发布版本对线上流量无影响 [应用优化](../../raw/application-user-guide/agenteval/agenteval-optimization.md)。  
- **告警通知渠道**：告警历史列表中**不展示具体通知渠道（如邮箱、短信）信息**，仅显示联系人/联系人组 [告警管理](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-alert-management.md)。

## 来源文档

- [概览](../../raw/application-user-guide/agenteval/agenteval-introduction.md)
- [快速开始](../../raw/application-user-guide/agenteval/agenteval-quick-start.md)
- [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)
- [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability.md)
- [应用评测](../../raw/application-user-guide/agenteval/agenteval-evaluation.md)
- [告警管理](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-alert-management.md)
- [评测集](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-set.md)
- [评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md)
- [评测任务](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)
- [应用优化](../../raw/application-user-guide/agenteval/agenteval-optimization.md)
- [标签管理](../../raw/application-user-guide/agenteval/agenteval-tags.md)
- [更新日志](../../raw/application-user-guide/agenteval/agenteval-changelog.md)
- [标签管理](../../raw/application-user-guide/agenteval/agenteval-tags/agenteval-tag-management.md)


