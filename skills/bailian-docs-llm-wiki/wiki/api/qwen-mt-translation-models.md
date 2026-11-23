# qwen mt translation models

Qwen MT 系列模型是阿里云百炼平台提供的专业化机器翻译能力集合，覆盖纯文本、图像、多格式文档及音频等全模态输入场景。模型采用统一架构设计，支持术语干预、领域提示、翻译记忆、敏感词过滤等企业级定制功能，并提供同步与异步两种调用模式以适配不同业务时延要求。所有模型均通过 DashScope 标准 API 协议或 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)提供服务。

## 支持的模型/功能

- **`qwen-mt-plus`**：纯文本翻译模型，支持中英等主流语种互译，适用于 API 集成场景。提供术语干预（`terms`）、翻译记忆（`tm_list`）和领域提示（`domains`）能力。[Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md) 详细说明了其 OpenAI 兼容调用方式。
- **`qwen-mt-image` / `qwen-mt-image-2.0`**：图像翻译专用模型，可精准识别并翻译图片中的文字，同时保留原始排版与视觉结构。`qwen-mt-image-2.0` 支持全部 55 种语言互译；`qwen-mt-image` 仅支持源/目标语种至少一方为中文或英文的组合。[千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md) 提供了图像格式、尺寸、URL 约束等关键限制。
- **`qwen-mt-uni`**：全模态统一翻译模型，支持文本（字符串/数组）、PDF/DOCX/PPTX/XLSX/TXT/HTML/Markdown、JPG/PNG、MP3/WAV 等多种输入格式，并自动重构为对应格式的译后文件。该模型是 `qwen-mt-image` 和 `qwen-mt-plus` 的超集，推荐新项目优先选用。[Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 明确了其跨模态路由机制与统一响应结构。

> **注意**：`qwen-mt-image` 与 `qwen-mt-uni` 均支持图像翻译，但 `qwen-mt-image` 仅接受图像输入，而 `qwen-mt-uni` 可处理图像、文档、音频等任意模态。二者在参数命名上存在差异（如术语表字段分别为 `terminologies` 和 `glossary`），实际使用时需按模型文档严格匹配。

## 关键参数

| 参数名 | 类型 | 是否必选 | 说明 | 所属模型 |
|--------|------|----------|------|----------|
| `source_lang` | `string` | 条件必选 | 源语言（全称或 ISO 639-1 编码），支持 `auto` 自动检测。`qwen-mt-plus` 中默认为 `auto`；`qwen-mt-image` 和 `qwen-mt-uni` 中若未指定则强制启用自动识别。 | 全部 |
| `target_lang` | `string` | 必选 | 目标语言（全称或编码），不可与 `source_lang` 相同。 | 全部 |
| `translation_options`（OpenAI 兼容） | `object` | 必选（当使用 `qwen-mt-plus` 时） | 包含 `source_lang`、`target_lang`、`terms`、`tm_list`、`domains` 等子字段。注意：此对象需置于 `extra_body` 中传入。 | `qwen-mt-plus` |
| `terms` / `tm_list` / `domains` | `array` / `array` / `string` | 可选 | 分别用于术语干预、翻译记忆、领域提示（仅 `qwen-mt-plus`）。领域提示内容须为英文，建议 ≤200 单词。 | `qwen-mt-plus` |
| `ext.terminologies` / `ext.sensitives` / `ext.domainHint` | `array` / `array` / `string` | 可选 | 图像模型专用扩展字段，语义与上一行一致，但字段路径和命名不同。`domainHint` 仅支持英文。 | `qwen-mt-image` |
| `ext.glossary` / `ext.sensitives` / `ext.domainHint` | `array` / `array` / `string` | 可选 | 全模态模型专用扩展字段，`glossary` 替代 `terminologies`，其余语义一致。 | `qwen-mt-uni` |
| `input.fileUrl` / `input.source_texts` | `string` / `string\|array<string>` | 条件必选（二选一） | `qwen-mt-uni` 输入载体：`fileUrl` 用于文件/图像/音频；`source_texts` 用于纯文本。二者不可共存。 | `qwen-mt-uni` |
| `config.imageSegment` | `boolean` | 可选 | 是否跳过图像主体（人物、Logo、商品）上的文字翻译。默认 `false`。`qwen-mt-image` 文档中曾使用旧参数 `skipImgSegment`，[千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md) 已明确标注其为兼容项，应优先使用 `imageSegment`。 | `qwen-mt-image`, `qwen-mt-uni` |

## 使用方式

- **文本翻译（`qwen-mt-plus`）**：使用 OpenAI SDK，配置 `base_url` 为地域专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），调用 `chat.completions.create`，将 `translation_options` 放入 `extra_body`。详见 [Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md) 中的 Python/Node.js/curl 示例。
- **图像翻译（`qwen-mt-image-*`）**：使用 HTTP POST 调用 `api/v1/services/aigc/image2image/image-synthesis` 接口，请求头需包含 `Authorization` 和 `Content-Type: application/json`，请求体为 JSON 格式，`input` 对象内含 `image_url`、`source_lang`、`target_lang` 等字段。
- **全模态翻译（`qwen-mt-uni`）**：使用 HTTP POST 调用 `api/v1/services/aigc/multimodal-generation/generation` 接口。若输入为文件 URL，设 `input.fileUrl`；若为文本，设 `input.source_texts`。同步调用直接返回结果；异步调用需添加请求头 `X-DashScope-Async: enable` 获取 `task_id`，再轮询 `GET /api/v1/tasks/{task_id}` 查询状态。
- **地域与认证**：所有模型均支持华北2（北京）、新加坡、美国（弗吉尼亚）等地域，需使用对应地域的 `base_url` 或 API endpoint，并配置有效的 `DASHSCOPE_API_KEY`。强烈建议迁移至业务空间专属域名（如 `{WorkspaceId}.cn-beijing.maas.aliyuncs.com`），以获得更高性能与稳定性。

## 限制和注意事项

- **语种限制**：`qwen-mt-image` 不支持非中/英文种之间的直译（如日→韩），而 `qwen-mt-image-2.0` 和 `qwen-mt-uni` 无此限制。务必根据业务语种需求选择模型。
- **输入约束**：
  - 图像：宽高 15–8192 px，宽高比 1:10 至 10:1，格式支持 JPG/JPEG/PNG/BMP/PNM/PPM/TIFF/WEBP，大小 ≤100 MB；
  - 文档/音频：单文件 ≤100 MB，文档 ≤200 页，音频时长 3 秒–60 分钟；
  - 所有 URL 地址中禁止包含中文字符。
- **术语与敏感词**：`terms`（`qwen-mt-plus`）、`terminologies`（`qwen-mt-image`）、`glossary`（`qwen-mt-uni`）三者语义相同但字段名不同；`sensitives` 在所有模型中均区分大小写，且为完全匹配过滤。
- **领域提示（`domainHint`/`domains`）**：当前**仅支持英文描述**，且长度建议 ≤200 英文单词，否则可能影响翻译效果。
- **异步任务管理**：`task_id` 和 `TranslatedFileUrl` 有效期均为 24 小时，需及时轮询与下载。异步查询接口默认 RPS 为 1，高频轮询请配置回调通知。

## 来源文档

- [Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md)
- [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)


