# agent governance

agent governance 是百炼平台面向 AI Agent 全生命周期提供的统一治理能力集合，涵盖可观测性（Observability）、可评测性（Evaluation）与可优化性（Optimization）三大核心支柱，并通过内生安全防护（Security）保障运行合规。它不依赖特定框架，基于 OpenTelemetry GenAI 标准实现即插即用，支持从开发调试、线上监控、质量量化到 Prompt 持续迭代的闭环管理。

## 支持的模型/功能

- **Agent 类型支持**：  
  - 智能体应用（Agent 1.0 和 Agent 2.0）  
  - 工作流应用（Flow Agent）  
  > **注意**：应用观测与评测暂不支持通过 Assistant API 创建的智能体，详见 [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)。

- **核心功能模块**：  
  - **观测（Observability）**：全链路 Trace 可视化（Prompt 解析、模型调用、工具执行、记忆读写），支持延时、[Token](../concepts/token.md)、QPM、首 [Token](../concepts/token.md) 耗时等分钟级监控与限流统计；支持告警规则配置与历史回溯。  
  - **评测（Evaluation）**：支持多维自动化评测，包括文本输出（准确性、简洁性、合规性）、执行轨迹（步骤逻辑、工具调用成功率、回答忠实度）、多模态内容（图片美学/指令遵循/幻觉检测）；提供预置 LLM/Code 评估器与自定义能力。  
  - **优化（Optimization）**：支持基于调试结果、评测任务低分样本或线上 Trace 数据的 Prompt 智能优化；提供多版本对比调试与一键采纳机制。  
  - **安全（Security）**：默认启用原生防护（内容安全 I/O、RAG 知识库扫描、Memory 内容检测等），高级防护（如提示词攻击检测、敏感数据外泄识别）需开通后按策略启用，且对账号下全部 Agent 全局生效 [安全策略](../../raw/application-user-guide/agent-governance/security-guide/section-adv/policy.md)。

- **数据类型支持**：  
  - 轨迹（Trajectory）：结构化 JSON，含 `steps`、`extra`、`final_metrics` 字段，用于过程可靠性评估 [添加轨迹评测数据](../../raw/_short/agenteval-evaluation-set-trajectory-data-7bbfb9904b121823.md)。  
  - 多模态（Multimodal）：`Array<Object>` 格式，支持 `text`/`image_url`/`audio_url`/`video_url` 混排，用于图文音视频理解与生成评测。

## 关键参数

| 参数类别 | 参数名 | 说明 | 约束 |
|----------|--------|------|------|
| **观测配置** | `OpenTelemetry 服务角色` | 必须授权以采集 Trace 数据 | 主账号操作；子账号需主账号预先配置权限 |
| **评测集** | `字段数据类型` | 映射必须严格一致（如 `trajectory` 列 → `trajectory` 变量） | 类型不匹配将导致导入/评测失败 |
| **评估器映射** | `变量与数据源映射` | 所有评估器变量必须完成映射（支持评测集字段 / 应用输出） | 未映射无法保存评测任务配置 |
| **安全策略** | `全局生效标识` | 安全策略配置后对账号下所有 Agent 生效，不区分业务空间 | 修改前需评估跨空间影响 [安全策略](../../raw/application-user-guide/agent-governance/security-guide/section-adv/policy.md) |
| **标签类型** | `分类/布尔/数字/文本` | 用于人工标注，支持筛选与指标统计 | 分类标签最多 20 个选项；文本标签最多 10000 字符 |

## 使用方式

1. **接入观测**：  
   - 进入 [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)，点击目标应用「开启观测」；  
   - 首次使用需完成「应用观测配置」（授权 OTel 角色、开通服务、初始化 LogStore）；  
   - Trace 数据自动同步（分钟级），支持按 `Request ID`/`Trace ID` 搜索、导出（JSONL/EXCEL）及添加至评测集。

2. **创建评测**：  
   - 先创建并**发布**评测集（草稿不可用）；场景可选「智能体」「工作流」「轨迹」「多模态」；  
   - 选择预置或自定义评估器，严格按要求映射变量（如轨迹评估器必须映射到 `trajectory` 类型列）；  
   - 发起评测任务后，可在「数据明细」查看每条样本的自动评分与轨迹详情，在「指标统计」分析分布与回归对比。

