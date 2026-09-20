# security api guide

百炼平台的 Security API 提供模型输入/输出内容安全检测能力，支持文本、图像等多模态内容的风险识别（如涉政、暴恐、色情、违禁等）。该 API 以独立服务形式提供，需通过标准 HTTP 调用，并依赖平台统一认证机制。开发者应结合业务场景选择合适策略与阈值，避免误拦或漏检。

## 支持的模型/功能

- **基础检测模型**：`security-text-v1`（文本）、`security-image-v1`（图像），均基于百炼自研多标签分类模型，支持细粒度风险类型返回（如 `politics`, `terrorism`, `pornography`, `illegal` 等）  
- **功能覆盖**：实时同步检测、批量异步检测（仅限文本）、策略级结果聚合（如按应用 ID 统计日告警量）  
- 注意：图像检测暂不支持 GIF 动图及超过 5MB 的单文件；文本检测最大长度为 65536 字符。详细能力说明见 [API 总览与认证](../../raw/application-api-reference/security-api-guide/security-api-overview.md)

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `content` | string / base64 | 是 | 待检测内容：纯文本或图片 Base64 编码（含 `data:image/xxx;base64,` 前缀） |
| `model` | string | 是 | 固定为 `security-text-v1` 或 `security-image-v1` |
| `policy_id` | string | 否 | 指定策略 ID；若未传，则使用租户默认策略（参见 [策略与告警](../../raw/application-api-reference/security-api-guide/security-api-policies.md)） |
| `return_details` | boolean | 否 | 默认 `false`；设为 `true` 可返回各风险维度的置信度分数 |

> **注意**：原始文档中 [防护概况](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md) 提到 `content_type` 参数用于自动推断类型，但该参数已在 v2.3+ 版本中废弃，实际调用应严格通过 `model` 显式指定，否则返回 `400 Bad Request`

## 使用方式

1. **认证**：使用平台颁发的 `Authorization: Bearer <api_key>` 请求头（API Key 需在控制台「安全中心 → API 密钥」中创建）  
2. **请求示例（文本）**：
   ```bash
   curl -X POST https://dashscope.aliyuncs.com/api/v1/security/detect \
     -H "Authorization: Bearer sk-xxx" \
     -H "Content-Type: application/json" \
     -d '{
           "model": "security-text-v1",
           "content": "这个产品违反了国家法规。",
           "policy_id": "pol-abc123"
         }'
   ```
3. **响应结构**：包含 `result.safety`（布尔值，`true` 表示安全）、`result.risk_types`（风险类型数组）、`result.details`（当 `return_details=true` 时存在）  
   完整字段定义与错误码详见 [API 总览与认证](../../raw/application-api-reference/security-api-guide/security-api-overview.md)

## 限制和注意事项

- **QPS 限制**：免费版 5 QPS，企业版可配置至 100 QPS（需联系技术支持开通）  
- **配额计量**：每次调用按 1 次计费，无论 `content` 长度或是否触发风险  
- **策略生效延迟**：新创建或修改的策略最长需 2 分钟同步至检测服务，期间仍沿用旧策略  
- **图像检测兼容性**：仅支持 JPEG、PNG、WEBP 格式；不支持 ICC Profile 或旋转元数据校正，可能导致部分倾斜图像误判 —— 具体格式与性能边界请参考 [防护概况](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md)

## 来源文档

- [Security](../../raw/application-api-reference/security-api-guide.md)


