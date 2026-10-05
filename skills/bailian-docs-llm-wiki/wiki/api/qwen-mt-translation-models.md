# qwen mt translation models

Qwen MT 系列模型是阿里云百炼平台提供的专业机器翻译能力集合，覆盖文本、图像、文档、音频等多模态输入场景。其核心模型包括面向纯文本的 `qwen-mt-plus`（[OpenAI 兼容接口](../concepts/openai-compatible-api.md)）、面向图像的 `qwen-mt-image`/`qwen-mt-image-2.0`，以及统一处理多模态输入的 `qwen-mt-uni`。所有模型均支持术语干预、领域提示、敏感词过滤等企业级定制功能，并提供同步与异步两种调用模式。

## 支持的模型与功能

- **`qwen-mt-plus`**：纯文本翻译模型，通过 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)调用，支持中英日韩等主流语言互译，适用于 API 集成和 SDK 快速接入。详情见 [Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)。
- **`qwen-mt-image` 与 `qwen-mt-image-2.0`**：专用于图像翻译的模型，可精准识别并翻译图像内文字，同时保留原始排版与视觉结构。`qwen-mt-image-2.0` 支持全部 55 种语种间的任意互译；而 `qwen-mt-image` 仅支持源或目标语种至少有一项为中文或英文的组合（如日→中、英→法），不支持日→韩等非中/英语种直译。该差异在 [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md) 中明确说明。
- **`qwen-mt-uni`**：全模态统一翻译模型，支持文本（字符串/数组）、PDF/DOCX/PPTX/XLSX/TXT/HTML/Markdown、JPG/PNG、MP3/WAV 等十余种格式输入，并自动重构为同格式输出。它是目前功能最完备、适用场景最广的 Qwen MT 模型，详见 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)。

> **注意**：文档 1 中称 `qwen-mt-image` “支持中/英文与其他语种之间的互译”，但未明确禁止非中/英语种间互译；而文档 3 的 `qwen-mt-uni` 在图像处理路径中实际复用了 `qwen-mt-image-2.0` 的能力，且明确支持任意语种对。因此，若需跨非中/英语种图像翻译，应优先选用 `qwen-mt-image-2.0` 或 `qwen-mt-uni`，避免使用已受限的 `qwen-mt-image`。

## 关键参数

所有模型共用以下核心参数（命名与语义高度一致，便于迁移）：

- **`source_lang`**：源语言标识，支持语种全称（如 `"Chinese"`）、ISO 639-1 编码（如 `"zh"`）或 `"auto"`（自动检测）。`qwen-mt-image` 对其有语种组合限制，`qwen-mt-uni` 和 `qwen-mt-plus` 无此限制。
- **`target_lang`**：目标语言标识，要求与 `source_lang` 不同，格式同上。
- **`ext` 对象**（各模型字段名略有差异，但功能等价）：
  - `domainHint`（字符串）：英文领域提示，≤200 单词，用于引导译文风格。[千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md) 和 [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md) 均强调“仅支持英文”。
  - `sensitives` / `sensitives` / `sensitives`（字符串数组）：敏感词列表，**完全匹配、大小写敏感**，单次请求 ≤50 项。
  - `terminologies`（`qwen-mt-image`） / `terms`（`qwen-mt-plus`） / `glossary`（`qwen-mt-uni`）：术语干预表，格式均为 `{"src": "...", "tgt": "..."}`，语种需与 `source_lang`/`target_lang` 严格对应。
  - `config.imageSegment`（布尔值）：**仅图像输入生效**，控制是否跳过人物/商品/Logo 等主体区域的文字翻译。旧参数 `skipImgSegment` 已废弃，建议统一使用 `imageSegment`。

## 使用方式

- **文本翻译（`qwen-mt-plus`）**：使用 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)，`POST /compatible-mode/v1/chat/completions`，将原文放入 `messages[0].content`，翻译选项置于 `translation_options`（非 `extra_body` 内嵌对象，Node.js/Python SDK 示例已验证该结构有效）。
- **图像翻译（`qwen-mt-image-*`）**：使用 DashScope 原生接口，`POST /api/v1/services/aigc/image2image/image-synthesis`，通过 `input.image_url` 传图，必须指定 `X-DashScope-Async: enable` 头以启用异步（`qwen-mt-image` 强制异步；`qwen-mt-image-2.0` 同步/异步均可）。
- **多模态翻译（`qwen-mt-uni`）**：使用 DashScope 统一接口，`POST /api/v1/services/aigc/multimodal-generation/generation`，支持 `input.fileUrl`（任意支持格式）或 `input.source_texts`（字符串或数组）两种输入方式，同样通过 `X-DashScope-Async: enable` 控制同步/异步模式。

所有调用均需配置 `Authorization: Bearer ${DASHSCOPE_API_KEY}` 及 `Content-Type: application/json`，并替换 `{WorkspaceId}` 为实际业务空间 ID。地域 URL 因地而异，推荐使用专属域名（如北京：`{WorkspaceId}.cn-beijing.maas.aliyuncs.com`）而非旧版 `dashscope.aliyuncs.com`。

## 限制和注意事项

- **语种限制**：`qwen-mt-image` 存在明确的语种组合约束（必须含中或英），而 `qwen-mt-image-2.0` 和 `qwen-mt-uni` 支持全部 55 种语言任意互译。开发者应根据需求选择模型，避免因语种不匹配导致 `InvalidParameter` 错误。
- **输入限制**：
  - 图像：宽高 15–8192 px，宽高比 1:10 至 10:1，格式 JPG/JPEG/PNG/BMP/PNM/PPM/TIFF/WEBP，大小 ≤100 MB；
  - 文档/音频（`qwen-mt-uni`）：单文件 ≤100 MB，PDF/DOCX/PPTX ≤200 页，音频时长 3 秒–60 分钟；
  - 所有 URL：不得含中文字符。
- **异步任务管理**：`task_id` 有效期为 24 小时，查询结果接口（`GET /api/v1/tasks/{task_id}`）默认 RPS 为 1；任务成功后返回的 `TranslatedFileUrl` 同样仅 24 小时有效，需及时下载。
- **术语与敏感词**：`glossary`（`qwen-mt-uni`）最多支持 100 组术语，而 `terminologies`（`qwen-mt-image`）和 `terms`（`qwen-mt-plus`）未明确上限，但文档均建议单次 ≤50 项以保障效果。
- > **注意**：文档 2 的 `qwen-mt-plus` 示例中 `translation_options` 字段在 curl 请求体中直接平级出现，而 Python SDK 需通过 `extra_body` 传入；文档 3 的 `qwen-mt-uni` 则始终将 `ext` 作为 `input` 的子对象。参数嵌套层级差异属接口设计使然，非错误，开发者需按对应模型文档组织 payload 结构。

## 来源文档

- [千问-图像翻译API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-image-api.md)
- [Qwen-MT API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-api.md)
- [Qwen-MT-Uni API参考](../../raw/model-api-reference/qwen-mt-translation-models/qwen-mt-uni-api.md)


