# qwen mt translation models

Qwen-MT 系列模型是阿里云百炼平台提供的专业机器翻译能力集合，覆盖文本、图像、文档、音频等多模态输入场景，支持术语干预、领域提示、翻译记忆、敏感词过滤等企业级定制功能。所有模型均通过统一的 DashScope API 协议提供服务，兼容 OpenAI SDK 调用方式，并支持同步与异步两种调用模式。

## 支持的模型/功能

- **`qwen-mt-plus`**：纯文本翻译模型，支持中英等主流语种互译，适用于高精度、低延迟的文本翻译场景。支持 `translation_options` 参数配置源/目标语言、术语表（`terms`）、翻译记忆（`tm_list`）和领域提示（`domains`）。详见 [Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)。
- **`qwen-mt-image` / `qwen-mt-image-2.0`**：图像翻译专用模型，可精准识别并翻译图片中的文字，同时保留原始排版与视觉结构。`qwen-mt-image-2.0` 支持 55 种语言间任意互译；`qwen-mt-image` 仅支持源/目标语种至少一方为中文或英文。两者均支持 `imageSegment` 主体分割、`sensitives` 敏感词过滤及 `terminologies` 术语干预。
- **`qwen-mt-uni`**：全模态统一翻译模型，支持文本（字符串/数组）、PDF/DOCX/PPTX/XLSX/TXT/HTML/Markdown 文档、JPG/PNG 图像、MP3/WAV 音频等 10+ 格式输入，自动识别模态并执行端到端高保真翻译与格式重构。其设计目标是“一个接口、多种输入、一致体验”，是当前推荐的通用翻译入口。该模型的详细能力说明见 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)。

> **注意**：文档 1 中 `qwen-mt-plus` 的 `domains` 字段示例被截断（末尾为 `"profe"`），且未说明字段实际名称应为 `domainHint`（与 `qwen-mt-image` 和 `qwen-mt-uni` 保持一致）。正确字段名以 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 和 [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md) 为准。

## 关键参数

| 参数 | 类型 | 说明 | 所属模型 |
|------|------|------|----------|
| `source_lang` / `target_lang` | `string` | 源/目标语言标识，支持全称（如 `"Chinese"`）、ISO 639-1 编码（如 `"zh"`）或 `"auto"`（仅 `source_lang`）。`qwen-mt-image` 要求至少一端为 `zh`/`en`；`qwen-mt-image-2.0` 和 `qwen-mt-uni` 无此限制。 | 全部 |
| `terms` / `terminologies` / `glossary` | `array` | 术语干预列表。`qwen-mt-plus` 使用 `terms`（字段名不同）；`qwen-mt-image` 使用 `terminologies`；`qwen-mt-uni` 使用 `glossary`。三者结构均为 `{"src": "...", "tgt": "..."}`，语种需与 `source_lang`/`target_lang` 严格匹配。 | `qwen-mt-plus`, `qwen-mt-image`, `qwen-mt-uni` |
| `tm_list` | `array` | 翻译记忆（Translation Memory）列表，仅 `qwen-mt-plus` 支持，格式为 `{"source": "...", "target": "..."}`。 | `qwen-mt-plus` |
| `domainHint` | `string` | **英文**领域提示，用于引导译文风格（如技术文档、电商客服）。最大 200 英文单词。`qwen-mt-plus` 文档中误标为 `domains`，应统一使用 `domainHint`。 | `qwen-mt-plus`, `qwen-mt-image`, `qwen-mt-uni` |
| `sensitives` | `array` | 敏感词列表，**大小写敏感**，完全匹配时跳过翻译并保留原文。建议 ≤50 项。 | `qwen-mt-image`, `qwen-mt-uni` |
| `imageSegment` | `boolean` | 是否跳过图像主体（人物、商品、Logo）上的文字翻译。默认 `false`。旧参数 `skipImgSegment` 已废弃，见 [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md)。 | `qwen-mt-image`, `qwen-mt-uni` |

## 使用方式

- **文本翻译（`qwen-mt-plus`）**：使用 [OpenAI 兼容接口](../concepts/openai-compatibility.md)，`POST /compatible-mode/v1/chat/completions`，将 `translation_options` 作为 `extra_body`（Python）或顶层字段（Node.js/curl）传入。
- **图像翻译（`qwen-mt-image-*`）**：使用 DashScope 专用接口，`POST /api/v1/services/aigc/image2image/image-synthesis`，请求体为 `input` 对象，含 `image_url`、`source_lang`、`target_lang` 等字段。
- **全模态翻译（`qwen-mt-uni`）**：使用 DashScope 统一接口，`POST /api/v1/services/aigc/multimodal-generation/generation`，通过 `fileUrl`（文件 URL）或 `source_texts`（文本）指定输入，自动路由处理。
- **同步 vs 异步**：
  - 同步：直接返回结果（文本内容或文件 URL），适合小文本、单图、短音频（≤60s）。
  - 异步：请求头添加 `X-DashScope-Async: enable`，先获 `task_id`，再轮询 `GET /api/v1/tasks/{task_id}` 获取结果，适合大文档（>200页）、长音频（>60s）等耗时任务。

## 限制和注意事项

- **地域与域名**：推荐使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），而非旧版 `dashscope.aliyuncs.com`。北京、新加坡、美国（弗吉尼亚）地域均支持，`{WorkspaceId}` 需在控制台获取。[Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md) 明确指出旧域名“仍可正常使用”，但新域名“提供卓越性能和更高稳定性”。
- **输入限制**：
  - 图像：宽高 15–8192 px，宽高比 1:10 至 10:1，格式 JPG/JPEG/PNG/BMP/PNM/PPM/TIFF/WEBP，大小 ≤100 MB。
  - 文档/音频：单文件 ≤100 MB，文档 ≤200 页，音频时长 3s–60min。
  - URL：必须公网可访问、不含中文字符。
- **语言识别**：`source_lang="auto"` 仅在 `qwen-mt-image-2.0` 和 `qwen-mt-uni` 中稳定支持；`qwen-mt-plus` 自动识别能力有限，建议显式指定。
- **领域提示**：所有模型的 `domainHint` **仅接受英文描述**，中文提示无效。
- **错误处理**：`qwen-mt-plus`（OpenAI 兼容）失败时返回 OpenAI 格式 error object；`qwen-mt-image` 和 `qwen-mt-uni`（DashScope 原生）失败时顶层返回 `code`/`message` 字段，成功时返回 `output` 对象。务必按协议区分响应结构。

## 来源文档

- [Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md)
- [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)


