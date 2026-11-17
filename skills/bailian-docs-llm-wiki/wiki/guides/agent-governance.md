# agent governance

agent governance 是百炼平台面向 AI Agent 全生命周期提供的统一治理能力集合，涵盖可观测性（Observability）、可评测性（Evaluation）与可优化性（Optimization）三大核心支柱，并内嵌原生安全防护体系。它不依赖特定框架，基于 OpenTelemetry GenAI 标准实现链路采集，支持从开发调试、线上运行到效果迭代的闭环管理，帮助开发者系统性提升 Agent 的稳定性、质量与安全性。

## 支持的模型/功能

- **观测能力**：支持 Agent 1.0、Agent 2.0 和工作流应用的全链路追踪（Trace），覆盖 Prompt 解析、大模型调用（含 TTFT、[Token](../concepts/token.md) 消耗）、工具执行（MCP）、知识库检索、记忆读写等节点；**不支持通过 Assistant API 创建的智能体** [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)。
- **评测能力**：支持多维度自动化评测，包括：
  - **输出评测**：准确性、简洁性、合规性等文本维度；
  - **轨迹评测**：基于结构化 `trajectory` 数据评估执行逻辑、工具调用成功率、回答忠实度等 [添加轨迹评测数据](../../raw/_short/agenteval-evaluation-set-trajectory-data-7bbfb9904b121823.md)；
  - **多模态评测**：支持图片、音频、视频及混排内容的理解与生成质量评估 [添加多模态评测数据](../../raw/_short/agenteval-evaluation-set-multimodal-data-660c12b477900b3c.md)。
- **优化能力**：支持基于调试对话、评测任务结果、线上 Trace 数据或评测集样本的 Prompt 智能优化，并提供多版本对比与一键采纳功能。
- **安全能力**：提供“量·挡·记”三层防护：默认防护自动生效（覆盖 Flow Agent 输入输出、Managed Agent 运行时、RAG 知识库、Memory 内容等）；高级防护支持 7 类策略（如提示词攻击、敏感数据外泄、RAG 数据投毒等），需服务授权后开通 [安全策略](../../raw/application-user-guide/agent-governance/security-guide/section-adv/policy.md)。

> **注意**：文档中多次提及“应用观测目前暂无 API”，但 Security 模块明确提供 `/api/v1/agentstudio/security` 下的 7 个 RESTful 接口（如 `/overview`, `/asset_summary`, `/policies`）。二者属不同子系统，观测能力当前仅限控制台使用，而安全治理能力已开放 API。

## 关键参数

| 功能模块 | 参数/配置项 | 说明 |
|----------|-------------|------|
| **观测** | `持续时间`、`告警检查周期`（秒） | 告警规则必填字段，用于定义触发条件的时间窗口与检测频率 [告警管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-alert-management.md) |
| **评测** | `评估器变量映射` | 必须确保评估器变量类型与评测集字段/应用输出字段严格一致（如 `trajectory` 类型变量只能映射到 `trajectory` 类型列） [评测任务](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-task.md) |
| **评测集** | `schema_version`（如 `"ATIF-v1.8"`） | 轨迹数据必需字段，标识结构规范版本；缺失或不匹配将导致轨迹导入失败 [添加轨迹评测数据](../../raw/_short/agenteval-evaluation-set-trajectory-data-7bbfb9904b121823.md) |
| **安全** | `风险等级`（高/中/低） | 风险与审计模块依据置信度与危害程度联合研判，仅开通高级防护后才产生数据 [风险与审计](../../raw/application-user-guide/agent-governance/security-guide/section-adv/audit.md) |

## 使用方式

