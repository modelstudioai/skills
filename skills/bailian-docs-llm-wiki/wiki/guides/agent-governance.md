# agent governance

agent governance 是百炼平台用于管控 Agent 行为、保障执行安全与结果可控的核心机制，涵盖权限约束、调用链路审计、工具调用白名单、响应合规性校验等能力。它不依赖模型自身推理实现治理，而是通过平台层拦截、重写与验证完成策略落地。该机制适用于所有通过 `agent.run()` 或 `AgentExecutor` 启动的 Agent 实例。

## 支持的模型与功能

- **支持模型**：Qwen-Max、Qwen-Plus、Qwen-Turbo（v202408 及以上版本）；Qwen-VL 等多模态模型暂不支持工具调用治理，仅支持基础响应过滤。
- **核心功能**：
  - 工具调用白名单控制（按 Agent 实例配置）
  - 敏感 API 参数脱敏与拦截（如 `os.system`、`requests.post` 直接构造）
  - 响应内容合规性扫描（基于预置规则集，支持自定义正则策略）
  - 执行链路日志归因（关联 trace_id 与用户 identity_id）

> **注意**：文档 [Agent 治理与进化](../../raw/application-user-guide/agent-governance.md) 中提及的 “Evolution” 模块当前已下线，其 A/B 测试能力由 [agenteval.md](../../raw/application-user-guide/agent-governance/agenteval.md) 中描述的 `eval_mode: 'governance_v2'` 替代，旧参数 `evolution_enabled: true` 已废弃。

## 关键参数

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `governance_enabled` | bool | `true` | 全局开关，设为 `false` 将跳过全部治理逻辑（**仅调试用，生产环境禁用**） |
| `tool_whitelist` | list[str] | `[]` | 允许调用的工具 ID 列表，空列表表示禁止所有工具调用；ID 格式需与 `tool_registry.get_tool(id)` 一致 |
| `response_filter_rules` | list[dict] | `[{"type": "keyword", "pattern": ["密码", "token"]}]` | 响应过滤规则，详见 [security-guide.md](../../raw/application-user-guide/agent-governance/security-guide.md) |

## 使用方式

1. 在初始化 Agent 时传入治理配置：
   ```python
   agent = Agent(
       model="qwen-max",
       tools=[search_tool, db_query_tool],
       governance_config={
           "governance_enabled": True,
           "tool_whitelist": ["search_tool"],
           "response_filter_rules": [{"type": "regex", "pattern": r"API_KEY=\w+"}]
       }
   )
   ```
2. 运行时可通过 `agent.run(input, governance_override={...})` 动态覆盖部分参数（仅限 `tool_whitelist` 和 `response_filter_rules`）。

## 限制和注意事项

- 单次请求最大治理规则数：50 条；超出将触发 `GovernanceConfigError` 异常。
- 不支持对流式响应（`stream=True`）进行实时内容过滤，仅对最终聚合响应生效。
- 工具白名单仅校验 `tool.id`，不校验工具内部实现；若工具封装了危险操作（如 `subprocess.run`），仍需在工具代码中自行加固。
- 所有治理行为均记录于 `x-bailian-gov-trace` header 中，可用于审计溯源。详细日志字段定义见 [security-guide.md](../../raw/application-user-guide/agent-governance/security-guide.md)。

## 来源文档

- [Agent 治理与进化](../../raw/application-user-guide/agent-governance.md)


