# security api guide

Security API 是百炼平台提供的安全能力调用接口，用于集成应用层防护、策略管理与实时告警等核心安全功能。开发者可通过该 API 实现自动化策略配置、防护状态查询及安全事件响应。所有接口均需通过标准认证流程，并遵循统一的错误码规范。

## 支持的模型/功能

Security API 当前支持以下核心安全能力：
- 应用防护概况查询（如 WAF、Bot 管理、API 安全防护状态）  
- 安全策略的增删改查（含规则组、自定义规则、速率限制策略）  
- 告警配置与历史告警检索（支持按时间范围、策略 ID、事件类型过滤）  
- 防护日志导出（需配合 [防护概况](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md) 中定义的 log_type 枚举值使用）  

> **注意**：文档中提及的“AI 模型安全检测”功能（见 [概览](../../raw/application-api-reference/security-api-guide/security-api-overview.md) 第 2.3 节）尚未在 v1.2 API 中开放，实际调用将返回 `404 Not Found`；请以 [错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md) 文档中 `ERR_UNSUPPORTED_FEATURE` 的说明为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `x-api-key` | string | 是 | 从控制台「API 密钥管理」获取的认证密钥，用于 [认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md) |
| `x-region-id` | string | 否 | 指定资源所在地域（如 `cn-beijing`），默认为账户默认地域 |
| `policy_id` | string | 条件必填 | 执行策略操作时必需，格式为 `pol-xxxxxx`，可在 [策略与告警](../../raw/application-api-reference/security-api-guide/security-api-policies.md) 中查得 |

## 使用方式

1. **认证**：在 HTTP Header 中携带 `x-api-key`，不支持 query 或 body 传参方式；  
2. **请求示例（cURL）**：
   ```bash
   curl -X GET "https://api.bailian.aliyuncs.com/v1/security/policies" \
     -H "x-api-key: sk-xxx" \
     -H "x-region-id: cn-shanghai"
   ```
3. **响应解析**：成功响应均为 JSON 格式，含 `code=200` 和 `data` 字段；失败时严格遵循 [错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md) 定义，建议对 `code` 和 `message` 双字段做容错处理。

## 限制和注意事项

- 单账号 QPS 限制为 50，突发流量触发限流时返回 `429 Too Many Requests`（详见 [错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md)）；  
- 策略更新操作为最终一致性，变更后最多 30 秒内生效，不可依赖立即生效语义；  
- 所有时间戳参数必须为 ISO 8601 格式（如 `2024-01-01T00:00:00Z`），不接受 Unix 时间戳或本地时区格式。

## 来源文档

- [Security API](../../raw/application-api-reference/security-api-guide.md)


