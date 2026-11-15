# qwen mt translation models

Qwen-MT 系列模型是阿里云百炼平台提供的专业机器翻译能力集合，覆盖文本、图像、音频及多格式文档等全模态输入场景。模型通过统一架构实现高保真语义理解与格式还原，支持术语干预、领域提示、翻译记忆等企业级定制功能。所有模型均通过 DashScope 标准 API 或 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)调用，适配不同业务规模与延迟敏感度需求。

## 支持的模型/功能

- **`qwen-mt-plus`**：纯文本翻译模型，支持中英等主流语言互译，提供术语干预（`terms`）、翻译记忆（`tm_list`）和领域提示（`domains`）能力。使用 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)，详见 [Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)。
- **`qwen-mt-image` / `qwen-mt-image-2.0`**：图像翻译专用模型，可精准识别并翻译图片内文字，保留原始排版与视觉结构；`qwen-mt-image-2.0` 支持 55 种语言互译，而 `qwen-mt-image` 仅支持源/目标语言至少一方为中文或英文。详细参数与限制见 [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md)。
- **`qwen-mt-uni`**：全模态统一翻译模型，支持文本字符串、PDF/DOCX/PPTX/XLSX/TXT/HTML/Markdown 文档、JPG/PNG 图像、MP3/WAV 音频等多种输入格式，并自动重构为对应格式的译后文件。其设计目标是“一次接入、多模态复用”，能力覆盖范围最广，参见 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)。

> **注意**：`qwen-mt-image` 与 `qwen-mt-uni` 均支持图像翻译，但 `qwen-mt-image` 仅接受图像输入，而 `qwen-mt-uni` 可在同一接口下处理图像、文档、音频等混合类型——开发者应根据输入模态复杂度选择：若仅需图像翻译且对语种支持要求高（如日→韩），优先选 `qwen-mt-image-2.0`；若需统一接入多类型文件，必须使用 `qwen-mt-uni`。

## 关键参数

所有模型共用以下核心参数（命名与语义一致，但字段路径略有差异）：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `source_lang` | `string` | 否（`qwen-mt-plus` 和 `qwen-mt-image` 中为必填；`qwen-mt-uni` 中可选，不填则自动识别） | 源语言标识，支持全称（如 `"Chinese"`）、ISO 639-1 编码（如 `"zh"`）或 `"auto"`。`qwen-mt-image` 要求源/目标语言至少含中/英文；`qwen-mt-image-2.0` 和 `qwen-mt-uni` 无此限制。 |
| `target_lang` | `string` | 是 | 目标语言标识，同上。值必须与 `source_lang` 不同。 |
| `terms` / `terminologies` / `glossary` | `array` | 否 | 术语干预列表。`qwen-mt-plus` 使用 `terms`（对象数组，含 `source`/`target` 字段）；`qwen-mt-image` 使用 `terminologies`（含 `src`/`tgt`）；`qwen-mt-uni` 使用 `glossary`（同样含 `src`/`tgt`）。三者语义完全一致，均为强制术语映射。 |
| `domainHint` | `string` | 否 | 领域提示，**仅支持英文描述**（建议 ≤200 单词），用于引导译文风格。该参数在 `qwen-mt-image` 和 `qwen-mt-uni` 的 `ext` 对象中；`qwen-mt-plus` 使用 `domains` 字段（文档中示例截断，但语义相同）。 |
| `sensitives` / `sensitives` | `array` | 否 | 敏感词过滤列表，**大小写敏感**，完全匹配时跳过翻译。`qwen-mt-image` 与 `qwen-mt-uni` 均使用 `sensitives` 字段，最大 50 项。 |

> **注意**：`qwen-mt-plus` 的 `domains` 字段在文档 1 中示例被意外截断（末尾为 `profe`），完整字段名应为 `domains`，且内容须为英文描述；而 `qwen-mt-image` 和 `qwen-mt-uni` 统一使用 `domainHint`。开发者应以实际 API 字段名为准，避免因命名差异导致请求失败。

## 使用方式

- **文本翻译（`qwen-mt-plus`）**：使用 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)，`POST /chat/completions`，将 `translation_options` 作为 `extra_body`（Python SDK）或顶层字段（Node.js/curl）传入。[Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md) 提供了各语言 SDK 示例。
- **图像翻译（`qwen-mt-image-*`）**：使用 DashScope 专属接口 `POST /api/v1/services/aigc/image2image/image-synthesis`，同步模式直接返回译后图 URL；异步模式需先创建任务再轮询。注意 `qwen-mt-image` **必须**使用异步（带 `X-DashScope-Async: enable` 头），而 `qwen-mt-image-2.0` 支持同步。
- **全模态翻译（`qwen-mt-uni`）**：使用 DashScope 接口 `POST /api/v1/services/aigc/multimodal-generation/generation`，通过 `input.fileUrl`（文件 URL）或 `input.source_texts`（文本）指定输入。同步/异步切换仅依赖 `X-DashScope-Async` 请求头，其余参数完全一致。[Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 明确定义了响应结构与轮询逻辑。

所有调用均需配置：
- `Authorization: Bearer ${DASHSCOPE_API_KEY}`
- `base_url` 或请求地址中的 `{WorkspaceId}` 替换为真实业务空间 ID（见控制台「业务空间详情」）
- 推荐使用新域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）而非旧 `dashscope.aliyuncs.com`，以获得更高稳定性与性能。

## 限制和注意事项

- **地域与域名**：北京、新加坡、美国（弗吉尼亚）地域均支持全部模型，但 `qwen-mt-image` 仅明确列出华北2（北京）和新加坡；`qwen-mt-uni` 文档未列明地域限制，实践中三地均可调用。务必使用业务空间专属域名（`{WorkspaceId}.<region>.maas.aliyuncs.com`），旧域名虽兼容但不推荐。
- **输入限制**：
  - 图像：宽高 15–8192 px，宽高比 1:10 至 10:1，格式 JPG/JPEG/PNG/BMP/PNM/PPM/TIFF/WEBP，大小 ≤100 MB（`qwen-mt-image` 和 `qwen-mt-uni` 共同要求）。
  - 文档/音频：`qwen-mt-uni` 明确限制单文件 ≤100 MB、文档 ≤200 页、音频 3 秒–60 分钟；`qwen-mt-plus` 和 `qwen-mt-image` 无显式文档/音频支持。
- **术语与领域**：`domainHint` 和 `domains` 字段**仅接受英文输入**，中文提示将导致效果下降或报错；`glossary`（`qwen-mt-uni`）和 `terms`（`qwen-mt-plus`）中 `src`/`source` 必须与 `source_lang` 一致，`tgt`/`target` 必须与 `target_lang` 一致。
- **异步任务管理**：`qwen-mt-image` 和 `qwen-mt-uni` 的异步任务 `task_id` 有效期为 24 小时，查询接口默认 RPS 为 1；译后文件 URL（如 `TranslatedFileUrl`）同样有效期 24 小时，需及时下载。
- **错误处理**：`qwen-mt-plus`（OpenAI 兼容）失败时返回标准 OpenAI 错误格式；`qwen-mt-image` 和 `qwen-mt-uni`（DashScope 标准）失败时顶层返回 `code`/`message`，成功时返回 `output` 对象。请勿混淆两种错误响应结构。

## 来源文档

- [Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)
- [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md)
- [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)


