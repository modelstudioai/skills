# security api guide

百炼平台的 Security API 提供模型调用过程中的内容安全防护能力，支持在请求/响应阶段实时检测和拦截风险内容（如违法、违规、敏感信息等）。开发者可通过统一接口集成策略配置、告警订阅与防护状态查询等功能。所有接口均需通过平台标准认证机制访问。

## 支持的模型/功能

Security API 本身不直接提供大模型推理服务，而是作为**防护中间件**，与百炼支持的全部文本生成类模型（如 Qwen 系列、Qwen2、Qwen3）协同工作。其核心功能包括：
- 请求输入内容安全检测（含文本、图像 base64 编码）
- 响应输出内容安全过滤（支持阻断或脱敏返回）
- 多维度防护策略管理（按应用、模型、场景粒度配置）
- 实时告警事件推送（通过 Webhook 或轮询方式获取）

> **注意**：部分旧版文档中提及“仅支持 Qwen1.5”，该描述已过时；当前 [API 总览与认证](../../raw/application-api-reference/security-api-guide/security-api-overview.md) 明确说明所有启用安全防护的模型均受支持。

## 关键参数

调用 Security API 时，以下参数为必需或强推荐：

| 参数名 | 类型 | 是否必需 | 说明 |
|--------|------|----------|------|
| `app_id` | string | 是 | 百炼控制台创建的应用唯一标识，用于策略绑定与配额统计 |
| `content` | string | 是（输入检测） | 待检测的原始文本或 base64 编码图像字符串 |
| `scene` | string | 否（默认 `"general"`） | 防护场景标识，如 `"chat"`、`"search"`、`"moderation"`，影响策略匹配优先级 |
| `enable_filter` | boolean | 否（默认 `false`） | 设为 `true` 时对响应内容执行过滤（如替换敏感词），详见 [防护概况](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md) |
| `policy_id` | string | 否 | 指定生效策略 ID；若未指定，则使用应用默认策略 |

## 使用方式

1. **前置准备**：在百炼控制台「安全中心」完成策略配置，并确保应用已开启「内容安全防护」开关；
2. **集成调用**：在模型请求前，先调用 `/v1/security/detect` 接口检测用户输入；若需响应过滤，需在模型请求头中添加 `X-Enable-Security-Filter: true`；
3. **结果处理**：根据响应中的 `action` 字段（`"allow"` / `"block"` / `"review"`）决定是否继续调用模型或返回提示；
4. **告警订阅**：通过 [策略与告警](../../raw/application-api-reference/security-api-guide/security-api-policies.md) 中定义的 Webhook 地址接收异步风险事件。

## 限制和注意事项

- 单次 `content` 长度上限为 10,000 字符（文本）或 5 MB（图像 base64）；
- 输入检测接口 QPS 限流为 100，超出将返回 `429 Too Many Requests`；
- 启用 `enable_filter` 时，响应体中 `output` 字段可能被重写，原始模型输出需从 `original_output` 字段提取；
- 图像检测仅支持 JPEG/PNG 格式，且必须为合法 base64 编码（无换行、无前缀）；
- 所有策略配置变更需 30 秒内生效，但缓存可能导致首次检测延迟，建议在上线前充分测试。

> **注意**：[防护概况](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md) 中提到的“支持自定义正则策略”功能暂未开放公测，实际可用策略类型请以控制台界面及 [策略与告警](../../raw/application-api-reference/security-api-guide/security-api-policies.md) 文档为准。

## 来源文档

- [Security](../../raw/application-api-reference/security-api-guide.md)


