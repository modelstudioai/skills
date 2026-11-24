# qwen mt translation models

Qwen MT 系列模型是阿里云百炼平台提供的专业机器翻译能力集合，覆盖文本、图像、文档、音频等多模态输入场景。核心模型包括面向纯文本的 `qwen-mt-plus`（[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)）、面向图像的 `qwen-mt-image`/`qwen-mt-image-2.0`，以及统一处理多模态输入的 `qwen-mt-uni`。所有模型均支持术语干预、领域提示、敏感词过滤等生产级定制功能。

## 支持的模型与功能

- **`qwen-mt-plus`**：纯文本翻译模型，通过 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)调用，支持源/目标语言自动检测、术语表（`terms`）、翻译记忆（`tm_list`）和领域提示（`domains`）。详见 [Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)。
- **`qwen-mt-image` 与 `qwen-mt-image-2.0`**：专用于图像翻译，可精准识别并重排版图像内文字。`qwen-mt-image-2.0` 支持全部 55 种语言互译；`qwen-mt-image` 仅支持源或目标语种至少有一项为中文或英文的组合。二者均支持 `imageSegment` 主体分割控制。详见 [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md)。
- **`qwen-mt-uni`**：全模态统一翻译模型，支持文本（字符串/数组）、PDF/DOCX/PPTX/XLSX/TXT/HTML/Markdown、JPG/PNG、MP3/WAV 等输入格式，并原格式输出。同步/异步双模式，内置智能路由与跨模态重构能力。详见 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)。

> **注意**：文档 1 中称 `qwen-mt-image` “不支持在非中/英语种之间直接翻译”，而文档 3 的 `qwen-mt-uni` 明确支持任意语言对（如日→韩），且其图像处理路径实际复用 `qwen-mt-image-2.0` 能力。因此 `qwen-mt-image` 的语种限制是旧版模型约束，新业务应优先选用 `qwen-mt-uni` 或 `qwen-mt-image-2.0`。

## 关键参数

| 参数 | 作用 | 适用模型 | 说明 |
|------|------|----------|------|
| `source_lang` / `target_lang` | 指定源/目标语言 | 全部 | 支持语种编码（`zh`, `en`）或全称（`Chinese`, `English`），`auto` 表示自动检测；`qwen-mt-image` 对语种组合有额外限制。 |
| `ext.domainHint` | 领域风格提示 | 全部 | **仅支持英文**，建议 ≤200 单词；影响译文术语选择与表达风格。 |
| `ext.sensitives` | 敏感词过滤列表 | 全部 | **大小写敏感**，完全匹配时保留原文不翻译；单次请求 ≤50 项。 |
| `ext.terminologies`（`qwen-mt-image`）<br>`ext.glossary`（`qwen-mt-uni`）<br>`translation_options.terms`（`qwen-mt-plus`） | 术语强制干预 | 全部 | 格式均为 `{"src": "...", "tgt": "..."}`；`qwen-mt-uni` 最多支持 100 组。 |
| `ext.config.imageSegment` | 图像主体分割开关 | `qwen-mt-image*` 和 `qwen-mt-uni`（仅图像输入生效） | `true` 时跳过人物/商品/Logo 上的文字；旧参数 `skipImgSegment` 已弃用，见 [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md)。 |

## 使用方式

- **文本翻译（`qwen-mt-plus`）**：使用 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)，`POST /chat/completions`，将翻译选项置于 `translation_options` 字段（或 `extra_body` 中）。支持北京、新加坡、美国（弗吉尼亚）三地域。
- **图像翻译（`qwen-mt-image*`）**：使用 DashScope 原生接口，`POST /api/v1/services/aigc/image2image/image-synthesis`。必须指定 `X-DashScope-Async: enable` 头才能异步调用；`qwen-mt-image` **不支持同步调用**（文档 1 中同步调用示例仅适用于 `qwen-mt-image-2.0`）。
- **全模态翻译（`qwen-mt-uni`）**：使用 DashScope 原生接口，`POST /api/v1/services/aigc/multimodal-generation/generation`。通过 `input.fileUrl`（文件 URL）或 `input.source_texts`（文本）二选一传入；响应结构统一，成功时返回 `output.Data.TranslatedFileUrl` 或 `output.Data.TranslatedTexts`。
- **通用前提**：需已获取 API Key 并配置至环境变量 `DASHSCOPE_API_KEY`，Workspace ID 需从控制台获取并替换 URL 中的 `{WorkspaceId}`。

## 限制和注意事项

- **格式与尺寸**：图像输入支持 JPG/JPEG/PNG/BMP/PNM/PPM/TIFF/WEBP，宽高 15–8192px，宽高比 1:10 至 10:1，单文件 ≤100 MB；文档类（PDF/DOCX 等）≤100 MB 且 ≤200 页；音频（MP3/WAV）时长 3 秒–60 分钟。URL 中禁止含中文字符。
- **异步任务管理**：`task_id` 有效期 24 小时；查询结果接口默认 RPS=1；译后文件 URL 有效期亦为 24 小时，需及时下载。
- **术语与敏感词**：`qwen-mt-image` 的 `terminologies` 与 `qwen-mt-uni` 的 `glossary` 功能等价，但字段名不同；`qwen-mt-plus` 的 `terms` 字段位于 `translation_options` 内层，结构略有差异。
- **错误处理**：同步调用失败时顶层返回 `code`/`message`；异步调用创建任务失败同理，但任务执行失败需检查 `output.Success === false`（即使 `task_status === "SUCCEEDED"`）。所有错误码详见 [错误码文档](../../raw/model-api-reference/preparations/error-code.md)。

## 来源文档

- [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md)
- [Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)
- [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)


