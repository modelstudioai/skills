# security api guide

Security API 是百炼平台提供的安全能力调用接口，用于集成应用层防护、策略管理与实时告警功能。开发者可通过该 API 查询防护状态、配置安全策略、获取威胁事件详情，并与自有运维系统联动。所有接口均需通过标准认证流程访问，详见 [Security API](../../raw/application-api-reference/security-api-guide.md)。

## 支持的模型/功能

- **防护能力**：支持 Web 应用防火墙（WAF）、API 流量异常检测、SQL 注入/XSS 实时拦截等基础防护；具体能力覆盖范围请参考 [防护概况](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md)。  
- **策略管理**：提供策略创建、更新、启用/禁用及批量导入导出能力，支持按域名、路径、HTTP 方法等维度精细化配置。  
- **告警与事件**：支持查询近 30 天的安全事件（如攻击尝试、规则命中），并可订阅实时告警推送（需额外配置 Webhook）。

## 关键参数

- `X-Api-Key`（必填）：用于身份鉴权，需在控制台「API 密钥管理」中生成，有效期默认 90 天。  
- `X-Request-ID`（推荐）：客户端生成的唯一 UUID，便于问题追踪与日志关联。  
- `scope`（部分接口必填）：指定操作范围，取值为 `app:<app_id>` 或 `domain:<domain_name>`，不传则默认作用于当前授权应用。  
- `start_time` / `end_time`（时间范围类接口）：ISO 8601 格式（如 `2024-01-01T00:00:00Z`），最大跨度为 7 天 —— 此限制与 [错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md) 中 `ERR_TIME_RANGE_EXCEEDED` 的说明一致。

## 使用方式

1. **认证**：所有请求必须携带 `X-Api-Key` 请求头，且需通过 HTTPS 发起；不支持 Basic Auth 或 Cookie 认证。  
2. **请求示例（查询防护状态）**：
   ```bash
   curl -X GET "https://api.bailian.ai/v1/security/protection/status" \
     -H "X-Api-Key: sk-xxx" \
     -H "scope: app:app-12345"
   ```
3. **响应处理**：成功响应均为 `200 OK`，结构统一为 `{ "code": 0, "data": {...}, "message": "" }`；失败响应遵循 [错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md) 定义。

## 限制和注意事项

- 单个 API Key 每分钟限流 600 次（QPM），超出将返回 `429 Too Many Requests`；高频轮询类场景建议使用长轮询或事件订阅替代。  
- 策略生效存在最多 30 秒延迟，修改后不可立即验证效果；若文档 [策略与告警](../../raw/application-api-reference/security-api-guide/security-api-policies.md) 中提及“秒级生效”，请以本条为准。  
> **注意**：原始文档中 [认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md) 提到支持 `Authorization: Bearer <token>` 方式，但该方式已于 v2.3.0 版本下线，当前仅接受 `X-Api-Key`；请勿沿用旧文档示例。  
- 所有时间参数均以 UTC 为准，客户端需自行完成本地时区转换。

## 来源文档

- [Security API](../../raw/application-api-reference/security-api-guide.md)


