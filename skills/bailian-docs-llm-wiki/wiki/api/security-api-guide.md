# security api guide

百炼平台的 Security API 提供模型输入/输出内容安全检测能力，支持文本、图片等多模态内容的风险识别（如涉政、暴恐、色情、违禁等）。该 API 以独立服务形式提供，需通过标准 HTTP 接口调用，并依赖平台统一认证机制。开发者可将其集成至应用链路中，实现前置过滤或后置审计。

## 支持的模型与功能

Security API 当前不依赖大语言模型推理引擎，而是基于专用规则引擎与轻量级多模态分类模型提供检测服务。支持以下核心能力：
- 文本内容安全检测（UTF-8 编码，最大长度 65536 字符）
- 图片内容安全检测（JPEG/PNG 格式，最大尺寸 4096×4096 像素，文件大小 ≤10 MB）
- 同步返回细粒度风险标签（如 `politics`, `terrorism`, `porn`）及置信度分数  
- 批量检测（单次请求最多 10 条文本或 5 张图片）

> **注意**：文档 [API 总览与认证](../../raw/application-api-reference/security-api-guide/security-api-overview.md) 中提及“支持音频内容检测”，但该能力尚未上线，当前版本实际不支持音频；请以 [防护概况](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md) 中的功能列表为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `input` | object | 是 | 输入对象，含 `text`（字符串）或 `image_url` / `image_base64`（二选一） |
| `categories` | array of string | 否 | 指定检测风险类型，例如 `["politics", "porn"]`；留空则启用全部默认类别 |
| `return_categories` | boolean | 否 | 是否返回各子类别的详细置信度，默认 `false` |
| `timeout` | integer | 否 | 超时时间（秒），范围 1–30，默认 15 |

注意：`image_base64` 值需为标准 Base64 编码（无换行、无前缀），且必须使用 `data:image/<type>;base64,` 前缀的格式——此要求在 [策略与告警](../../raw/application-api-reference/security-api-guide/security-api-policies.md) 中有明确说明。

## 使用方式

1. **认证**：使用平台颁发的 `Authorization: Bearer <api_key>` 请求头（API Key 通过控制台「密钥管理」获取）  
2. **请求地址**：`POST https://dashscope.aliyuncs.com/api/v1/security/detect`  
3. **示例请求体（文本）**：
   ```json
   {
     "input": {"text": "这是一段待检测的文本"},
     "categories": ["politics", "terrorism"]
   }
   ```
4. **响应结构**：返回 `result` 对象，含 `suggestion`（`pass`/`review`/`block`）、`risk_level`（`low`/`medium`/`high`）及 `labels` 数组  

完整调用流程与错误码说明详见 [API 总览与认证](../../raw/application-api-reference/security-api-guide/security-api-overview.md)。

## 限制和注意事项

- QPS 限制：默认 10 次/秒（可提交工单申请提升）  
- 每日调用量上限：免费版 10,000 次，商用版按配额计费  
- 图片检测不支持 GIF 动图及 SVG 矢量图，仅支持静态 JPEG/PNG  
- 若传入 `image_url`，服务端将发起 HTTPS GET 请求拉取资源，要求目标 URL 可公开访问且响应头含 `Content-Type`  
- 检测结果不保证 100% 准确，高风险场景建议结合人工复核；具体误报/漏报率指标参见 [防护概况](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md)  

> **注意**：[策略与告警](../../raw/application-api-reference/security-api-guide/security-api-policies.md) 中提到“支持自定义策略 ID 透传”，但当前 API 接口尚未开放 `policy_id` 字段，该功能计划于 v2.3 版本上线，现阶段忽略该参数。

## 来源文档

- [Security](../../raw/application-api-reference/security-api-guide.md)


