# agent governance

agent governance 是百炼平台面向 AI Agent 全生命周期提供的治理能力集合，涵盖可观测性、自动化评测、Prompt 智能优化及内生安全防护四大核心维度。它不依赖特定开发框架，基于 OpenTelemetry GenAI 标准实现即插即用，支持从开发调试、线上运行到效果迭代的闭环管理，帮助开发者系统性提升 Agent 的可靠性、合规性与业务效果。

## 支持的模型/功能

- **观测能力**：支持 Agent 1.0、Agent 2.0 和工作流应用的全链路追踪（Trace），完整记录 Prompt 解析、模型调用（含 TTFT、Token 消耗）、工具执行、记忆读写等环节；暂不支持通过 Assistant API 创建的智能体 [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)。
- **评测能力**：支持三类评测对象：
  - **文本输出**：准确性、简洁性、合规性等维度；
  - **轨迹（Trajectory）**：评估执行过程逻辑性、工具调用成功率、观察信息增益等，需评测集包含 `trajectory` 类型字段 [添加轨迹评测数据](../../raw/_short/agenteval-evaluation-set-trajectory-data-7bbfb9904b121823.md)；
  - **多模态内容**：支持图文音视频混排输入/输出的美学质量、指令遵循、画质、文字渲染等评估，需评测集字段类型为 `多模态` [添加多模态评测数据](../../raw/_short/agenteval-evaluation-set-multimodal-data-660c12b477900b3c.md)。
- **优化能力**：支持基于调试结果、评测任务结果或线上 Trace 数据驱动的 Prompt 多版本对比与智能优化，生成结果可人工审查后采纳至编辑区（不自动发布）。
- **安全能力**：提供默认生效的内生防护（如内容安全 I/O 检测、知识库预扫描）和可选开通的高级防护（如提示词攻击检测、RAG 数据投毒识别），覆盖 Flow Agent、Managed Agent、RAG、Memory、Store 全模块 [概述](../../raw/application-user-guide/agent-governance/security-guide/section-gs/introduction.md)。

> **注意**：文档中“应用观测目前暂无 API”与“Security 模块提供 7 个接口”存在功能边界差异——前者指观测数据导出无专用 API，后者指安全策略与审计数据可通过 API 查询；二者不矛盾，但需明确：观测数据仅支持控制台导出（JSONL/EXCEL），而安全事件、资产概览等支持程序化访问。

## 关键参数

| 功能模块 | 参数/配置项 | 说明 |
|---------|------------|------|
| **观测** | `Request ID` / `Trace ID` / `Span ID` | 用于在 Trace 列表中精确检索单次调用链；Trace 数据同步延迟为分钟级 [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md) |
| **评测** | 评测集字段映射、评估器变量映射 | 必须严格匹配数据类型：轨迹变量 → `trajectory` 列，多模态变量 → `多模态` 列；类型不匹配将导致配置无法保存 [评测任务](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-task.md) |
| **告警** | 持续时间（分钟）、告警检查周期（秒）、统计周期（分钟） | 预置模板如“QPM 限流大于 6000”对应指标 `QPM`，阈值需结合业务负载设定 [告警管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-alert-management.md) |
| **安全策略** | 策略全局生效、服务授权必要 | 所有安全策略配置对账号下全部 Agent 生效，不区分业务空间；高级防护需完成服务授权后开通 [安全策略](../../raw/application-user-guide/agent-governance/security-guide/section-adv/policy.md) |

## 使用方式