1. **观测接入**：  
   - 在控制台进入[应用观测](https://bailian.console.aliyun.com/loop/app-observe)，点击右上角**应用观测配置**，使用主账号完成 OpenTelemetry 服务角色授权、服务开通与 LogStore 初始化；  
   - 对目标应用点击**开启观测**，输入测试问题生成 Trace 后，在详情页查看 Trace 列表、监控统计（QPM、[Token](../concepts/token.md)、耗时）、限流统计，并可导出 JSONL/EXCEL 数据。

2. **评测构建**：  
   - 创建评测集（支持空建或文件上传），选择场景（智能体/工作流/轨迹/自定义），配置字段（如 `input`、`reference_output`、`trajectory`）；  
   - **必须发布评测集后才能用于评测任务**；草稿状态不可用 [创建与管理](../../raw/_short/agenteval-evaluation-set-946c810bda606877.md)；  
   - 创建评测任务，关联已发布评测集与目标应用，配置评估器（最多 10 个）并完成变量映射；支持“不关联应用”模式用于纯人工标注。

3. **优化执行**：  
   - 进入应用优化页面，选择应用后可选三种路径：  
     - **多版本对比**：手动编辑 Prompt 组合，输入问题并对比回复差异；  
     - **调试&反馈**：发送测试问题 → 选择调试结果 → 输入具体人工反馈 → 生成优化 Prompt；  
     - **基于评测集/评测任务**：选择已发布评测集版本或已完成的评测任务（状态为“已完成”），映射字段后启动智能优化。

4. **安全管理**：  
   - 默认防护自动生效，无需操作；  
   - 高级防护需在 **Security > 高级防护 > 安全策略** 页面完成服务授权并开通，策略对账号下全部 Agent 全局生效；  
   - 风险事件与审计日志在 **Security > 高级防护 > 风险与审计** 查看，支持按风险等级、节点类型筛选。

## 限制和注意事项

- **观测限制**：  
  - 不支持 Assistant API 创建的智能体；  
  - Trace 数据同步延迟为分钟级，监控/限流指标更新频率也为分钟级；  
  - 当前无观测能力的公开 API。

- **评测限制**：  
  - 单条轨迹数据大小 ≤ 1 MB；单个评测集文件上传 ≤ 20 MB；  
  - 多模态字段校验严格：图片（JPG/JPEG/PNG，≤20 MB）、音频（MP3，≤100 MB）、视频（MP4/MOV，≤100 MB）；  
  - 评测任务创建后，应用、评测集、评估器配置均不可修改，仅支持新增人工标签。

- **优化限制**：  
  - 采纳优化结果仅更新当前编辑中的 Prompt，**不会自动发布应用**，需手动发布生效；  
  - 基于评测集优化时，若评测集包含多个冲突业务目标，可能导致生成 Prompt 约束过载，建议拆分任务。

- **安全限制**：  
  - 高级防护策略当前**仅支持风险监测与告警，不支持自动阻断**；  
  - 安全策略配置全局生效，修改前需评估对全部 Agent 的影响；  
  - CLI 命令（如 `bl agents security alerts`）查询的是账号级数据，**不区分业务空间** [使用 CLI](../../raw/application-user-guide/agent-governance/security-guide/section-gs/cli.md)。

## 来源文档

- [开始使用](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using.md)
- [Evolution](../../raw/application-user-guide/agent-governance/agenteval.md)
- [快速开始](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using/agenteval-quick-start.md)
- [概览](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using/agenteval-introduction.md)
- [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability.md)
- [告警管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-alert-management.md)
- [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)
- [应用评测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation.md)
- [评测集](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-set-index.md)
- [创建与管理](../../raw/_short/agenteval-evaluation-set-946c810bda606877.md)
- [添加轨迹评测数据](../../raw/_short/agenteval-evaluation-set-trajectory-data-7bbfb9904b121823.md)
- [添加多模态评测数据](../../raw/_short/agenteval-evaluation-set-multimodal-data-660c12b477900b3c.md)
- [应用优化](../../raw/application-user-guide/agent-governance/agenteval/agenteval-optimization.md)
- [评测任务](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)
- [评估器](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-grader.md)
- [标签管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-tags.md)
- [标签管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-tags/agenteval-tag-management.md)
- [Security](../../raw/application-user-guide/agent-governance/security-guide.md)
- [开始使用](../../raw/application-user-guide/agent-governance/security-guide/section-gs.md)
- [概述](../../raw/application-user-guide/agent-governance/security-guide/section-gs/introduction.md)
- [使用 CLI](../../raw/application-user-guide/agent-governance/security-guide/section-gs/cli.md)
- [资产盘点](../../raw/application-user-guide/agent-governance/security-guide/section-assets.md)
- [防护总览](../../raw/application-user-guide/agent-governance/security-guide/section-assets/overview.md)
- [Agent 资产](../../raw/application-user-guide/agent-governance/security-guide/section-assets/assets.md)
- [高级防护](../../raw/application-user-guide/agent-governance/security-guide/section-adv.md)
- [安全策略](../../raw/application-user-guide/agent-governance/security-guide/section-adv/policy.md)
- [风险与审计](../../raw/application-user-guide/agent-governance/security-guide/section-adv/audit.md)
- [参考](../../raw/application-user-guide/agent-governance/security-guide/section-ref.md)
- [API 参考](../../raw/application-user-guide/agent-governance/security-guide/section-ref/api.md)


