# security api guide

Security API 是百炼平台提供的安全能力调用接口，用于集成应用层防护、策略管理与实时告警功能。开发者可通过该 API 查询防护状态、配置安全策略、获取威胁事件详情，并与自有运维系统联动。所有接口均基于 RESTful 设计，需通过标准认证流程访问。

## 支持的模型/功能

Security API 当前不涉及大模型推理，而是聚焦于**应用安全管控能力**，包括：
- 防护概况查询（如 WAF、API 安全网关的运行状态与拦截统计）  
- 策略生命周期管理（创建、更新、启用/禁用自定义规则）  
- 告警事件检索与确认（支持按时间范围、风险等级、资源 ID 过滤）  
- 安全资产关联信息获取（如受保护域名、API 分组与策略绑定关系）  

> **注意**：文档中提及的“模型”仅指安全策略模板（如 `waf-rule-template-v2`），并非生成式 AI 模型；请勿与 `/v1/models` 下的 LLM 列表混淆 —— 详见 [Security API](../../raw/application-api-reference/security-api-guide.md) 的上下文说明。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `X-Api-Key` | string | 是 | 通过 [认证](../../raw/application-api-reference/security-api-guide/security-api-authentication.md) 获取的长期访问密钥 |
| `X-Timestamp` | string | 是 | 请求 UTC 时间戳（秒级，如 `1717023456`），用于防重放攻击 |
| `X-Signature` | string | 是 | 使用 `HMAC-SHA256(api_secret, timestamp + method + path + body)` 计算的签名值 |
| `page_size` | integer | 否 | 分页大小，默认 `20`，最大 `100`（见 [错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md) 中 `INVALID_PAGE_SIZE` 定义） |

## 使用方式

1. **认证准备**：在控制台「安全设置 → API 密钥」中创建密钥对，保存 `api_key` 和 `api_secret`  
2. **构造请求**：按规范生成 `X-Signature`，例如 Python 示例：
   ```python
   import hmac, hashlib, time
   ts = str(int(time.time()))
   msg = f"{ts}GET/v1/security/policies"
   sig = hmac.new(api_secret.encode(), msg.encode(), hashlib.sha256).hexdigest()
   ```
3. **调用示例**（查询高危告警）：
   ```bash
   curl -X GET "https://dashscope.aliyuncs.com/v1/security/alerts?severity=high&start_time=1717020000" \
     -H "X-Api-Key: ak-xxx" \
     -H "X-Timestamp: $ts" \
     -H "X-Signature: $sig"
   ```

## 限制和注意事项

- 单账户默认 QPS 限流为 10，突发峰值不超过 30；超出将返回 `429 Too Many Requests`（参考 [错误码](../../raw/application-api-reference/security-api-guide/security-api-errors.md)）  
- 策略更新操作（`PUT /v1/security/policies/{id}`）为最终一致性，变更生效延迟 ≤ 3 秒  
- 所有时间参数使用 Unix 时间戳（秒），**不支持毫秒或 ISO 8601 字符串格式** —— 此要求与部分旧版 SDK 文档冲突，请以 [防护概况](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md) 中的字段定义为准  
- 告警事件保留周期为 90 天，过期数据不可检索  

> **注意**：`/v1/security/policies` 接口的 `enabled` 字段在 [策略与告警](../../raw/application-api-reference/security-api-guide/security-api-policies.md) 中定义为布尔值，但实际响应中可能返回字符串 `"true"` 或 `"false"`；建议客户端做兼容性解析。

## 来源文档

- [Security API](../../raw/application-api-reference/security-api-guide.md)


