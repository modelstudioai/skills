# security api guide

Security API 提供对百炼平台安全防护能力的程序化访问，支持策略配置、告警管理、防护状态查询等核心安全运维场景。该 API 面向企业级开发者设计，需通过标准 OAuth 2.0 认证接入。所有接口均遵循 RESTful 规范，返回结构化 JSON 响应，并统一使用 HTTP 状态码标识调用结果。

## 支持的模型/功能

Security API 当前覆盖以下关键安全能力模块：
- **防护概况查询**：获取租户级实时防护统计（如拦截请求数、攻击类型分布）  
- **策略管理**：创建、更新、启用/禁用 WAF 规则、速率限制策略及自定义规则集  
- **告警管理**：检索、确认、关闭安全告警，支持按时间范围与严重等级过滤  
- **日志导出**（Beta）：拉取近 7 天的原始安全事件日志（需额外开通权限）  

> **注意**：日志导出功能在 [防护概况](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md) 中未明确说明支持周期，但 [策略与告警](../../raw/application-api-reference/security-api-guide/security-api-policies.md) 文档补充了“仅限 7 天内日志”的限制，以该文档为准。

## 关键参数

所有请求必须携带以下认证与上下文参数：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `Authorization` | string | 是 | Bearer `<access_token>`，由 [认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md) 流程颁发 |
| `X-Region` | string | 是 | 指定资源所在地域（如 `cn-beijing`），不传将默认使用账户主地域 |
| `X-Tenant-ID` | string | 是 | 租户唯一标识，用于多租户隔离，不可省略 |
| `page` / `page_size` | integer | 否 | 分页参数，`page_size` 最大值为 100（见 [错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md) 中 `INVALID_PAGE_SIZE` 定义） |

## 使用方式

1. **获取 [Token](../concepts/token.md)**：调用 `/v1/oauth/token` 接口，使用 client_id + client_secret 申请短期 access_token（有效期 1 小时）  
2. **构造请求**：以 `https://api.bailian.aliyun.com/v1/security/` 为根路径，例如查询防护概况：  
   ```http
   GET /v1/security/protection/overview HTTP/1.1
   Authorization: Bearer abc123...
   X-Region: cn-shanghai
   X-Tenant-ID: t-456789
   ```
3. **处理响应**：检查 HTTP 状态码（200 表示成功，4xx/5xx 需参考 [错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md) 解析具体原因）

## 限制和注意事项

- 单租户 QPS 限制为 50，突发流量触发限流时返回 `429 Too Many Requests`  
- 所有策略变更操作（如创建规则）均为异步生效，需轮询 `/v1/security/policies/{id}/status` 确认最终状态  
- 不支持跨地域策略同步；`X-Region` 必须与目标资源实际部署地域严格一致  
- 告警确认后不可撤销，且确认操作本身不触发回调通知（该行为与 [策略与告警](../../raw/application-api-reference/security-api-guide/security-api-policies.md) 文档描述一致，无需额外兼容）

## 来源文档

- [Security API](../../raw/application-api-reference/security-api-guide.md)


