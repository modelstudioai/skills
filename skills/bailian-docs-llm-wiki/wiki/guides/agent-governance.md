# agent governance

agent governance 是百炼平台用于管控 Agent 行为、保障执行安全与结果可控的核心机制，涵盖权限约束、调用链路审计、输出内容过滤及策略驱动的动态干预能力。它不依赖模型自身推理实现治理，而是通过平台层拦截、重写与熔断等手段，在 Agent 执行生命周期各阶段施加确定性控制。该机制适用于所有接入百炼 Agent 框架的模型实例，但具体能力边界受模型类型与部署模式影响。

## 支持的模型/功能

- **支持模型**：Qwen-Max、Qwen-Plus、Qwen-Turbo 及所有已接入百炼 Agent Runtime 的自定义模型（含 vLLM 部署的私有模型）；不支持直接对非 Agent 封装的 raw model endpoint 启用完整治理链路。  
- **核心功能**：  
  - 输入/输出内容安全过滤（基于 [Security](../../raw/application-user-guide/agent-governance/security-guide.md) 规则集）  
  - 工具调用白名单与参数校验（参考 [Evolution](../../raw/application-user-guide/agent-governance/agenteval.md) 中的 tool schema binding 说明）  
  - 执行超时熔断与 step-level 回滚  
  - 审计日志自动注入至 `x-bailian-trace-id` 关联链路  

> **注意**：文档 [Agent 治理与进化](../../raw/application-user-guide/agent-governance.md) 中提及的“实时策略热更新”功能在 v3.2.0+ 版本中已移除，当前仅支持重启 runtime 生效；请以 [Evolution](../../raw/application-user-guide/agent-governance/agenteval.md) 的版本兼容性表格为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `governance.enabled` | boolean | 否 | 默认 `true`；设为 `false` 将完全跳过治理中间件（调试时可用） |
| `governance.ruleset_id` | string | 否 | 指向预置规则集 ID（如 `"sec-2024-q3"`），未指定则使用租户默认规则集 |
| `governance.max_steps` | integer | 否 | 单次 Agent 调用最大执行步数，默认 `15`，超过即终止并返回 `TOO_MANY_STEPS` 错误 |

## 使用方式

1. 在创建 Agent 时，于 `runtime_config` 字段中声明治理配置：  
   ```json
   {
     "runtime_config": {
       "governance": {
         "enabled": true,
         "ruleset_id": "sec-2024-q3",
         "max_steps": 12
       }
     }
   }
   ```
2. 运行时可通过 `X-Bailian-Governance-Override` HTTP Header 动态覆盖单次请求的 `max_steps`（仅限调试环境，生产禁用）。  
3. 规则集管理与审计日志查询，请参阅 [Security](../../raw/application-user-guide/agent-governance/security-guide.md) 文档中的控制台操作指引。

## 限制和注意事项

- 治理逻辑运行于 Agent Runtime 层，**无法干预模型内部 token 级生成过程**，仅作用于输入 [prompt](prompt.md)、工具调用请求、工具返回结果、最终 output 四个关键切面。  
- 启用 `governance.enabled` 后，平均延迟增加约 8–12ms（实测于 Qwen-Plus + 3 工具调用场景），高并发下需预留相应资源配额。  
- 自定义工具若未正确声明 `parameters` schema，可能导致参数校验失效——此行为已在 [Evolution](../../raw/application-user-guide/agent-governance/agenteval.md) 的 schema 兼容性章节中明确标注。

## 来源文档

- [Agent 治理与进化](../../raw/application-user-guide/agent-governance.md)