3. **启动优化**：  
   - 在「应用优化」页面选择目标应用；  
   - 三种路径可选：  
     - *调试反馈*：发送测试问题 → 选择调试结果 → 输入具体改进方向 → 生成并采纳 Prompt；  
     - *基于评测集*：选择已发布评测集版本 → 映射 `应用输入`/`应用输出`/`轨迹` 字段 → 启动优化；  
     - *基于评测任务*：选择「已完成」任务 → 筛选低分/失败样本 → 启动定向优化。

4. **配置安全**：  
   - 默认防护自动生效（无需操作）；  
   - 高级防护需进入 [安全策略](../../raw/application-user-guide/agent-governance/security-guide/section-adv/policy.md) 页面开通（限时免费），默认启用前 6 项策略，`内容安全` 需手动开启；  
   - 风险事件与审计日志统一在「风险与审计」页面查看（按账号聚合，不区分业务空间）。

## 限制和注意事项

- **功能限制**：  
  - 应用观测暂无开放 API，仅支持控制台操作；  
  - 评测任务创建后，其关联的「应用」与「评测集」配置不可修改，需新建任务调整；  
  - 单个评测任务最多支持 10 个评估器；单个评测集最多支持 50 个字段映射；  
  - 轨迹数据单条大小 ≤ 1 MB，多模态单文件限制：图片 ≤ 20 MB、音频/视频 ≤ 100 MB。

- **权限与范围**：  
  - 子账号需主账号授予 `AliyunBailianFullAccess` 或最小必要权限才能开通观测服务；  
  - 安全策略配置为**账号级全局生效**，修改将影响所有业务空间下的 Agent，务必提前评估 [安全策略](../../raw/application-user-guide/agent-governance/security-guide/section-adv/policy.md)。

- **数据一致性注意**：  
  - 评测集字段类型与评估器变量类型、Trace 字段与评测集映射字段类型必须完全一致，否则导入/评测失败；  
  - 「不关联应用」的评测任务仅支持纯人工标注，不触发任何模型调用；  
  - 评测任务中「采纳」优化结果仅更新当前编辑中的 Prompt，**不会自动发布应用**，发布需单独操作。

## 来源文档

- [Evolution](../../raw/application-user-guide/agent-governance/agenteval.md)
- [概览](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using/agenteval-introduction.md)
- [开始使用](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using.md)
- [快速开始](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using/agenteval-quick-start.md)
- [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability.md)
- [告警管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-alert-management.md)
- [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)
- [应用评测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation.md)
- [创建与管理](../../raw/_short/agenteval-evaluation-set-946c810bda606877.md)
- [评测集](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-set-index.md)
- [添加轨迹评测数据](../../raw/_short/agenteval-evaluation-set-trajectory-data-7bbfb9904b121823.md)
- [添加多模态评测数据](../../raw/_short/agenteval-evaluation-set-multimodal-data-660c12b477900b3c.md)
- [评估器](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-grader.md)
- [评测任务](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)
- [应用优化](../../raw/application-user-guide/agent-governance/agenteval/agenteval-optimization.md)
- [标签管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-tags.md)
- [标签管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-tags/agenteval-tag-management.md)
- [Security](../../raw/application-user-guide/agent-governance/security-guide.md)
- [开始使用](../../raw/application-user-guide/agent-governance/security-guide/section-gs.md)
- [使用 CLI](../../raw/application-user-guide/agent-governance/security-guide/section-gs/cli.md)
- [概述](../../raw/application-user-guide/agent-governance/security-guide/section-gs/introduction.md)
- [资产盘点](../../raw/application-user-guide/agent-governance/security-guide/section-assets.md)
- [防护总览](../../raw/application-user-guide/agent-governance/security-guide/section-assets/overview.md)
- [高级防护](../../raw/application-user-guide/agent-governance/security-guide/section-adv.md)
- [Agent 资产](../../raw/application-user-guide/agent-governance/security-guide/section-assets/assets.md)
- [安全策略](../../raw/application-user-guide/agent-governance/security-guide/section-adv/policy.md)
- [风险与审计](../../raw/application-user-guide/agent-governance/security-guide/section-adv/audit.md)
- [参考](../../raw/application-user-guide/agent-governance/security-guide/section-ref.md)
- [API 参考](../../raw/application-user-guide/agent-governance/security-guide/section-ref/api.md)


