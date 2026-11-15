# agent governance

agent governance 是百炼平台用于管控 Agent 行为、保障执行安全与结果可控的核心机制，涵盖权限约束、调用链路审计、输出内容过滤及进化评估等能力。它并非独立模型，而是嵌入在 Agent 生命周期各环节的策略层，需配合特定模型与参数启用。开发者可通过 API 请求头、系统提示词或平台控制台配置治理规则。

## 支持的模型与功能

- **模型支持**：当前仅 `qwen-max` 和 `qwen-plus` 支持完整的 agent governance 功能（含工具调用拦截、敏感操作二次确认、响应重写）；`qwen-turbo` 仅支持基础输出过滤，不支持工具级治理。  
- **核心功能**：  
  - 工具调用白名单/黑名单控制（需在 [Agent 治理与进化](../../raw/application-user-guide/agent-governance.md) 中配置）  
  - 响应内容实时脱敏（如手机号、身份证号自动掩码）  
  - 执行路径审计日志生成（日志字段详见 [Evolution](../../raw/application-user-guide/agent-governance/agenteval.md)）  
  - 风险动作熔断（如高频外部 API 调用触发限流）

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `governance_policy` | string | 否 | 策略标识符，如 `"strict"`（启用全部治理）、`"audit_only"`（仅记录不拦截）、`"off"`（默认，禁用）；详见 [Security](../../raw/application-user-guide/agent-governance/security-guide.md) |
| `allowed_tools` | array of string | 否 | 显式声明允许调用的工具 ID 列表，优先级高于全局白名单 |
| `sensitive_patterns` | object | 否 | 自定义正则模式，用于扩展脱敏规则，格式：`{"phone": "1[3-9]\\d{9}"}` |

> **注意**：`governance_policy=strict` 在 `qwen-turbo` 上实际降级为 `audit_only`，该行为与 [Agent 治理与进化](../../raw/application-user-guide/agent-governance.md) 文档中“所有模型均支持 strict 模式”的描述矛盾，请以实际 API 响应为准。

## 使用方式

1. **API 调用**：在请求体 `parameters` 中传入治理参数，例如：
   ```json
   {
     "model": "qwen-max",
     "parameters": {
       "governance_policy": "strict",
       "allowed_tools": ["search_web", "get_weather"]
     }
   }
   ```
2. **控制台配置**：在 Agent 编辑页 → “安全与治理” 标签页中设置默认策略，该配置将覆盖 API 未显式指定的参数。  
3. **系统提示词注入**：对不支持参数传递的旧版 SDK，可在 `system_prompt` 开头添加 `<!-- GOVERNANCE: strict -->` 指令（兼容性见 [Security](../../raw/application-user-guide/agent-governance/security-guide.md)）。

## 限制和注意事项

- 单次请求最多配置 50 个 `allowed_tools`，超出部分被静默忽略；  
- 敏感模式匹配仅作用于最终响应文本，**不扫描工具调用参数或中间思考过程**；  
- 审计日志保留 30 天，需通过 `/v1/agent/logs` 接口主动拉取，非实时推送；  
- 启用 `governance_policy=strict` 时，平均延迟增加 120–350ms（实测于华东1区），高并发场景建议压测验证。

## 来源文档

- [Agent 治理与进化](../../raw/application-user-guide/agent-governance.md)


