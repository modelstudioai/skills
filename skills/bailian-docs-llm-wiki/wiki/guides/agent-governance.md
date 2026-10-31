# agent governance

agent governance 是百炼平台用于管控 Agent 行为、保障执行安全与结果可控的核心机制，涵盖权限约束、调用链路审计、输出内容过滤及进化评估等能力。它并非独立模型，而是嵌入在 Agent 生命周期各环节的治理策略集合，需通过 SDK 或 API 显式启用对应治理模块。具体能力边界和配置方式依赖所选底层模型与运行时环境。

## 支持的模型/功能

- 当前仅 `qwen-max` 和 `qwen-plus` 支持完整的 agent governance 功能栈（含执行沙箱、工具调用白名单、响应重写）；`qwen-turbo` 仅支持基础输出过滤（如敏感词拦截），不支持工具调用审计。
- 治理能力按模块解耦：`security` 模块提供输入/输出内容安全检测，`evolution` 模块支持基于 [Evolution](../../raw/application-user-guide/agent-governance/agenteval.md) 的多轮行为评估与策略迭代。
- 所有治理模块均需配合 `agent_runtime_v2` 运行时启用，`v1` 运行时不兼容（详见 [Security](../../raw/application-user-guide/agent-governance/security-guide.md) 中的兼容性说明）。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `governance_config` | object | 否 | 治理策略配置对象，结构见下表 |
| `governance_config.security` | object | 否 | 安全策略，支持 `enable_input_filter`, `enable_output_filter`, `blocklist`（字符串数组）等字段；默认全关闭 |
| `governance_config.evolution` | object | 否 | 进化评估策略，需指定 `eval_template_id`（引用 [Evolution](../../raw/application-user-guide/agent-governance/agenteval.md) 中预置模板）及 `eval_interval`（单位：轮次） |

> **注意**：原始文档中 `governance_config.evolution.eval_template_id` 被描述为“可选字符串”，但实测若启用 `evolution` 模块却未提供该 ID，将返回 `400 Bad Request`。请以 [Evolution](../../raw/application-user-guide/agent-governance/agenteval.md) 中的模板注册状态为准，避免空值传参。

## 使用方式

1. 在创建 Agent 实例时，于 `create_agent` 请求体中传入 `governance_config`；
2. 若需动态调整策略，调用 `update_agent` 接口并传入更新后的 `governance_config`（仅支持覆盖式更新，不支持局部 patch）；
3. 治理日志默认不返回至客户端，需单独调用 `/v1/agents/{agent_id}/governance/logs` 查询（需 `read:governance_logs` 权限）。

## 限制和注意事项

- 单次请求中 `governance_config` 总大小不得超过 8KB，超限将被拒绝；
- `security` 模块启用后，平均延迟增加 120–350ms（取决于 blocklist 规则数量），建议生产环境对 `blocklist` 做精简合并；
- `evolution` 模块仅在 `stream=false` 模式下生效；流式响应（`stream=true`）中不触发评估逻辑；
- 当前不支持跨 Agent 共享 `governance_config` 配置，每个 Agent 实例需独立配置。  
> **注意**：[Security](../../raw/application-user-guide/agent-governance/security-guide.md) 文档中提及“支持通过组织级策略自动继承治理配置”，但该功能尚未上线（截至 v2024.07.15），实际调用仍需显式传参。

## 来源文档

- [Agent 治理与进化](../../raw/application-user-guide/agent-governance.md)


