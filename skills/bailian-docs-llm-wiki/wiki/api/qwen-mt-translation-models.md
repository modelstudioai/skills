# qwen mt translation models

Qwen MT 系列模型是阿里云百炼平台提供的专业化机器翻译模型族，覆盖文本、图像、多模态文档及音频等输入形态，支持高精度、高保真、可定制的端到端翻译服务。所有模型均通过统一的业务空间（Workspace）域名接入，需配合 DashScope API Key 使用。开发者可根据输入类型、延迟要求与领域需求选择对应模型。

## 支持的模型/功能

- **`qwen-mt-plus`**：纯文本翻译模型，基于 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)调用，支持术语干预（`terms`）、翻译记忆（`tm_list`）、领域提示（`domains`）和自动语言检测（`source_lang: "auto"`）。详见 [Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)。
- **`qwen-mt-uni`**：全模态翻译模型，支持文本（`source_texts`）、PDF/DOCX/PPTX/XLSX/TXT/HTML/Markdown 文档、JPG/PNG 图像、MP3/WAV 音频等输入格式，输出保持原始格式（如译后 PDF、带文字替换的 JPG）。提供同步与异步两种调用模式，适用于从短文本到长文档/大文件的全场景。详见 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)。
- **`qwen-mt-image-2.0` / `qwen-mt-image`**：专用图像翻译模型，精准识别并翻译图像内文字，保留原始排版与图像尺寸。`qwen-mt-image-2.0` 支持全部 55 种语种间互译；`qwen-mt-image` 仅支持源或目标语言至少一方为中/英文的组合。两者均支持敏感词过滤（`sensitives`）、术语干预（`terminologies`）与图像主体分割控制（`imageSegment`）。详见 [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md)。

> **注意**：`qwen-mt-image` 模型**必须使用异步调用**（即请求头含 `X-DashScope-Async: enable`），而 `qwen-mt-image-2.0` 同时支持同步与异步。该限制在 [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md) 中明确说明，但部分旧示例未强调，实际集成时须严格遵守。

## 关键参数

| 参数名 | 类型 | 是否必填 | 说明 | 所属模型 |
|--------|------|----------|------|----------|
| `source_lang` | `string` | 否（`qwen-mt-plus` 可选；`qwen-mt-uni`/`qwen-mt-image` 必填） | 源语言代码或全称（如 `"zh"` 或 `"Chinese"`），`"auto"` 表示自动检测。`qwen-mt-image` 要求与 `target_lang` 不同且至少一方为中/英。 | 全部 |
| `target_lang` | `string` | 是 | 目标语言代码或全称（如 `"en"` 或 `"English"`），`qwen-mt-image` 同样受中/英限制。 | 全部 |
| `translation_options` | `object` | 是（`qwen-mt-plus`） | 包含 `source_lang`, `target_lang`, `terms`, `tm_list`, `domains` 等子字段，需置于 `extra_body` 中。 | `qwen-mt-plus` |
| `input.source_texts` 或 `input.fileUrl` | `string \| string[]` | 是（二选一） | `qwen-mt-uni` 的核心输入：纯文本数组或公网可访问的文件 URL（PDF/DOCX/JPG/MP3 等）。二者**必须且只能提供一个**。 | `qwen-mt-uni` |
| `input.image_url` | `string` | 是 | `qwen-mt-image-*` 的图像输入 URL，支持 JPG/JPEG/PNG/BMP/WEBP 等格式，大小 ≤100 MB，宽高 15–8192 px。 | `qwen-mt-image-*` |
| `ext.glossary` | `array` | 否 | `qwen-mt-uni` 术语表，格式 `[{"src": "...", "tgt": "..."}]`，最多 100 组。 | `qwen-mt-uni` |
| `ext.terminologies` | `array` | 否 | `qwen-mt-image-*` 术语表，格式同上，语种需与 `source_lang`/`target_lang` 严格匹配。 | `qwen-mt-image-*` |
| `ext.domainHint` | `string` | 否 | **仅支持英文**，最多 200 单词，用于引导领域风格（如 `"These sentences are from B2C e-commerce..."`）。三类模型均支持，但 [Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md) 中 `domains` 字段为字符串而非 `domainHint`，属命名不一致。 |

> **注意**：`qwen-mt-plus` 使用 `domains` 字段（字符串），而 `qwen-mt-uni` 和 `qwen-mt-image-*` 使用 `ext.domainHint`（字符串），二者语义相同但参数路径与命名不同，集成时需按模型区分。

## 使用方式

- **统一接入点**：所有模型均通过业务空间专属域名调用，格式为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com`，其中 `{WorkspaceId}` 在百炼控制台「业务空间详情」页获取。地域支持北京（`cn-beijing`）、新加坡（`ap-southeast-1`）、美国弗吉尼亚（`us-east-1`）。[Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md) 明确建议迁移至新域名以获得更高稳定性。
- **认证方式**：通过环境变量 `DASHSCOPE_API_KEY` 或请求头 `Authorization: Bearer <API_KEY>` 认证。
- **调用模式**：
  - `qwen-mt-plus`：仅同步，使用 OpenAI SDK 的 `chat.completions.create()` 方法，`translation_options` 传入 `extra_body`（Python）或顶层参数（Node.js）。
  - `qwen-mt-uni`：同步调用地址为 `/api/v1/services/aigc/multimodal-generation/generation`；异步需加请求头 `X-DashScope-Async: enable` 并轮询 `/api/v1/tasks/{task_id}`。
  - `qwen-mt-image-*`：同步调用地址为 `/api/v1/services/aigc/image2image/image-synthesis`（仅 `qwen-mt-image-2.0` 支持）；异步调用同上，但 `qwen-mt-image` **强制异步**。

## 限制和注意事项

- **语言限制**：`qwen-mt-image` 不支持非中/英语种间的直接翻译（如日→韩），而 `qwen-mt-image-2.0` 和 `qwen-mt-uni` 无此限制。
- **文件限制**：`qwen-mt-uni` 单文件 ≤100 MB、文档 ≤200 页、音频 3 秒–60 分钟；`qwen-mt-image-*` 图像 ≤100 MB、宽高 15–8192 px、宽高比 1:10 至 10:1。
- **术语与敏感词**：`qwen-mt-plus` 的 `terms` 和 `tm_list` 为 JSON 数组；`qwen-mt-uni` 的 `glossary` 和 `qwen-mt-image-*` 的 `terminologies` 格式相同但参数名不同；所有敏感词（`sensitives`）均**区分大小写**且要求**完全匹配**。
- **领域提示**：`domainHint`（`qwen-mt-uni`/`qwen-mt-image-*`）与 `domains`（`qwen-mt-plus`）均仅接受英文描述，中文提示将导致效果下降或报错。
- **兼容性**：`qwen-mt-image` 旧版参数 `skipImgSegment` 已被 `imageSegment` 替代，虽仍兼容但应优先使用新参数。该说明见于 [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md)。

## 来源文档

- [Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)
- [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md)


