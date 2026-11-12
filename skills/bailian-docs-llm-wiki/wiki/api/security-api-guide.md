# security api guide

Security API 是百炼平台提供的安全能力调用接口，用于集成应用层防护、策略管理与实时告警等核心安全功能。开发者可通过该 API 实现自动化策略配置、防护状态查询及安全事件响应。所有接口均需通过标准认证流程，并遵循统一的错误码规范。

## 支持的模型/功能

Security API 当前支持以下核心安全能力：
- 应用防护概况查询（如 WAF、Bot 管理、API 安全防护的启用状态与统计）
- 安全策略管理（含规则组、自定义规则、速率限制策略的增删改查）
- 告警配置与历史事件检索（支持按时间范围、风险等级、触发策略过滤）

> **注意**：文档中提及的“AI 模型安全检测”功能（见 [Security API](../../raw/application-api-reference/security-api-guide.md)）尚未在当前版本 API 中开放，该描述与 [防护概况](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md) 中的功能列表存在不一致，请以后者为准。

## 关键参数

所有 Security API 请求必须包含以下通用参数：
- `X-Api-Key`（必选，通过控制台获取的访问密钥）
- `X-Timestamp`（必选，ISO 8601 格式 UTC 时间戳，有效期 5 分钟）
- `X-Signature`（必选，基于 `method + path + timestamp + body` 的 HMAC-SHA256 签名）

策略类接口额外要求 `policy_id` 或 `rule_id`；告警类接口支持 `start_time` / `end_time`（RFC 3339 格式）和 `severity`（`low`/`medium`/`high`/`critical`）。

## 使用方式

1. 首先完成认证：参考 [认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md) 文档生成合法签名；
2. 调用 `GET /v1/security/protection/overview` 获取当前防护状态；
3. 如需配置策略，使用 `POST /v1/security/policies` 提交 JSON 格式策略定义（结构详见 [策略与告警](../../raw/application-api-reference/security-api-guide/security-api-policies.md)）；
4. 所有响应均遵循统一格式：`{ "code": 200, "data": {...}, "message": "success" }`，错误详情请查阅 [错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md)。

## 限制和注意事项

- 单个 API Key 每分钟限流 600 次，突发请求将返回 `429 Too Many Requests`；
- 策略更新操作为最终一致性，变更生效延迟不超过 30 秒；
- `body` 中禁止提交 base64 编码的二进制内容（如证书文件），仅支持纯文本 JSON 结构；
- 所有时间参数必须为 UTC，本地时区转换需由客户端完成。

## 来源文档

- [Security API](../../raw/application-api-reference/security-api-guide.md)


