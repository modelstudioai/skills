# security api guide

百炼平台的 Security API 提供模型输入/输出内容安全检测能力，支持实时识别敏感信息、违法不良信息及潜在风险内容。开发者可通过统一 HTTP 接口调用，集成到应用的数据流中实现自动化内容审核。该能力基于阿里云内容安全服务底层能力，与百炼模型推理链路深度协同。

## 支持的模型/功能

Security API 不依赖具体大模型实例，而是作为独立的安全检测服务提供以下核心能力：
- 文本内容安全检测（含涉政、暴恐、色情、违禁品、辱骂等 10+ 类风险）
- 敏感词与自定义关键词匹配（支持正则与模糊匹配）
- 图片 OCR 后文本联合分析（需传入 base64 编码图片）
- 防护策略执行结果反馈（如拦截、脱敏、告警）

> **注意**：文档 [API 总览与认证](../../raw/application-api-reference/security-api-guide/security-api-overview.md) 中提及的 `model: security-2023` 已下线，当前无需指定 model 参数；实际调用时仅需使用 `/v1/security/scan` 端点，详见 [防护概况](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md)。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `content` | string | 是 | 待检测的 UTF-8 编码文本；若检测图片，需先 OCR 提取文本并传入 |
| `scene` | string | 否 | 检测场景，可选 `comment`、`search`、`profile` 等，影响策略权重，默认为 `general` |
| `risk_level` | string | 否 | 风险阈值，`low`/`medium`/`high`，默认 `medium`；参考 [策略与告警](../../raw/application-api-reference/security-api-guide/security-api-policies.md) 中的分级定义 |

## 使用方式

1. 使用百炼平台颁发的 `AccessKeyId` 和 `AccessKeySecret` 签名请求（推荐使用 SDK 自动签名）  
2. 发送 POST 请求至 `https://dashscope.aliyuncs.com/api/v1/security/scan`  
3. 请求体为 JSON，示例：
```json
{
  "content": "这个产品支持破解微信密码。",
  "scene": "comment",
  "risk_level": "high"
}
```
4. 响应包含 `result.suggestion`（`pass`/`review`/`block`）、`result.risk_items` 及各风险项置信度

## 限制和注意事项

- 单次请求 `content` 最长 10,000 字符；超长内容需分段调用并自行聚合结果  
- QPS 限制为 50（按 AccessKey 维度），突发流量建议启用异步回调模式（见 [API 总览与认证](../../raw/application-api-reference/security-api-guide/security-api-overview.md)）  
- 不支持直接检测音频、视频或原始二进制图片——必须先通过 OCR 或 ASR 提取文本再调用  
- 返回的 `risk_items` 中 `category` 字段值以 [防护概况](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md) 定义为准，旧版文档中部分 category 别名（如 `"politics_v2"`）已统一为 `"politics"`

## 来源文档

- [Security](../../raw/application-api-reference/security-api-guide.md)


