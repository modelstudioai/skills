# agent governance

agent governance 是百炼平台面向 AI Agent 全生命周期提供的治理能力集合，涵盖可观测性（Observability）、可评测性（Evaluation）与可优化性（Optimization）三大支柱。它通过 OpenTelemetry 标准接入、结构化轨迹（Trajectory）建模与多维评估器体系，帮助开发者在开发、上线与运维阶段系统性地定位问题、量化质量、驱动迭代。核心能力不依赖特定框架，支持 Agent 1.0/2.0、工作流应用，但暂不支持 Assistant API 创建的智能体。

## 支持的模型/功能

- **可观测性**：支持全链路 Trace 上报与可视化，覆盖 Prompt 解析、大模型调用（含 TTFT、[Token](../concepts/token.md) 消耗）、工具执行（MCP/Skill）、向量检索、记忆读写等节点；提供分钟级监控统计（QPM、错误率、耗时、[Token](../concepts/token.md) 分布）与限流指标，并支持基于 Trace 数据一键回流至评测集 [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)。
- **可评测性**：支持端到端输出评测与轨迹（Trajectory）评测双模式。预置 LLM/Code 类评估器（如轨迹准确性、工具调用成功率、回答忠实度等），支持自定义 LLM Prompt 或 Python 脚本评估逻辑；评测集支持 `input`/`reference_output`/`trajectory` 多类型字段，其中 `trajectory` 字段需为符合 ATIF-v1.8 规范的 JSON 结构 [添加轨迹评测数据](../../raw/_short/agenteval-evaluation-set-trajectory-data-7bbfb9904b121823.md)。
- **可优化性**：提供 Prompt 多版本对比调试、基于调试反馈的智能优化、以及基于评测集/评测任务结果的定向优化三条路径；所有优化均生成可对比的 Prompt 版本，采纳后仅更新草稿态 Prompt，不自动发布应用 [应用优化](../../raw/application-user-guide/agent-governance/agenteval/agenteval-optimization.md)。
- **安全治理**：提供默认生效的原生防护（内容安全 I/O、RAG 文件预扫描、凭证隔离等）与按需开通的高级防护（提示词攻击检测、敏感数据外泄检测等），策略配置对账号下全部 Agent 全局生效，不区分业务空间 [概述](../../raw/application-user-guide/agent-governance/security-guide/section-gs/introduction.md)。

> **注意**：文档中关于“应用观测目前暂无 API”的表述（见 [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)）与 Security 模块明确提供 `/api/v1/agentstudio/security` 系列 API 的事实存在矛盾。实际可观测数据可通过 Security API 中的 `/agent_logs` 等接口间接获取风险与审计日志，但原生 Trace 数据暂无独立 REST API，该限制仍有效。

## 关键参数

- **Trace 字段映射**：将观测 Trace 导入评测集时，必须保证 Trace 字段与评测集列的数据类型严格一致（如 `trajectory` 字段只能映射到数据类型为“轨迹”的评测集列），否则导入失败 [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)。
- **评估器变量映射**：创建评测任务时，评估器所有变量必须完成映射，且映射源（评测集字段或应用输出）的数据类型须与变量声明类型一致（例如轨迹类型变量必须映射到轨迹列），否则无法保存配置 [评测任务](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)。
- **安全策略作用域**：所有安全策略（如提示词攻击、敏感数据外泄）配置后对此账号下全部 Agent 全局生效，不区分业务空间，修改前需评估影响范围 [安全策略](../../raw/application-user-guide/agent-governance/security-guide/section-adv/policy.md)。

## 使用方式

