# security api guide

Security API 是百炼平台提供的安全能力调用接口，用于集成应用层防护、策略管理与实时告警等核心安全功能。开发者可通过该 API 实现自动化策略配置、防护状态查询及安全事件响应。所有请求需通过标准认证流程，并遵循统一的错误码规范与速率限制。

## 支持的模型/功能

Security API 当前支持以下核心能力：
- 应用防护概况查询（如 WAF、Bot 管理、API 安全防护的启用状态与统计）
- 安全策略管理（含规则组、自定义规则、IP 黑白名单、速率限制策略）
- 告警配置与历史事件检索（支持按时间范围、严重等级、触发策略过滤）

> **注意**：文档 [防护概况](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md) 中描述的 `GET /v1/protection/summary` 接口返回字段与 [策略与告警](../../raw/application-api-reference/security-api-guide/security-api-policies.md) 中的 `policy_id` 关联逻辑存在不一致——前者使用 `policy_ref` 字段引用策略，后者示例中直接使用 `id`；请以 [策略与告警](../../raw/application-api-reference/security-api-guide/security-api-policies.md) 的 `id` 字段为准，`policy_ref` 已废弃。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `x-api-key` | string | 是 | 从控制台获取的 API 密钥，用于 [认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md) |
| `x-region-id` | string | 否 | 指定资源所在地域（如 `cn-beijing`），默认为调用方主地域 |
| `limit` / `offset` | integer | 否 | 分页参数，`limit` 最大值为 100（见 [错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md) 中 `INVALID_PARAMETER` 说明） |

## 使用方式

1. **认证**：在 HTTP Header 中携带 `x-api-key`，无需 OAuth 或 JWT 流程（详见 [认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md)）  
2. **调用示例**（查询当前地域防护概况）：  
   ```bash
   curl -H "x-api-key: sk-xxx" \
        "https://api.bailian.aliyuncs.com/v1/protection/summary"
   ```  
3. **错误处理**：所有失败响应均返回标准 JSON 格式错误体，含 `code` 与 `message` 字段，具体含义参考 [错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md)

## 限制和注意事项

- 单个 API Key 默认 QPS 限流为 50，突发流量可短暂突破至 100，超限返回 `429 Too Many Requests`  
- 策略更新操作（如 `PUT /policies/{id}`）为最终一致性，变更生效延迟 ≤ 3 秒  
- 所有时间戳参数必须为 ISO 8601 格式（`YYYY-MM-DDTHH:mm:ssZ`），不支持毫秒或本地时区偏移（此要求在 [概览](../../raw/application-api-reference/security-api-guide/security-api-overview.md) 中未明确，但实际接口校验严格）  
- 删除策略前必须确保无关联的防护实例，否则返回 `POLICY_IN_USE` 错误（见 [策略与告警](../../raw/application-api-reference/security-api-guide/security-api-policies.md)）

## 来源文档

- [Security API](../../raw/application-api-reference/security-api-guide.md)


