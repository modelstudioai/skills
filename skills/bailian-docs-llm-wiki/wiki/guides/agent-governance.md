# agent governance

agent governance 是百炼平台用于管控 Agent 行为、保障执行安全与结果可控的核心机制，涵盖权限控制、调用链路审计、输出内容过滤及运行时策略干预等功能。它不依赖模型自身能力，而通过平台层拦截与重写实现治理，适用于所有接入百炼 Agent 框架的模型实例。该机制与 [Agent 治理与进化](../../raw/application-user-guide/agent-governance.md) 文档中定义的 Evolution 和 Security 两大支柱紧密协同。

## 支持的模型/功能

- **模型兼容性**：支持所有已接入百炼 Agent Runtime 的模型（包括 Qwen 系列、Qwen2.5、Qwen3 及第三方模型封装实例），但仅在启用 `agent_mode: true` 且配置 `governance_policy` 时生效。
- **核心功能**：
  - 输入指令清洗（如移除越权工具调用请求）
  - 工具调用白名单/黑名单控制
  - 输出敏感信息脱敏（如手机号、身份证号正则匹配掩码）
  - 执行超时与重试次数硬限制
  - 调用链路日志注入（含 policy 匹配结果与干预动作）

> **注意**：部分旧版文档（如 [Evolution](../../raw/application-user-guide/agent-governance/agenteval.md)）提及“模型内嵌治理插件”，该能力已于 v2.3.0 下线，当前全部治理逻辑统一由平台 Runtime 层实现，详见 [Agent 治理与进化](../../raw/application-user-guide/agent-governance.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `governance_policy` | string | 是 | 策略 ID，需提前在控制台创建；支持 `default`, `finance-strict`, `gov-public` 等预置策略 |
| `enable_governance` | boolean | 否（默认 `true`） | 显式关闭治理时设为 `false`，调试阶段可用 |
| `governance_timeout_ms` | integer | 否（默认 `15000`） | 单次治理检查最大耗时，超时则跳过并记录告警 |

## 使用方式

1. 在 Agent 配置 YAML 中声明策略：
   ```yaml
   agent:
     mode: "tool"
     governance_policy: "finance-strict"
   ```
2. 或通过 API 请求头传递（优先级高于配置）：
   ```http
   X-Bailian-Governance-Policy: gov-public
   ```
3. 策略效果实时生效，无需重启服务；变更策略后，新会话立即应用，存量会话维持原策略直至结束。

## 限制和注意事项

- 每个 Agent 实例最多绑定 1 个 `governance_policy`，不支持运行时动态切换策略（需重建实例）。
- 工具调用拦截发生在 `tool_call` 解析后、执行前，因此无法阻止模型生成非法 tool name（需配合 LLM 输出 schema 校验）。
- 敏感词脱敏基于正则匹配，不支持语义级识别；如需更细粒度控制，请参考 [Security](../../raw/application-user-guide/agent-governance/security-guide.md) 中的自定义规则扩展方式。

## 来源文档

- [Agent 治理与进化](../../raw/application-user-guide/agent-governance.md)


