# agent governance

agent governance 是百炼平台用于管控 Agent 行为、保障执行安全与结果可控的核心机制，涵盖权限控制、调用链路审计、输出内容过滤及运行时策略干预等功能。它不依赖模型自身能力，而是通过平台层的统一拦截与决策实现治理，适用于所有接入百炼 Agent 框架的模型实例。该机制与 [Agent 治理与进化](../../raw/application-user-guide/agent-governance.md) 文档中定义的演进路径和安全边界强绑定。

## 支持的模型/功能

- **模型兼容性**：所有支持 `agent_mode: true` 的百炼原生模型（如 qwen-plus、qwen-max）均默认启用基础治理能力；第三方模型需通过 `model_type: "custom"` 显式注册后，方可接入治理管道。
- **核心功能**：
  - 输入/输出内容合规性扫描（基于关键词、正则、LLM 分类器三级检测）
  - 工具调用白名单控制（限制可执行的 function call 列表）
  - 执行深度与步数限制（防止无限循环或过度推理）
  - 敏感操作实时阻断（如 `shell_exec`、`http_post_to_internal_ip` 等高危动作）

> **注意**：[Agent 治理与进化](../../raw/application-user-guide/agent-governance.md) 中提及的 “自动进化策略” 尚未在 v3.2.0 生产环境开放，当前仅支持手动配置的静态规则集，相关能力请以 [Evolution](../../raw/application-user-guide/agent-governance/agenteval.md) 的最新说明为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `governance_policy_id` | string | 否 | 引用预置策略 ID（如 `"default-safe"`、`"finance-restricted"`），留空则使用租户默认策略 |
| `max_tool_calls` | integer | 否 | 单次会话最大工具调用次数，默认 `10`，设为 `0` 表示禁用所有工具 |
| `output_filter_level` | string | 否 | 输出过滤强度：`"none"` / `"basic"` / `"strict"`，默认 `"basic"` |

## 使用方式

1. 在创建 Agent 实例时，于 `config` 字段中传入治理参数：
   ```json
   {
     "model": "qwen-max",
     "agent_mode": true,
     "governance_policy_id": "finance-restricted",
     "max_tool_calls": 5
   }
   ```
2. 运行时可通过 `X-Bailian-Governance-Override` HTTP Header 动态覆盖部分策略（仅限调试场景，生产环境禁用）。
3. 策略详情与日志可在控制台「Agent → Governance → Audit Logs」中查看，原始行为记录与拦截原因均保留完整上下文。

## 限制和注意事项

- 治理规则在请求入口处生效，**无法覆盖模型内部 self-refine 或 memory-based reasoning 过程**；
- 启用 `output_filter_level: "strict"` 时，可能因误判导致合法长文本被截断，建议结合 [Security](../../raw/application-user-guide/agent-governance/security-guide.md) 中的 false-positive 评估流程校准；
- 单次请求的治理耗时计入整体 latency，复杂策略（如启用 LLM 分类器）平均增加 120–300ms 延迟；
- 不支持对 streaming 响应流中的中间 token 实时过滤，仅对最终 `finish_reason == "stop"` 的完整响应体生效。

## 来源文档

- [Agent 治理与进化](../../raw/application-user-guide/agent-governance.md)


