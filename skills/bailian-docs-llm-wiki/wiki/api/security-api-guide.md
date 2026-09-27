# security api guide

百炼平台的 Security API 提供模型输入/输出内容安全检测能力，支持文本、图像等多模态内容的风险识别（如涉黄、暴恐、违禁等）。开发者可通过统一 HTTP 接口调用，集成到应用链路中实现实时防护。所有请求需携带有效 API Key 并遵循鉴权规范。

## 支持的模型/功能

- **文本安全检测**：支持对用户输入、模型生成文本进行多维度风险分类（L1–L4 级别），覆盖色情、暴力、政治敏感、违法违禁等 12+ 类风险类型  
- **图像安全检测**：支持 JPG/PNG 格式图片的 OCR 文本提取 + 视觉内容联合分析（需启用 `enable_ocr: true`）  
- **批量异步检测**：通过 `/v1/security/async/submit` 提交任务，后续轮询 `/v1/security/async/result` 获取结果（详见 [API 总览与认证](../../raw/application-api-reference/security-api-guide/security-api-overview.md)）  

> **注意**：原始文档中 [防护概况](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md) 提到“支持音频文件检测”，但当前 v1.3.0 API 实际未开放该能力，该描述已过时，请以 [API 总览与认证](../../raw/application-api-reference/security-api-guide/security-api-overview.md) 中的接口列表为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `content` | string | 是（文本） | 待检测文本内容，UTF-8 编码，最大 65536 字符 |
| `image_url` | string | 是（图像） | 图片公网可访问 URL（HTTPS），支持防盗链白名单配置 |
| `scene` | string | 否 | 检测场景，如 `"chat"`（对话）、`"search"`（搜索）、`"generation"`（生成），影响策略权重，默认 `"general"` |
| `enable_ocr` | boolean | 否 | 图像检测时是否启用 OCR 文本识别，默认 `false`；启用后将增加约 300ms 延迟 |

## 使用方式

1. **同步调用（推荐用于低延迟场景）**  
   ```bash
   curl -X POST "https://dashscope.aliyuncs.com/api/v1/security/text" \
     -H "Authorization: Bearer $API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"content":"测试文本","scene":"chat"}'
   ```

2. **异步调用（适用于大图或高并发批量检测）**  
   先提交任务获取 `task_id`，再按 [策略与告警](../../raw/application-api-reference/security-api-guide/security-api-policies.md) 中定义的轮询机制查询结果，超时时间默认 30 分钟。

## 限制和注意事项

- 单次文本检测上限：65536 字符；单张图像分辨率上限：4096×4096 像素，文件大小 ≤ 10MB  
- 同步接口 QPS 限流为 50，异步接口提交 QPS 限流为 10（企业版可申请提升）  
- 返回字段 `risk_level` 为整数（0=安全，1=低危，2=中危，3=高危），**不等于**原始文档 [防护概况](../../raw/application-api-reference/security-api-guide/security-api-protection-overview.md) 中描述的字符串枚举值，实际响应以接口返回 JSON 为准  
- 所有检测结果仅保留 7 天，审计日志需自行落库留存

## 来源文档

- [Security](../../raw/application-api-reference/security-api-guide.md)


