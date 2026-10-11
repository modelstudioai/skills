# 内容安全过滤

内容安全过滤是百炼平台提供的核心安全能力，用于在模型输入（用户请求）和输出（模型生成）环节，实时识别并拦截涉政、暴恐、色情、违禁、广告等高风险内容，保障应用合规性与用户体验。该能力由统一策略引擎驱动，支持规则+轻量多模态模型融合检测，不依赖大语言模型推理资源。

## 在百炼平台的不同场景中，这个概念如何使用

内容安全过滤以三种互补方式集成到平台各层，开发者可根据需求选择粒度与控制权：

- **独立 Security API**：适用于需自主编排安全链路的场景（如前置审核、批量审计）。直接调用 `POST /api/v1/security/detect`，支持文本（≤65536 字符）和图片（JPEG/PNG，≤10 MB），同步返回 `suggestion`（`pass`/`review`/`block`）、`risk_level` 和细粒度 `labels`（如 `politics`, `porn`）。适合与自有风控系统对接或离线扫描。

- **模型 API 内置安全参数**：在 `chat/completions` 等模型调用中，通过请求体 `security` 对象启用端到端防护。设置 `input_filter=true` 拦截恶意指令与敏感输入，`output_filter=true` 阻断高危生成内容；指定 `security_policy_id` 可复用预置或自定义策略（如“金融行业专用策略”）。此方式自动适配 Qwen 系列等所有托管大模型，但不支持第三方模型或 Embedding/Rerank 模型。

- **HTTP 请求头护栏（AI 安全护栏）**：最轻量接入方式，无需修改业务逻辑。在任意模型 API 请求头添加 `X-DashScope-DataInspection: {"input":"cip","output":"cip"}` 即可启用双路检测。违规时直接返回 `400 DataInspectionFailed` 错误，无模型输出泄露。适用于快速上线、灰度验证或 CLI 工具链（如 `bailian-cli --security-policy-id`）。

> ⚠️ 注意：流式响应（`stream=true`）下，内容安全过滤仅在流结束时执行最终校验，不支持逐 token 实时拦截。

## 关键参数和配置

| 参数 | 位置 | 类型 | 说明 | 默认值 |
|------|------|------|------|--------|
| `security_policy_id` | `security` 对象内（模型 API） | string | 指定策略 ID；为空则禁用防护 | `null` |
| `input_filter` / `output_filter` | `security` 对象内（模型 API） | boolean | 控制是否启用输入/输出过滤 | `true` / `true` |
| `audit_level` | `security` 对象内（模型 API） | `none`/`basic`/`full` | 审计深度，影响日志保留与溯源能力 | `basic` |
| `categories` | Security API 请求体 | string[] | 指定检测风险类型（如 `["politics", "porn"]`），留空启用全部默认类别 | 全部启用 |
| `return_categories` | Security API 请求体 | boolean | 是否返回各子类别的置信度分数 | `false` |
| `timeout` | Security API 请求体 | integer | 检测超时时间（秒），范围 1–30 | `15` |
| `X-DashScope-DataInspection` | HTTP 请求头 | JSON string | 启用 AI 安全护栏，值为 `{"input":"cip","output":"cip"}` | 未设置即禁用 |

> ✅ 提示：Security API 的 `image_base64` 必须为标准 Base64（无换行、无前缀），且需带 `data:image/<type>;base64,` 前缀；`image_url` 要求目标 URL 可公开访问且含正确 `Content-Type` 响应头。

## 面向开发者，简洁实用

- **快速启用**：优先使用 `X-DashScope-DataInspection` 请求头，5 秒完成接入；生产环境再按需升级为 `security` 对象精细控制。
- **调试建议**：测试时设 `audit_level=full` 并检查审计日志（保留 90 天），定位误报/漏报；高风险场景务必人工复核 `suggestion=review` 结果。
- **性能注意**：`output_filter=true` 增加 ≤200ms 延迟；`audit_level=full` 额外增加 300–800ms；避免在低延迟敏感路径（如实时对话）中滥用 `full` 审计。
- **限制牢记**：  
  - 图片检测不支持 GIF/SVG；  
  - Security API 不支持音频（文档中标注“尚未上线”）；  
  - 单次最多 10 文本 / 5 图片批量检测；  
  - 免费版每日限 10,000 次 Security API 调用。
- **错误处理**：模型 API 触发拦截时返回 `{"error": {"code": "content_blocked", ...}}`；Security API 返回 `400` 或 `500` 错误码，需解析 `code` 字段（如 `InputLengthExceeded`）做降级处理。

## 关联主题页

- [security api guide](../api/security-api-guide.md)
- [security guide](../guides/security-guide.md)
- [security and compliance](../guides/security-and-compliance.md)
- [application support](../guides/application-support.md)
- [rag api](../api/rag-api.md)


