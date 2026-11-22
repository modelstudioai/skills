# security api guide

Security API 是百炼平台提供的安全能力调用接口，用于集成应用层防护、策略管理与实时告警等核心安全功能。开发者可通过该 API 实现自动化策略配置、防护状态查询及安全事件响应。所有接口均需通过标准认证流程，并遵循统一的错误码规范。

## 支持的模型/功能

Security API 当前支持以下核心安全能力：
- 应用防护概况查询（如 WAF、Bot 管理、API 安全防护状态）  
- 安全策略的增删改查（含规则组、自定义规则、速率限制策略）  
- 告警配置与历史告警检索（支持按时间范围、策略 ID、事件类型过滤）  
- 防护日志导出（需配合 [防护概况](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md) 中定义的 log_type 枚举值使用）  

> **注意**：文档中提及的“AI 模型安全检测”功能（见 [概览](../../raw/application-api-reference/security-api-guide/security-api-overview.md) 第 2.3 节）尚未在当前 API 版本中开放，实际调用将返回 `404 Not Found`；请以 [错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md) 文档中 `ERR_UNSUPPORTED_FEATURE` 的说明为准。

## 关键参数

所有 Security API 请求必须包含以下参数：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `X-Api-Key` | string | 是 | 从控制台「API 密钥管理」获取的长期凭证，替代 Bearer [Token](../concepts/token.md) 方案（参见 [认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md)） |
| `X-Request-ID` | string | 否 | 推荐提供，用于问题排查与审计追踪 |
| `Content-Type` | string | 是 | 固定为 `application/json` |

策略类接口（如 `/policies`）额外要求 `x-region-id` 头部，取值须与资源所属地域一致，否则返回 `400 Bad Request`。

## 使用方式

1. **认证**：在请求 Header 中携带 `X-Api-Key`，无需额外 token 刷新逻辑；密钥权限由控制台 IAM 策略控制。  
2. **调用示例（创建策略）**：
   ```bash
   curl -X POST https://api.bailian.aliyuncs.com/v1/security/policies \
     -H "X-Api-Key: sk-xxx" \
     -H "x-region-id: cn-beijing" \
     -H "Content-Type: application/json" \
     -d '{
           "name": "block-malicious-ip",
           "type": "ip_block",
           "enabled": true,
           "conditions": [{"field": "client_ip", "op": "in", "value": ["192.0.2.1"]}]
         }'
   ```
3. **响应处理**：成功返回 `201 Created` 及完整策略对象；失败时严格遵循 [错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md) 文档定义的结构，含 `code`、`message` 和可选 `request_id`。

## 限制和注意事项

- 单账户默认 QPS 限流为 10，突发峰值不超过 30；超出将返回 `429 Too Many Requests`（详见 [错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md)）。  
- 策略名称（`name` 字段）长度限制为 1–64 字符，仅允许字母、数字、下划线和短横线；违反将触发 `400 Bad Request`。  
- 所有时间戳参数（如 `start_time` / `end_time`）必须为 RFC 3339 格式（例如 `2024-05-20T08:00:00Z`），不支持 Unix timestamp 或本地时区格式——该约束在 [策略与告警](../../raw/application-api-reference/security-api-guide/security-api-policies.md) 文档中明确，但部分旧版 SDK 示例误用毫秒时间戳，务必校验。

## 来源文档

- [Security API](../../raw/application-api-reference/security-api-guide.md)