1. **观测接入**：  
   - 主账号进入[应用观测配置](https://bailian.console.aliyun.com/loop/app-observe)，授权 OpenTelemetry 角色、开通服务、初始化 LogStore；  
   - 在应用列表点击**开启观测**，输入测试问题触发 Trace 上报；  
   - 通过 Trace 列表、监控统计（调用数/Tokens/模型分析）、限流统计（QPM/限流次数）进行排查。

2. **评测执行**：  
   - 创建评测集（选择场景：智能体/工作流/轨迹/多模态），**必须发布后才能使用**；  
   - 基于预置模板创建评估器（如“轨迹准确性”“图片指令遵循”），或自定义 LLM/Code 评估器；  
   - 创建评测任务，关联已发布评测集版本与目标应用，完成评估器变量映射（如 `query`→评测集`input`，`trajectory`→评测集`trajectory`列）；  
   - 查看数据明细（含轨迹预览）与指标统计（得分分布、回归对比）。

3. **Prompt 优化**：  
   - 进入应用优化页，选择“调试&反馈优化”或“基于评测集优化”；  
   - 若选调试路径：发送测试问题 → 选择代表性调试结果 → 输入具体人工反馈（如“回答遗漏价格条款，需在末尾强制追加‘价格以官网为准’”）→ 生成并对比 Prompt → 采纳至编辑区；  
   - 若选评测路径：直接选择已发布的优质评测集版本，系统基于样本与参考输出生成优化建议。

4. **安全防护**：  
   - 默认防护自动生效（无需操作），覆盖输入输出内容安全、知识库预扫描等；  
   - 高级防护需在 **Security > 高级防护 > 安全策略** 页面完成服务授权后开通，默认启用前 6 项策略（如提示词攻击、敏感数据外泄），`内容安全`需手动开启；  
   - 风险事件统一在 **Security > 风险与审计** 查看，支持按风险等级、节点类型筛选。

## 限制和注意事项

- **观测限制**：仅支持已发布且归属当前业务空间的应用；子账号需主账号预先配置 OpenTelemetry 权限；Trace 数据最长保留 30 天，导出格式仅支持 JSONL 或 EXCEL。
- **评测限制**：单条轨迹数据大小 ≤ 1 MB；多模态文件单个限制：图片 ≤ 20 MB（JPG/PNG）、音频 ≤ 100 MB（MP3）、视频 ≤ 100 MB（MP4/MOV）；评测任务最多添加 10 个评估器，创建后不可修改应用或评测集配置。
- **优化限制**：采纳优化结果仅更新当前编辑中的 Prompt，**不会自动发布应用**；多版本对比最多支持 1 个基准组 + 2 个对照组。
- **安全限制**：高级防护策略全局生效，修改前需评估对全部 Agent 的影响；风险与审计页面展示账号下所有 Agent 数据，**不区分业务空间**；CLI 命令 `bl agents security overview` 固定查询最近 24 小时数据，不支持自定义时间范围 [使用 CLI](../../raw/application-user-guide/agent-governance/security-guide/section-gs/cli.md)。
- **通用限制**：所有评测任务调用大模型产生的 Token 按实际消耗计费；评测集草稿状态不可用于评测任务，必须发布 [创建与管理](../../raw/_short/agenteval-evaluation-set-946c810bda606877.md)。

## 来源文档

- [开始使用](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using.md)
- [概览](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using/agenteval-introduction.md)
- [快速开始](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using/agenteval-quick-start.md)
- [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)
- [告警管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-alert-management.md)
- [应用评测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation.md)
- [评测集](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-set-index.md)
- [Evolution](../../raw/application-user-guide/agent-governance/agenteval.md)
- [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability.md)
- [添加轨迹评测数据](../../raw/_short/agenteval-evaluation-set-trajectory-data-7bbfb9904b121823.md)
- [添加多模态评测数据](../../raw/_short/agenteval-evaluation-set-multimodal-data-660c12b477900b3c.md)
- [评估器](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-grader.md)
- [评测任务](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)
- [应用优化](../../raw/application-user-guide/agent-governance/agenteval/agenteval-optimization.md)
- [标签管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-tags.md)
- [标签管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-tags/agenteval-tag-management.md)
- [Security](../../raw/application-user-guide/agent-governance/security-guide.md)
- [开始使用](../../raw/application-user-guide/agent-governance/security-guide/section-gs.md)
- [创建与管理](../../raw/_short/agenteval-evaluation-set-946c810bda606877.md)
- [概述](../../raw/application-user-guide/agent-governance/security-guide/section-gs/introduction.md)
- [使用 CLI](../../raw/application-user-guide/agent-governance/security-guide/section-gs/cli.md)
- [资产盘点](../../raw/application-user-guide/agent-governance/security-guide/section-assets.md)
- [Agent 资产](../../raw/application-user-guide/agent-governance/security-guide/section-assets/assets.md)
- [防护总览](../../raw/application-user-guide/agent-governance/security-guide/section-assets/overview.md)
- [高级防护](../../raw/application-user-guide/agent-governance/security-guide/section-adv.md)
- [安全策略](../../raw/application-user-guide/agent-governance/security-guide/section-adv/policy.md)
- [风险与审计](../../raw/application-user-guide/agent-governance/security-guide/section-adv/audit.md)
- [参考](../../raw/application-user-guide/agent-governance/security-guide/section-ref.md)
- [API 参考](../../raw/application-user-guide/agent-governance/security-guide/section-ref/api.md)


