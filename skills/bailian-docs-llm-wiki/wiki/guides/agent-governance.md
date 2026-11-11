# agent governance

agent governance 是百炼平台用于对 Agent 行为进行可控干预、安全约束与持续优化的一套机制，涵盖运行时策略控制、输出合规性校验、调用链路审计及基于反馈的迭代进化能力。它不依赖模型自身推理完成治理，而是通过平台层插件化策略引擎实现解耦管控。该机制适用于所有支持 `agent` 模式调用的模型，且需在请求中显式启用相关参数。

## 支持的模型与功能

当前支持 agent governance 的模型包括：`qwen-max`, `qwen-plus`, `qwen-turbo`（v202409 及以上版本），以及 `qwen2.5-72b-instruct`（需开启 `enable_governance: true`）。核心功能包括：
- **输出内容过滤**：基于敏感词、PII、越界指令等规则实时拦截或重写响应；
- **工具调用白名单控制**：限制 Agent 可触发的工具集（如仅允许 `search` 和 `calculator`）；
- **执行深度与步数限制**：防止无限循环或过度推理；
- **进化反馈闭环**：支持将人工标注的“治理失败案例”回传至 [Evolution](../../raw/application-user-guide/agent-governance/agenteval.md) 模块用于策略迭代。

> **注意**：文档 [Agent 治理与进化](../../raw/application-user-guide/agent-governance.md) 中提及的 `qwen-14b-chat` 仍标为“实验支持”，但根据最新平台日志（2024-10-15），该模型已移出支持列表，请以控制台模型规格页为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `governance_config` | object | 否 | 治理策略配置对象，详见下表子字段 |
| `governance_config.enabled` | boolean | 否，默认 `false` | 是否启用治理引擎 |
| `governance_config.rules` | array[string] | 否 | 启用的规则 ID 列表，如 `["pii_redaction", "tool_whitelist"]` |
| `governance_config.tool_whitelist` | array[string] | 否 | 当启用 `tool_whitelist` 规则时，必须指定允许调用的工具名数组 |
| `governance_config.max_steps` | integer | 否，默认 `15` | Agent 单次会话最大执行步数（含 LLM 调用与工具执行） |

完整参数定义与默认值请参考 [Security](../../raw/application-user-guide/agent-governance/security-guide.md) 文档中的“Runtime Governance Schema”章节。

## 使用方式

1. 在 `/v1/chat/completions` 请求体中，于 `messages` 同级添加 `governance_config` 字段；
2. 确保所选模型在 [Agent 治理与进化](../../raw/application-user-guide/agent-governance.md) 文档的支持列表中；
3. 若启用 `tool_whitelist`，须确保 `tools` 数组中声明的工具 ID 与白名单完全匹配，否则工具调用将被静默拒绝（不报错，返回空 `tool_calls`）；
4. 治理结果（如拦截原因、重写后响应）通过响应头 `X-Bailian-Governance-Result` 返回 JSON 字符串，建议解析该字段用于监控与告警。

## 限制和注意事项

- 治理策略仅作用于 `agent` 模式（即 `mode: "agent"` 或 `tools` 非空），对纯 `chat` 模式无效；
- 启用治理后，平均延迟增加约 80–120ms（实测于华东1区），高并发场景需预留资源余量；
- `governance_config` 不支持嵌套策略继承，父会话配置不会自动透传至子 Agent 调用；
- 所有治理日志默认保留 7 天，如需长期审计，须主动调用 `/v1/governance/logs/export` 接口导出——该接口细节见 [Security](../../raw/application-user-guide/agent-governance/security-guide.md)。

## 来源文档

- [Agent 治理与进化](../../raw/application-user-guide/agent-governance.md)