1. **接入观测**：主账号进入[应用观测配置](https://bailian.console.aliyun.com/loop/app-observe)，授权 OpenTelemetry 服务角色、开通服务并初始化 LogStore；在应用列表点击“开启观测”，输入测试问题触发 Trace 上报。
2. **创建评测**：先创建并**发布**评测集（草稿不可用），选择场景（智能体/工作流/轨迹）配置表结构；再创建评估器（预置或自定义），最后在评测任务中关联已发布评测集版本、目标应用及评估器并配置字段映射。
3. **发起优化**：在“应用优化”页面选择目标应用，可任选以下路径：
   - *多版本对比*：设置基准组与对照组 Prompt，输入问题并对比回复差异；
   - *调试反馈*：发送测试问题，选择调试结果并填写具体人工反馈后启动优化；
   - *评测集/评测任务*：选择已发布的评测集版本或已完成的评测任务，勾选低分/失败样本，配置字段映射后启动。
4. **配置安全告警**：通过 CLI 命令 `bl agents security alerts --risk-level high` 查询高风险事件，或在控制台 Security > 高级防护 > 风险与审计 页面筛选处理。

## 限制和注意事项

- **应用支持范围**：应用观测与评测仅支持 Agent 1.0、Agent 2.0 和工作流应用，**明确不支持通过 Assistant API 创建的智能体** [快速开始](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using/agenteval-quick-start.md)。
- **评测集版本管理**：评测集最多保存 10 个历史版本，超出后自动覆盖旧版本；草稿状态的评测集不可用于评测任务，必须发布后才能选择 [创建与管理](../../raw/_short/agenteval-evaluation-set-946c810bda606877.md)。
- **轨迹数据约束**：单条轨迹 JSON 大小不能超过 1 MB，且必须为合法 JSON 对象；评测集若含 `trajectory` 列，其数据类型必须设为“轨迹”，否则无法被轨迹评估器正确识别 [添加轨迹评测数据](../../raw/_short/agenteval-evaluation-set-trajectory-data-7bbfb9904b121823.md)。
- **优化与发布解耦**：所有优化路径（对比、调试、评测）的“采纳”操作仅更新当前应用的草稿态 Prompt，**不会自动发布应用**；发布需手动进入应用编辑页完成 [应用优化](../../raw/application-user-guide/agent-governance/agenteval/agenteval-optimization.md)。
- **安全策略开通状态**：高级防护（如提示词攻击检测）需完成服务授权并开通，当前处于限时免费阶段；而默认防护（如内容安全 I/O 拦截）随 Agent 使用对应模块（如 RAG、Memory）自动生效，无需额外操作 [概述](../../raw/application-user-guide/agent-governance/security-guide/section-gs/introduction.md)。

## 来源文档

- [开始使用](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using.md)
- [概览](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using/agenteval-introduction.md)
- [快速开始](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using/agenteval-quick-start.md)
- [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability.md)
- [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)
- [告警管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-alert-management.md)
- [应用评测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation.md)
- [评测集](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-set-index.md)
- [创建与管理](../../raw/_short/agenteval-evaluation-set-946c810bda606877.md)
- [添加轨迹评测数据](../../raw/_short/agenteval-evaluation-set-trajectory-data-7bbfb9904b121823.md)
- [评测任务](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)
- [评估器](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-grader.md)
- [标签管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-tags.md)
- [应用优化](../../raw/application-user-guide/agent-governance/agenteval/agenteval-optimization.md)
- [Evolution](../../raw/application-user-guide/agent-governance/agenteval.md)
- [标签管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-tags/agenteval-tag-management.md)
- [Security](../../raw/application-user-guide/agent-governance/security-guide.md)
- [开始使用](../../raw/application-user-guide/agent-governance/security-guide/section-gs.md)
- [使用 CLI](../../raw/application-user-guide/agent-governance/security-guide/section-gs/cli.md)
- [概述](../../raw/application-user-guide/agent-governance/security-guide/section-gs/introduction.md)
- [资产盘点](../../raw/application-user-guide/agent-governance/security-guide/section-assets.md)
- [防护总览](../../raw/application-user-guide/agent-governance/security-guide/section-assets/overview.md)
- [Agent 资产](../../raw/application-user-guide/agent-governance/security-guide/section-assets/assets.md)
- [高级防护](../../raw/application-user-guide/agent-governance/security-guide/section-adv.md)
- [安全策略](../../raw/application-user-guide/agent-governance/security-guide/section-adv/policy.md)
- [风险与审计](../../raw/application-user-guide/agent-governance/security-guide/section-adv/audit.md)
- [参考](../../raw/application-user-guide/agent-governance/security-guide/section-ref.md)
- [API 参考](../../raw/application-user-guide/agent-governance/security-guide/section-ref/api.md)


